from dotenv import load_dotenv
import sys,os
import requests

from utils.exceptions import CustomException
from utils.logger import logging
from utils.common_utils import save_reviews
from dataclasses import dataclass

load_dotenv(dotenv_path=".env")
RAPID_API_KEY=os.getenv("RAPID_API_KEY")


@dataclass
class GoogleMapsDataPullConfig:
    review_save_file_path : str = os.path.join("/tmp/data","raw")


class GoogleMapsDataPull:
    """
    This class will pull all the reviews from google maps.

    This class uses the rapid api and pull the data from the google maps. 
    """

    def __init__(self,foodPlace:str, review_save_file_path :str =GoogleMapsDataPullConfig().review_save_file_path,):
        """
        Initializes the ClassName instance.

        Args:
        foodPlace (str) : This is the name of the cafe,resturant you searched.
        review_save_file_path (str) : This is a path to save the pulled data.
        """
        self.foodPlace = foodPlace
        self.review_save_file_path = review_save_file_path

    def get_business_id(self) -> str:
        """
        This method will get the business id for the foodPlace using api from rapidapi.
        """
        try:
            logging.info("Entering into GoogleMapsDataPull...")
            url = "https://local-business-data.p.rapidapi.com/search"

            querystring = {"query":self.foodPlace,"limit":"35","lat":"37.359428","lng":"-121.925337","zoom":"13","language":"en","region":"us","extract_emails_and_contacts":"false"}

            headers = {
                "x-rapidapi-key": RAPID_API_KEY,
                "x-rapidapi-host": "local-business-data.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            logging.info(f"Responsed grerated for {self.foodPlace} ...")

            business_id=response.json()['parameters'][0].get("business_id")
            logging.info("Business id collection...")

            return business_id

        except Exception as e:
            raise CustomException(e,sys)
        
    def get_review_from_business_id(self,business_id:str) -> list:
        """
        This method will gather reviews from google map using rapid api and business_id.
        """
        try:
            logging.info(f"Starting the review pull from rapid api using {self.foodPlace}:{business_id}")
            url = "https://local-business-data.p.rapidapi.com/business-reviews"

            querystring = {"business_id":business_id,"limit":"5000","sort_by":"most_relevant","region":"us","language":"en"}

            headers = {
                "x-rapidapi-key": RAPID_API_KEY,
                "x-rapidapi-host": "local-business-data.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            logging.info(f"Responsed generated for {self.foodPlace} ...")
            print(response.json())
            data_list=list(response.json()['data'])
            logging.info(f"Data list obtained with {len(data_list)} datas.")
            reviews=[]

            for data in data_list:
                data=dict(data)
                review=data.get("review_text")

                reviews.append(review)

            
            logging.info(f"Collected {len(reviews)}.")
            return reviews

        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_google_maps_data_pull(self) -> str:
        """
        This method will inititate the GoogleMapsDataPull class.
        """
        try:
            logging.info("Start initiate_google_maps_data_pull method .")
            business_id = self.get_business_id()
            reviews = self.get_review_from_business_id(business_id=business_id)

            path=os.path.join(self.review_save_file_path,self.foodPlace,"google_maps.pkl")

            save_reviews(filepath=path,reviews=reviews)
            logging.info(f"Reviews for {self.foodPlace} collected from googlemaps and saved to {path}")
            return path
        except Exception as e:
            raise CustomException(e,sys)