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
import csv
import json


class WebScrapingManage:
    def __init__(self):
        self.client = requests.session()
        self.API_BASE_ENDPOINT = 'https://wtfact.ise.bgu.ac.il/'
        self.API_ADD_CLAIM_ENDPOINT = self.API_BASE_ENDPOINT + 'add_claim'
        self.API_SCRAPERS_IDS_ENDPOINT = self.API_BASE_ENDPOINT + 'users/get_all_scrapers_ids'
        self.API_RANDOM_CLAIMS_ENDPOINT = self.API_BASE_ENDPOINT + 'users/get_random_claims_from_scrapers'
        self.scrapers_dict = {'AfricaCheck': AfricaCheckScraper(),
                              'FactScan': FactScanScraper(),
                              'ClimateFeedback': ClimateFeedbackScraper(),
                              'GossipCop': GossipCopScraper(),
                              'Politifact': PolitifactScraper(),
                              'TruthOrFiction': TruthOrFictionScraper(),
                              'Polygraph': PolygraphScraper(),
                              'Snopes': SnopesScraper(),
                              'CNN': CnnAPI()}
        # C:/Users/adirc/Desktop/
        with open('/home/wtfact/Documents/Keys and Settings/scrapers_passwords.json') as scrapers_passwords_file:
            scrapers_passwords = json.load(scrapers_passwords_file)
        self.scrapers_passwords = {'AfricaCheck': scrapers_passwords['AfricaCheck'],
                                   'FactScan': scrapers_passwords['FactScan'],
                                   'ClimateFeedback': scrapers_passwords['ClimateFeedback'],
                                   'GossipCop': scrapers_passwords['GossipCop'],
                                   'Politifact': scrapers_passwords['Politifact'],
                                   'TruthOrFiction': scrapers_passwords['TruthOrFiction'],
                                   'Polygraph': scrapers_passwords['Polygraph'],
                                   'Snopes': scrapers_passwords['Snopes'],
                                   'CNN': scrapers_passwords['CNN']}
        # self.scrapers_num_pages = {'AfricaCheck': -1,
        #                            'FactScan': -1,
        #                            'ClimateFeedback': -1,
        #                            'GossipCop': -1,
        #                            'Politifact': -1,
        #                            'TruthOrFiction': -1,
        #                            'Polygraph': -1,
        #                            'Snopes': -1,
        #                            'CNN': -1}
        with open('/home/wtfact/Documents/Keys and Settings/email_password.json') as email_password_file:
            email_password = json.load(email_password_file)
        self.email = email_password['Email']
        self.email_pass = email_password['Password']
        keys = ['title', 'claim', 'description', 'url', 'verdict_date', 'tags',
                'category', 'label', 'image_src', 'add_comment', 'user_id', 'username']
        with open('claims.csv', 'a', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()

    def extract_claims_from_scrapers(self, num_of_pages):
        print('start')
        try:
            self.client.get(self.API_BASE_ENDPOINT)
            cookies = dict(self.client.cookies)
            csrf_token = self.client.cookies['csrftoken']
            headers = {'Referer': self.API_ADD_CLAIM_ENDPOINT, "X-CSRFToken": csrf_token}
            scrapers_ids = json.loads(self.client.get(self.API_SCRAPERS_IDS_ENDPOINT).content.decode('utf-8'))
            # for the first time to send scrapers' claims
            all_scrapers_claims = []
            for scraper_name, scraper_class in self.scrapers_dict.items():
                try:
                    claims_info_arr = scraper_class.extract_claims_info(num_of_pages)
                    print('Finished importing claims from %s' % scraper_name)
                    for claim_info in claims_info_arr:
                        claim_info['add_comment'] = 'true'
                        claim_info['user_id'] = scrapers_ids[scraper_name]
                        claim_info['username'] = scraper_name
                        self.update_csv(claim_info)
                        claim_info['password'] = self.scrapers_passwords[scraper_name]
                        # for the first time to send scrapers' claims
                        all_scrapers_claims.append(claim_info)
                        # requests.post(url=self.API_ADD_CLAIM_ENDPOINT, data=claim_info, headers=headers,
                        #               cookies=cookies)
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

    def update_csv(self, claim_info):
        keys = ['title', 'claim', 'description', 'url', 'verdict_date', 'tags',
                'category', 'label', 'image_src', 'add_comment', 'user_id', 'username']
        with open('claims.csv', 'a', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writerow(claim_info)

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