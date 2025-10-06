#!/usr/bin/env python3
"""
Test script for RAG system functionality
"""

from rag_system_windows import RAGSystem
import os

def test_rag_system():
    """Test the RAG system with sample knowledge"""
    print("Testing RAG System...")
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Test with sample knowledge file
    if os.path.exists("sample_knowledge.txt"):
        print("Loading sample knowledge...")
        
        # Load and process documents
        documents = rag.load_documents(["sample_knowledge.txt"])
        processed_docs = rag.process_documents(documents)
        
        # Create vector store
        rag.create_vectorstore(processed_docs, force_recreate=True)
        
        # Setup QA chain
        rag.setup_qa_chain()
        
        # Test queries
        test_queries = [
            "What is the company name?",
            "What are the pricing plans?",
            "How can I contact support?",
            "What is the response time?",
            "What languages are supported?"
        ]
        
        print("\nTesting queries:")
        for query in test_queries:
            print(f"\nQuery: {query}")
            result = rag.query(query)
            print(f"Answer: {result['answer']}")
            
        # Get stats
        stats = rag.get_stats()
        print(f"\nKnowledge Base Stats: {stats}")
        
    else:
        print("Sample knowledge file not found!")

if __name__ == "__main__":
    test_rag_system()
