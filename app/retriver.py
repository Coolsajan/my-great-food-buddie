import re ,os,sys
from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.base import VectorStoreRetriever
from utils.exceptions import CustomException
from utils.logger import logging


def load_retriver(foodPlace:str,presist_dir: str = "data/vector_store") -> VectorStoreRetriever:
    """
    load ChromaDB vectore store and retrun langchain retriver.
    """
    try:
        logging.info("Data retriver started..")
        safe_foodPlace = re.sub(r"[^\w.-]", "_", foodPlace)

        chroma_path=os.path.join(presist_dir,safe_foodPlace)
        print(chroma_path)

        if not os.path.join(chroma_path):
            raise ValueError(f"no vectore store found at {chroma_path}")
        
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        vectoreDB=Chroma(
            collection_name=safe_foodPlace,
            persist_directory=chroma_path,
            embedding_function=embedding
        )

        retriver=vectoreDB.as_retriever(
            search_type="similarity",
            search_kwargs ={'k':3}
        )

        return retriver
    
    except Exception as e:
        raise CustomException(e,sys)
    
