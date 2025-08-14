"""
RAG (Retrieval Augmented Generation) system management
"""
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import (
    FAISS_DB_PATH, EMBEDDING_MODEL, EMBEDDING_DEVICE, 
    SIMILARITY_SEARCH_K, CHUNK_SIZE, CHUNK_OVERLAP
)
import document_processor as dp

class RAGSystem:
    """Manages RAG components including vectorstore and embeddings"""
    
    def __init__(self):
        self.vectorstore = None
        self.embeddings = None
        
    def get_embeddings(self):
        """Get or create embeddings model"""
        if self.embeddings is None:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': EMBEDDING_DEVICE}
            )
        return self.embeddings
    
    def setup_vectorstore(self, docs_folder: str):
        """Initialize RAG with a user-specified folder"""
        print(f"\n[RAG_SETUP] Initializing RAG with folder: {docs_folder}")

        if not os.path.exists(docs_folder):
            print(f"[RAG_SETUP] Error: Document folder does not exist: {docs_folder}")
            return None
            
        if self.vectorstore is None:
            print("[RAG_SETUP] No existing vectorstore found. Creating a new one.")
            embeddings = self.get_embeddings()
            
            # Check if FAISS vectorstore already exists on disk
            if os.path.exists(FAISS_DB_PATH):
                print(f"[RAG_SETUP] Loading existing FAISS vectorstore from {FAISS_DB_PATH}")
                try:
                    self.vectorstore = FAISS.load_local(
                        FAISS_DB_PATH, 
                        embeddings, 
                        allow_dangerous_deserialization=True
                    )
                    print("[RAG_SETUP] Successfully loaded existing vectorstore.")
                    return self.vectorstore
                except Exception as e:
                    print(f"[RAG_SETUP] Error loading existing vectorstore: {e}. Creating new one.")
            
            print(f"[RAG_SETUP] Processing documents from: {docs_folder}")
            documents = dp.process_health_documents(docs_folder, is_directory=True)
            print(f"[RAG_SETUP] Document processing complete. Found {len(documents)} documents.")
            
            if not documents:
                print("[RAG_SETUP] Warning: No documents found or processed.")
                return None

            chunked_docs = dp.chunk_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
            print(f"[RAG_SETUP] Chunked documents into {len(chunked_docs)} chunks.")

            print("[RAG_SETUP] Creating FAISS vectorstore instance.")
            self.vectorstore = FAISS.from_documents(
                documents=chunked_docs,
                embedding=embeddings
            )
            print(f"[RAG_SETUP] Added {len(chunked_docs)} chunks to the vectorstore.")
            # Save the vectorstore to disk for persistence
            self.vectorstore.save_local(FAISS_DB_PATH)
            print("[RAG_SETUP] Documents successfully added to the vectorstore.")
        else:
            print("[RAG_SETUP] Using existing vectorstore.")
        
        return self.vectorstore
    
    def similarity_search(self, query: str, k: int = None):
        """Perform similarity search on the vectorstore"""
        if self.vectorstore is None:
            print("[RAG_SYSTEM] Warning: Vectorstore not initialized")
            return []
        
        k = k or SIMILARITY_SEARCH_K
        try:
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            print(f"[RAG_SYSTEM] Error during similarity search: {e}")
            return []
    
    def reset_vectorstore(self):
        """Reset the vectorstore"""
        self.vectorstore = None

# Global RAG system instance
rag_system = RAGSystem()
