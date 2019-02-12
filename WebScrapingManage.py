import requests
import json
from SnopesScraper import SnopesScraper
from TruthOrFictionScraper import TruthOrFictionScraper
from PolygraphScraper import PolygraphScraper
from PolitifactScraper import PolitifactScraper
from GossipCopScraper import GossipCopScraper
from FactScanScraper import FactScanScraper
from ClimateFeedbackScraper import ClimateFeedbackScraper
from AfricaCheckScraper import AfricaCheckScraper


class WebScrapingManage:
    def __init__(self):
        self.API_BASE_ENDPOINT = 'http://127.0.0.1:8000/' # defining the api-endpoint 'http://132.72.23.63:3004/'
        self.API_ADD_CLAIM_ENDPOINT = self.API_BASE_ENDPOINT + 'add_claim'
        self.API_SCRAPERS_IDS_ENDPOINT = self.API_BASE_ENDPOINT + 'users/get_scrapers'
        self.scrapers_dict = {'FactScan': FactScanScraper(), 'ClimateFeedback': ClimateFeedbackScraper(),
                              'Politifact': PolitifactScraper(), 'GossipCop': GossipCopScraper(),
                              'Snopes': SnopesScraper(), 'Polygraph': PolygraphScraper(), 'TruthOrFiction': TruthOrFictionScraper()}

    def extract_claims_from_scrapers(self, num_of_pages):
        print('start')
        client = requests.session()
        client.get(self.API_BASE_ENDPOINT)
        cookies = dict(client.cookies)
        csrf_token = client.cookies['csrftoken']
        headers = {'url': self.API_ADD_CLAIM_ENDPOINT, "X-CSRFToken": csrf_token}
        scrapers_ids = json.loads(client.get(self.API_SCRAPERS_IDS_ENDPOINT).content.decode('utf-8'))
        for scraper_name, scraper_class in self.scrapers_dict.items():
            claims_info_arr = scraper_class.extract_claims_info(num_of_pages)
            for claim_info in claims_info_arr:
                claim_info['user_id'] = scrapers_ids[scraper_name]
                # sending post request and saving response as response object
                print('Sending a claim from %s' % scraper_name)
                post_request = requests.post(url=self.API_ADD_CLAIM_ENDPOINT, data=claim_info, headers=headers, cookies=cookies)
                # scraper_class.update_claims_info_arr(claim_info)
            # scraper_class.clean_history()
            break
