import os
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path
import streamlit as st

# RAG Dependencies
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_openai import AzureChatOpenAI

from config import AzureConfig

class RAGSystem:
    """Retrieval-Augmented Generation system for knowledge base queries"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=AzureConfig.OPENAI_API_KEY,
            openai_api_base=AzureConfig.OPENAI_ENDPOINT,
            openai_api_version=AzureConfig.OPENAI_API_VERSION,
            deployment=AzureConfig.OPENAI_DEPLOYMENT
        )
        self.vectorstore = None
        self.qa_chain = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def load_documents(self, file_paths: List[str]) -> List[Document]:
        """Load documents from various file types"""
        documents = []
        
        for file_path in file_paths:
            file_extension = Path(file_path).suffix.lower()
            
            try:
                if file_extension == '.txt':
                    loader = TextLoader(file_path, encoding='utf-8')
                elif file_extension == '.pdf':
                    loader = PyPDFLoader(file_path)
                elif file_extension in ['.docx', '.doc']:
                    loader = Docx2txtLoader(file_path)
                else:
                    st.warning(f"Unsupported file type: {file_extension}")
                    continue
                    
                docs = loader.load()
                documents.extend(docs)
                st.success(f"Loaded {len(docs)} documents from {file_path}")
                
            except Exception as e:
                st.error(f"Error loading {file_path}: {str(e)}")
                
        return documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks for better retrieval"""
        if not documents:
            return []
            
        # Split documents into chunks
        doc_splits = self.text_splitter.split_documents(documents)
        st.info(f"Split documents into {len(doc_splits)} chunks")
        
        return doc_splits
    
    def create_vectorstore(self, documents: List[Document], force_recreate: bool = False):
        """Create or load vector store from documents"""
        if not documents:
            st.warning("No documents to process")
            return
            
        # Check if vectorstore already exists
        if os.path.exists(self.persist_directory) and not force_recreate:
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                st.success("Loaded existing vector store")
                return
            except Exception as e:
                st.warning(f"Could not load existing vector store: {e}")
                force_recreate = True
        
        # Create new vector store
        try:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            st.success(f"Created vector store with {len(documents)} documents")
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            raise
    
    def setup_qa_chain(self, k: int = 4):
        """Setup the question-answering chain"""
        if not self.vectorstore:
            st.error("Vector store not initialized")
            return
            
        try:
            # Initialize Azure OpenAI LLM
            llm = AzureChatOpenAI(
                openai_api_key=AzureConfig.OPENAI_API_KEY,
                openai_api_base=AzureConfig.OPENAI_ENDPOINT,
                openai_api_version=AzureConfig.OPENAI_API_VERSION,
                deployment_name=AzureConfig.OPENAI_DEPLOYMENT,
                temperature=0.7
            )
            
            # Create retriever
            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": k}
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )
            
            st.success("QA chain setup complete")
            
        except Exception as e:
            st.error(f"Error setting up QA chain: {str(e)}")
            raise
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system"""
        if not self.qa_chain:
            return {
                "answer": "RAG system not initialized. Please upload documents first.",
                "source_documents": []
            }
        
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            return {
                "answer": f"Error querying RAG system: {str(e)}",
                "source_documents": []
            }
    
    def get_similar_documents(self, query: str, k: int = 3) -> List[Document]:
        """Get similar documents without full QA processing"""
        if not self.vectorstore:
            return []
        
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
        except Exception as e:
            st.error(f"Error retrieving similar documents: {str(e)}")
            return []
    
    def clear_knowledge_base(self):
        """Clear the knowledge base"""
        try:
            if os.path.exists(self.persist_directory):
                import shutil
                shutil.rmtree(self.persist_directory)
            self.vectorstore = None
            self.qa_chain = None
            st.success("Knowledge base cleared")
        except Exception as e:
            st.error(f"Error clearing knowledge base: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        if not self.vectorstore:
            return {"total_documents": 0, "status": "Not initialized"}
        
        try:
            # Get collection info
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                "total_documents": count,
                "status": "Ready",
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {
                "total_documents": 0,
                "status": f"Error: {str(e)}",
                "persist_directory": self.persist_directory
            }
