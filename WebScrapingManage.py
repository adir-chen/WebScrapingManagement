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
        self.client = requests.session()
        self.API_BASE_ENDPOINT = 'http://127.0.0.1:8000/' # defining the api-endpoint 'http://132.72.23.63:3004/'
        self.API_ADD_CLAIM_ENDPOINT = self.API_BASE_ENDPOINT + 'add_claim'
        self.API_SCRAPERS_IDS_ENDPOINT = self.API_BASE_ENDPOINT + 'users/get_scrapers'
        self.API_RANDOM_CLAIMS_ENDPOINT = self.API_BASE_ENDPOINT + 'users/get_random_claims_from_scrapers'
        self.scrapers_dict = {'AfricaCheck': AfricaCheckScraper(), 'FactScan': FactScanScraper(), 'ClimateFeedback': ClimateFeedbackScraper(),
                              'Politifact': PolitifactScraper(), 'GossipCop': GossipCopScraper(),
                              'Snopes': SnopesScraper(), 'Polygraph': PolygraphScraper(), 'TruthOrFiction': TruthOrFictionScraper()}

    def extract_claims_from_scrapers(self, num_of_pages):
        print('start')
        self.client.get(self.API_BASE_ENDPOINT)
        cookies = dict(self.client.cookies)
        csrf_token = self.client.cookies['csrftoken']
        headers = {'url': self.API_ADD_CLAIM_ENDPOINT, "X-CSRFToken": csrf_token}
        scrapers_ids = json.loads(self.client.get(self.API_SCRAPERS_IDS_ENDPOINT).content.decode('utf-8'))
        for scraper_name, scraper_class in self.scrapers_dict.items():
            try:
                claims_info_arr = scraper_class.extract_claims_info(num_of_pages)
                for claim_info in claims_info_arr:
                    claim_info['user_id'] = scrapers_ids[scraper_name]
                    # sending post request and saving response as response object
                    print('Sending a claim from %s' % scraper_name)
                    post_request = requests.post(url=self.API_ADD_CLAIM_ENDPOINT, data=claim_info, headers=headers,
                                                 cookies=cookies)
                    # scraper_class.update_claims_info_arr(claim_info)
            except Exception as e:
                print('Error in scraper ' + scraper_name + ': can\'t import new claims')
            # scraper_class.clean_history()
                break

    def validate_scrapers(self, num_of_pages):
        no_errors = True
        random_claims = json.loads(self.client.get(self.API_RANDOM_CLAIMS_ENDPOINT).content.decode('utf-8'))
        for scraper_name, random_claim in random_claims.items():
            try:
                all_claims = self.scrapers_dict[scraper_name].extract_claims_info(num_of_pages)
            except Exception as e:
                print('Error in scraper ' + scraper_name + ': can\'t import new claims')
                return False
            else:
                found = False
                for claim in all_claims:
                    if not found and claim['url'] == random_claim['url']:
                        found = True
                        found_claim = claim
                if not found:
                    print('Error in scraper ' + scraper_name + ': wrong url')

                if not found_claim['title'] == random_claim['title']:
                    print('Error in scraper ' + scraper_name + ': wrong title')
                    print('Expected: ' + found_claim['title'] + '. Actual: ' + random_claim['title'])
                    no_errors = False
                if not found_claim['claim'] == random_claim['claim']:
                    print('Error in scraper ' + scraper_name + ': wrong claim')
                    print('Expected: ' + found_claim['claim'] + '. Actual: ' + random_claim['claim'])
                    no_errors = False
                if not found_claim['description'] == random_claim['description']:
                    print('Error in scraper ' + scraper_name + ': wrong description')
                    print('Expected: ' + found_claim['description'] + '. Actual: ' + random_claim['description'])
                    no_errors = False
                if not found_claim['verdict_date'] == random_claim['verdict_date']:
                    print('Error in scraper ' + scraper_name + ': wrong verdict_date')
                    print('Expected: ' + found_claim['verdict_date'] + '. Actual: ' + random_claim['verdict_date'])
                    no_errors = False
                if not found_claim['category'] == random_claim['category']:
                    print('Error in scraper ' + scraper_name + ': wrong category')
                    print('Expected: ' + found_claim['category'] + '. Actual: ' + random_claim['category'])
                    no_errors = False
                if not found_claim['label'] == random_claim['label']:
                    print('Error in scraper ' + scraper_name + ': wrong label')
                    print('Expected: ' + found_claim['label'] + '. Actual: ' + random_claim['label'])
                    no_errors = False
        return no_errors
    def extract_claims_from_scrapers_and_validate(self):
        NotImplemented()
