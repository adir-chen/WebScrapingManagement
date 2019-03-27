from SnopesScraper import SnopesScraper
from TruthOrFictionScraper import TruthOrFictionScraper
from PolygraphScraper import PolygraphScraper
from PolitifactScraper import PolitifactScraper
from GossipCopScraper import GossipCopScraper
from FactScanScraper import FactScanScraper
from ClimateFeedbackScraper import ClimateFeedbackScraper
from AfricaCheckScraper import AfricaCheckScraper
from CnnAPI import CnnAPI
import requests
import smtplib
import json


class WebScrapingManage:
    def __init__(self):
        self.client = requests.session()
        self.API_BASE_ENDPOINT = 'http://127.0.0.1:8000/'  # defining the api-endpoint 'http://132.72.23.63:3004/'
        self.API_ADD_CLAIM_ENDPOINT = self.API_BASE_ENDPOINT + 'add_claim'
        self.API_SCRAPERS_IDS_ENDPOINT = self.API_BASE_ENDPOINT + 'users/get_all_scrapers_ids'
        self.API_RANDOM_CLAIMS_ENDPOINT = self.API_BASE_ENDPOINT + 'users/get_random_claims_from_scrapers'
        self.scrapers_dict = {'CNN': CnnAPI(), 'AfricaCheck': AfricaCheckScraper(), 'FactScan': FactScanScraper(), 'ClimateFeedback': ClimateFeedbackScraper(),
                              'GossipCop': GossipCopScraper(), 'Politifact': PolitifactScraper(),
                              'TruthOrFiction': TruthOrFictionScraper(), 'Polygraph': PolygraphScraper(), 'Snopes': SnopesScraper()}
        self.scrapers_passwords = {'CNN': 'fbYmYExduj', 'AfricaCheck': 'HcrXqG8M6w', 'FactScan': 'GqFhx5bgqt',
                                   'ClimateFeedback': 'fCLtCtpCub', 'GossipCop': 'a5gq5eR7Kb', 'Politifact': 'Mnwnd3dbfP',
                                   'TruthOrFiction': '7uDMzAWjJ7', 'Polygraph': 'eaQt93uMrn', 'Snopes': 'd2GTfFfD6D'}
        self.email = 'wtfactnews@gmail.com'
        self.email_pass = 'amc8dGig'

    def extract_claims_from_scrapers(self, num_of_pages):
        print('start')
        try:
            self.client.get(self.API_BASE_ENDPOINT)
            cookies = dict(self.client.cookies)
            csrf_token = self.client.cookies['csrftoken']
            headers = {'url': self.API_ADD_CLAIM_ENDPOINT, "X-CSRFToken": csrf_token}
            scrapers_ids = json.loads(self.client.get(self.API_SCRAPERS_IDS_ENDPOINT).content.decode('utf-8'))
            # for the first time to send scrapers' claims
            all_scrapers_claims = []
            for scraper_name, scraper_class in self.scrapers_dict.items():
                print(scraper_name)
                try:
                    claims_info_arr = scraper_class.extract_claims_info(num_of_pages)
                    for claim_info in claims_info_arr:
                        claim_info['user_id'] = scrapers_ids[scraper_name]
                        claim_info['password'] = self.scrapers_passwords[scraper_name]
                        claim_info['add_comment'] = 'true'
                        # sending post request and saving response as response object
                        # print('Sending a claim from %s' % scraper_name)
                        # for the first time to send scrapers' claims
                        all_scrapers_claims.append(claim_info)
                        # post_request = requests.post(url=self.API_ADD_CLAIM_ENDPOINT, data=claim_info, headers=headers,
                        #                              cookies=cookies)
                        # scraper_class.update_claims_info_arr(claim_info)
                except Exception as e:
                    print('Error in scraper ' + scraper_name + ': can\'t import new claims')
                    err_msg = "\nError in scraper " + str(scraper_name) + ": can\'t import new claims"
                    self.send_mail(err_msg)
                    continue
            # for the first time to send scrapers' claims
            from datetime import datetime
            all_scrapers_claims_sorted_by_verdict_date = sorted(all_scrapers_claims,
                                                                key=lambda k:
                                                                datetime.strptime(k['verdict_date'], '%d/%m/%Y'))
            for claim_info in all_scrapers_claims_sorted_by_verdict_date:
                requests.post(url=self.API_ADD_CLAIM_ENDPOINT, data=claim_info, headers=headers,
                              cookies=cookies)
        except Exception as e:
            print('Connection error')
            err_msg = "\nConnection error : server does not run"
            self.send_mail(err_msg)

    def send_mail(self, err_msg):
        message = 'Subject: {}\n\n{}'.format("Error in WSM", err_msg)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.email_pass)
        server.sendmail(self.email,
                        self.email,
                        message)

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
                        break
                if not found:
                    print('Error in scraper ' + scraper_name + ': wrong url')
                    continue

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