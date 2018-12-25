import requests
from SnopesScraper import SnopesScraper
from TruthOrFictionScraper import TruthOrFictionScraper
from PolygraphScraper import PolygraphScraper


class WebScrapingManage:
    def __init__(self):
        self.API_ENDPOINT = 'http://192.168.1.22:80/add_claim'  # defining the api-endpoint 'http://127.0.0.1:8000/claims/add_claim'
        self.scrapers_dict = {'Snopes': SnopesScraper(), 'TruthOrFiction': TruthOrFictionScraper(), 'Polygraph': PolygraphScraper()}

    def extract_claims_from_scrapers(self, num_of_pages):
        print('start')
        for scraper_name, scraper_class in self.scrapers_dict.items():
            claims_info_arr = scraper_class.extract_claims_info(num_of_pages)
            for claim_info in claims_info_arr:
                # sending post request and saving response as response object
                print('sending')
                r = requests.post(url=self.API_ENDPOINT, data=claim_info, headers=dict(Referer=self.API_ENDPOINT))
                print(r.text)
                # scraper_class.update_claims_info_arr(claim_info)
            # scraper_class.clean_history()
