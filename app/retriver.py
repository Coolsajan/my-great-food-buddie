import re
import os
import sys
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.base import VectorStoreRetriever
from utils.exceptions import CustomException
from utils.logger import logging

def load_retriver(foodPlace: str, persist_dir: str = "data/vector_store") -> VectorStoreRetriever:
    """
    Load ChromaDB vector store and return langchain retriever.
    """
    try:
        logging.info("Data retriever started..")

        safe_foodPlace = re.sub(r"[^\w.-]", "_", foodPlace)
        chroma_path = os.path.join(persist_dir, safe_foodPlace)
        
        if not os.path.exists(chroma_path):
            raise ValueError(f"No vector store found at {chroma_path}")
        
        embedding = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2'
        )

       
        vectorDB = Chroma(
            persist_directory=chroma_path,
            embedding_function=embedding,
            collection_name=safe_foodPlace  
        )

        retriever = vectorDB.as_retriever(
            search_type="similarity",
            search_kwargs={'k': 3}
        )

        return retriever
    
    except Exception as e:
        raise CustomException(e, sys)