#!/usr/bin/env python3
"""
Simple RAG system without embeddings - uses direct text matching
"""

import os
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import streamlit as st

from config import AzureConfig
from langchain_openai import AzureChatOpenAI
from langchain.schema import Document

# Custom document loaders to avoid Windows compatibility issues
import PyPDF2
from docx import Document as DocxDocument

class SimpleRAGSystem:
    """Simple RAG system using text matching instead of embeddings"""
    
    def __init__(self):
        self.documents = []
        self.llm = None
        self.qa_chain = None
        
    def load_text_file(self, file_path: str) -> List[Document]:
        """Load text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [Document(page_content=content, metadata={"source": file_path})]
        except Exception as e:
            st.error(f"Error loading text file {file_path}: {str(e)}")
            return []
    
    def load_pdf_file(self, file_path: str) -> List[Document]:
        """Load PDF file"""
        try:
            documents = []
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(pdf_reader.pages):
                    content = page.extract_text()
                    if content.strip():
                        documents.append(Document(
                            page_content=content,
                            metadata={"source": file_path, "page": page_num}
                        ))
            return documents
        except Exception as e:
            st.error(f"Error loading PDF file {file_path}: {str(e)}")
            return []
    
    def load_docx_file(self, file_path: str) -> List[Document]:
        """Load DOCX file"""
        try:
            doc = DocxDocument(file_path)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return [Document(page_content=content, metadata={"source": file_path})]
        except Exception as e:
            st.error(f"Error loading DOCX file {file_path}: {str(e)}")
            return []
    
    def load_documents(self, file_paths: List[str]) -> List[Document]:
        """Load documents from various file types"""
        documents = []
        
        for file_path in file_paths:
            file_extension = Path(file_path).suffix.lower()
            
            try:
                if file_extension == '.txt':
                    docs = self.load_text_file(file_path)
                elif file_extension == '.pdf':
                    docs = self.load_pdf_file(file_path)
                elif file_extension in ['.docx', '.doc']:
                    docs = self.load_docx_file(file_path)
                else:
                    st.warning(f"Unsupported file type: {file_extension}")
                    continue
                    
                documents.extend(docs)
                st.success(f"Loaded {len(docs)} documents from {file_path}")
                
            except Exception as e:
                st.error(f"Error loading {file_path}: {str(e)}")
                
        return documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Process documents by splitting into chunks"""
        if not documents:
            return []
            
        # Simple text splitting
        processed_docs = []
        for doc in documents:
            # Split by paragraphs
            paragraphs = doc.page_content.split('\n\n')
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    processed_docs.append(Document(
                        page_content=paragraph.strip(),
                        metadata={**doc.metadata, "chunk": i}
                    ))
        
        st.info(f"Split documents into {len(processed_docs)} chunks")
        return processed_docs
    
    def create_knowledge_base(self, documents: List[Document]):
        """Create knowledge base from documents"""
        if not documents:
            st.warning("No documents to process")
            return
            
        self.documents = documents
        st.success(f"Created knowledge base with {len(documents)} document chunks")
        
        # Initialize LLM
        try:
            self.llm = AzureChatOpenAI(
                openai_api_key=AzureConfig.OPENAI_API_KEY,
                azure_endpoint=AzureConfig.OPENAI_ENDPOINT,
                openai_api_version=AzureConfig.OPENAI_API_VERSION,
                deployment_name=AzureConfig.OPENAI_DEPLOYMENT,
                temperature=0.7
            )
            st.success("LLM initialized successfully")
        except Exception as e:
            st.error(f"Error initializing LLM: {str(e)}")
            raise
    
    def find_relevant_documents(self, query: str, k: int = 3) -> List[Document]:
        """Find relevant documents using simple text matching"""
        if not self.documents:
            return []
        
        # Simple keyword matching
        query_words = set(re.findall(r'\w+', query.lower()))
        
        scored_docs = []
        for doc in self.documents:
            content_words = set(re.findall(r'\w+', doc.page_content.lower()))
            # Calculate simple overlap score
            overlap = len(query_words.intersection(content_words))
            if overlap > 0:
                scored_docs.append((overlap, doc))
        
        # Sort by score and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:k]]
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system"""
        if not self.llm or not self.documents:
            return {
                "answer": "RAG system not initialized. Please upload documents first.",
                "source_documents": []
            }
        
        try:
            # Find relevant documents
            relevant_docs = self.find_relevant_documents(question, k=3)
            
            if not relevant_docs:
                return {
                    "answer": "No relevant information found in the knowledge base.",
                    "source_documents": []
                }
            
            # Create context from relevant documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Create prompt
            prompt = f"""Based on the following information from the knowledge base, answer the question.

Knowledge Base Information:
{context}

Question: {question}

Please provide a helpful and accurate answer based on the information above. If the information doesn't directly answer the question, say so and provide what information is available."""

            # Get response from LLM
            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "answer": answer,
                "source_documents": relevant_docs
            }
            
        except Exception as e:
            return {
                "answer": f"Error querying RAG system: {str(e)}",
                "source_documents": []
            }
    
    def clear_knowledge_base(self):
        """Clear the knowledge base"""
        self.documents = []
        self.llm = None
        st.success("Knowledge base cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        if not self.documents:
            return {"total_documents": 0, "status": "Not initialized"}
        
        return {
            "total_documents": len(self.documents),
            "status": "Ready"
        }
