import pickle
import urllib 
from bs4 import BeautifulSoup, Comment
import csv
#from utils import *

#tfjs.converters.save_keras_model(model,"../")

def save_tokenizer():
    with open('scraper_tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_model(model_path):
    model.save(model_path)