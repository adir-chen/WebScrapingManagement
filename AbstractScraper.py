from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string


class AbstractScraper(ABC):

    def __init__(self):
        self.claims_history = []

    def open_fact_check_page(self, url):
        request = Request(url, headers={'User-Agent': 'Chclean_site_tagsrome/70.0.3538.102'})
        return BeautifulSoup(urlopen(request), "html.parser")

    @abstractmethod
    def extract_claims_info(self, num_of_pages):
        pass

    def clean_site_tags(self, site_tags):
        new_tags = []
        for tag in site_tags:
            new_tag = ''
            for char in tag:
                if char.isalpha() or char.isdigit() or char.isspace():
                    new_tag += char
            if new_tag != '':
                new_tags.append(new_tag)
        return ','.join(new_tags)

    def get_optional_tags(self, current_tags, claim_tags):
        optional_tags = []
        for tag in claim_tags:
            if tag.lower() not in current_tags.lower():
                optional_tags.append(tag)
        if current_tags:
            current_tags += ','
        return current_tags + ','.join(optional_tags)

    def extract_tags(self, claim):
        filtered_sentence = []
        tags = []
        # claim = claim.lower()
        stop_words = set(stopwords.words('english'))
        not_allowed_input = set(string.punctuation)
        for w in word_tokenize(claim):
            if w not in stop_words and all(c not in w for c in not_allowed_input) and len(w) != 1:
                filtered_sentence.append(w)
        lemmatizer = WordNetLemmatizer()
        filtered_sentence = nltk.pos_tag(filtered_sentence)
        for word_and_pos_tag in filtered_sentence:
            if word_and_pos_tag[1].startswith('NN'):
                word_lemmatize = lemmatizer.lemmatize(word_and_pos_tag[0])
                if not any(word_lemmatize.lower() in tag.lower() for tag in tags):
                    tags.append(word_lemmatize)
        return tags

    def replace_suffix_in_date(self, date):
        all_suffix = ["th", "rd", "nd", "st"]
        for suffix in all_suffix:
            date = date.replace(suffix, '')
        return date

    # def check_if_claim_exists(self, url):
    #     for claim_info in self.claims_history:
    #         if claim_info['url'] == url:
    #             return True
    #     return False

    # def update_claims_info_arr(self, claims_info):
    #     self.claims_history.append(claims_info)

    # def clean_history(self):
    #     date_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    #     delete_history = []
    #     for claim_info in self.claims_history:
    #         if datetime.datetime.strptime(claim_info['verdict_date'],'%d/%m/%Y') < date_week_ago:
    #             delete_history.append(claim_info)
    #     self.claims_history = [claim for claim in self.claims_history if claim not in delete_history]
