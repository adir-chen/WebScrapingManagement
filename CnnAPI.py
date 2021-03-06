from AbstractScraper import AbstractScraper
from datetime import datetime
import requests
import json


class CnnAPI(AbstractScraper):

    def __init__(self, api_name='CNN', api_url='https://newsapi.org/v2/top-headlines?sources=cnn&'):
        self.api_name = api_name
        self.api_url = api_url
        with open('/home/wtfact/Documents/Keys and Settings/cnn_api_key.json') as cnn_api_key_file:
            cnn_api_key = json.load(cnn_api_key_file)
        self.api_key = cnn_api_key['API_KEY']
        self.request = (self.api_url + 'apiKey=' + self.api_key)
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        response = requests.get(self.request)
        response = response.json()

        news_info_arr = []
        for article in response['articles']:
            # title
            title = article['title']

            # url
            url = article['url']

            # description
            description = article['description']

            # verdict date
            verdict_datetime = datetime.strptime(article['publishedAt'][:10], "%Y-%m-%d").date()
            verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

            # category
            category = 'News'

            # tags
            tags = ','.join(super().extract_tags(title))

            # img_src
            img_src = article['urlToImage']

            claim_info_dict = {'username': self.api_name,
                               'title': title,
                               'claim': title,
                               'description': description,
                               'url': url,
                               'verdict_date': verdict_date,
                               'tags': tags,
                               'category': category,
                               'label': 'True',
                               'image_src': img_src}
            news_info_arr.append(claim_info_dict)
        return news_info_arr
