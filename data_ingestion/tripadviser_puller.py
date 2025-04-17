from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from dotenv import load_dotenv
from pathlib import Path
import time,random
import sys,os
import requests

from utils.exceptions import CustomException
from utils.logger import logging
from utils.common_utils import save_reviews
from dataclasses import dataclass

load_dotenv(dotenv_path=".env")
RAPID_API_KEY=os.getenv("RAPID_API_KEY")

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

            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            options.add_argument("--headless")

            logging.info("Webdriver option setting sucessfull..")
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.tripadvisor.com/")

            search_box=WebDriverWait(driver=driver,timeout=15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[type='search'][placeholder*='Places to go']"))
                )
            logging.info("Search box found...")
            
            search_box.send_keys(self.foodPlace)
            time.sleep(random.uniform(2, 4))
            search_box.send_keys(Keys.ENTER)
            logging.info(f"{self.foodPlace} entered into search box.")

            first_result_card = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-attribute='location-results-card'] a"))
                )
            
            review_link=first_result_card.get_attribute("href")
            logging.info("TripAdviser link obtained sucessfully..")

            driver.quit()
            logging.info("Driver closed...")

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





        