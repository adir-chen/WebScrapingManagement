from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import datetime


class AbstractScraper(ABC):

    def __init__(self):
        self.claims_history = []

    def open_fact_check_page(self, url):
        request = Request(url, headers={'User-Agent': 'Chrome/70.0.3538.102'})
        return BeautifulSoup(urlopen(request), "html.parser")

    @abstractmethod
    def extract_claims_info(self):
        pass

    def extract_tags(self, claim):
        filtered_sentence = []
        tags = []
        # claim = claim.lower()
        stop_words = set(stopwords.words('english'))
        for w in word_tokenize(claim):
            if w not in stop_words and w not in string.punctuation and '\'' not in w:
                filtered_sentence.append(w)
        lemmatizer = WordNetLemmatizer()
        filtered_sentence = nltk.pos_tag(filtered_sentence)
        for word_and_pos_tag in filtered_sentence:
            if word_and_pos_tag[1].startswith('NN'):
                tags.append(lemmatizer.lemmatize(word_and_pos_tag[0]))
        return tags

    def check_if_claim_exists(self, url):
        for claim_info in self.claims_history:
            if claim_info['url'] == url:
                return True
        return False

    def update_claims_info_arr(self, claims_info):
        self.claims_history.append(claims_info)

    def clean_history(self):
        date_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        delete_history = []
        for claim_info in self.claims_history:
            if datetime.datetime.strptime(claim_info['verdict_date'],'%d/%m/%Y') < date_week_ago:
                delete_history.append(claim_info)
        self.claims_history = [claim for claim in self.claims_history if claim not in delete_history]
