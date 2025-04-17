import os,pickle,sys
from utils.logger import logging
from utils.exceptions import CustomException

def save_reviews(filepath,reviews):
    """This function will sall the list of data into file."""
    logging.info("saving reviews...")
    try:
        path=os.path.dirname(filepath)
        os.makedirs(path,exist_ok=True)
        with open(filepath,"wb") as f:
            pickle.dump(reviews,f)

    except Exception as e:
        raise CustomException(e,sys)
    
def load_reviews(filepath):
    """This function will load the reviews saved in selected filepath.."""
    logging.info("Loading reviews started...")
    try:
        with open(filepath,"rb") as f:
            reviews=pickle.load(f)

        return reviews
    except Exception as e:
        raise CustomException(e,sys)
        