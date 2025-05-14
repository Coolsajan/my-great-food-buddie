from utils.logger import logging
from utils.exceptions import CustomException
from utils.common_utils import load_reviews
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb import PersistentClient
from chromadb.config import Settings
import re
import os,sys
from dataclasses import dataclass


@dataclass
class CleanAndSaveToChromaDBConfig:
    chromedb_save_filepath : str = os.path.join("data","vector_store")

class CleanAndSaveToChromaDBC:
    """
    This will collect , clean and save revies.

    This path will collect the review scraped from ingestion clean and save to vector DB(ChromaDB).
    """

    def __init__(self):
        pass

    def get_data(self,filepath :list): 
        """This method will collect the data from ingestion artifaact.."""
        try:
            logging.info("Starting get_data method from CleanAndSaveToChromeDBC class.. ")

            first_review=load_reviews(filepath=filepath[0])
            second_review=load_reviews(filepath=filepath[-1])

            full_reviews = first_review + second_review

            logging.info("Exisiting get_data")
            return full_reviews
        
        except Exception as e:
            raise CustomException(e,sys)

    def clean_reviews(self, full_review: list):
        """Clean and chunk scraped reviews using LangChain's text splitter."""
        try:
            logging.info("Entering clean_reviews...")

            cleaned_reviews = []
            for review in full_review:
                review = review.lower()
                review = re.sub(r"[^a-zA-Z0-9\s]", "", review)
                review = re.sub(r"\s+", " ", review).strip()
                cleaned_reviews.append(review)

            # Use LangChain's RecursiveCharacterTextSplitter
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,          # max characters per chunk
                chunk_overlap=50,        # optional overlap
                separators=["\n\n", "\n", ".", " ", ""],  # split preference
            )

            split_docs = splitter.create_documents(cleaned_reviews)

            # Extract text content only
            chunked_texts = [doc.page_content for doc in split_docs]

            logging.info(f"Split into {len(chunked_texts)} chunks using LangChain splitter.")
            return chunked_texts

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_clean_chromadb(self,foodPlace : str, filepath : list):
        """
        This will initiate the clean store chromadb.
        """
        try:
            logging.info("Initiaiting the clean and get db...")
            full_reviews=self.get_data(filepath=filepath)
            logging.info(f"{len(full_reviews)} revies obtained..")
            cleaned_reviews=self.clean_reviews(full_review=full_reviews)
            logging.info("Cleanned the reviews..")

            model = SentenceTransformer("all-MiniLM-L6-v2")
            vectors = model.encode(cleaned_reviews)
            logging.info("Reviews converted into vectors....")

            safe_foodPlace = re.sub(r"[^\w.-]", "_", foodPlace)
            path=os.path.join(CleanAndSaveToChromaDBConfig().chromedb_save_filepath,safe_foodPlace)
            os.makedirs(path,exist_ok=True)
            
            client = PersistentClient(path=path)
            collection = client.get_or_create_collection(name=safe_foodPlace)
            collection.add(documents=cleaned_reviews, embeddings=vectors, ids=[f"id-{i}" for i in range(len(cleaned_reviews))])

        except Exception as e:
            raise CustomException(e,sys)

 