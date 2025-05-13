from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from dotenv import load_dotenv
from pathlib import Path
import sys,os
import requests
from serpapi import search

from utils.exceptions import CustomException
from utils.logger import logging
from utils.common_utils import save_reviews
from dataclasses import dataclass

load_dotenv(dotenv_path=".env")
RAPID_API_KEY=os.getenv("RAPID_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

@dataclass
class TripAdviserDataPullConfig:
    review_save_file_path : str = os.path.join("data","raw")


class TripAdviserDataPull:
    """
    Pulls the data of selected resturant,cafe.

    This instance will pull the review of selected cafe,resturant from website of tripadviser.
    """

    def __init__(self,foodPlace : str,review_save_file_path : str = TripAdviserDataPullConfig().review_save_file_path):
        """
        Initializes the ClassName instance.

        Args:
        foodPlace (str) : This is the name of the cafe,resturant you searched.
        review_save_file_path (str) : This is a path to save the pulled data.
        """
        self.foodPlace = foodPlace
        self.review_save_file_path = review_save_file_path

    
    def get_tripadviser_link(self) -> str:
        """
        This method will retrun the link for foodPlace link on tripadviser.
        """
        try:
            logging.info("Entered inot  TripAdviserDataPull... ")

            params = {"engine": "google",
                       "q": "white rabbit pokhara",
                        "api_key": SERPAPI_KEY}
            
            response = search(params=params)

            for data in response['organic_results']:
                if "tripadvisor.com" in data["link"]:
                    review_link = data['link']
                    break

            return review_link

        except Exception as e:
            raise CustomException(e,sys)
        
    def get_reviews(self,review_link) -> list:
        """
        This metod will use rapidapi and fetch all the review for foodPlace on tripadviser..        
        """
        try:
            global reviews
            reviews =[]

            url = "https://real-time-tripadvisor-scraper-api.p.rapidapi.com/tripadvisor_restaurants_reviews_v2"

            querystring = {"restaurant":review_link}

            headers = {
                "x-rapidapi-key": RAPID_API_KEY,
                "x-rapidapi-host": "real-time-tripadvisor-scraper-api.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            logging.info("Review captured in buled json...")

            print(response)
            data_list=list(response.json()["data"])

            for data in data_list:
                text = data.get("text")
                title = data.get("title")
                result = title + text

                reviews.append(result)

            logging.info("All review collected..")
            return reviews

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_tripadviser_data_pull(self)  -> str:
        """
        This will iniate the all TripAdviserDataPull class..
        """
        try:
            logging.info("Entering into initiate_tripadviser_data_pull.")
            review_link=self.get_tripadviser_link()
            reviews=self.get_reviews(review_link=review_link)

            filepath=os.path.join(self.review_save_file_path,self.foodPlace,"tripadviser.pkl")
            save_reviews(filepath=filepath,reviews=reviews)

            logging.info("Review pulling from TripAdviserDataPull ended sucessfull..")

            return filepath

        except Exception as e:
            raise CustomException(e,sys)




        