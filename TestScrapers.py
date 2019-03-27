from SnopesScraper import SnopesScraper
from TruthOrFictionScraper import TruthOrFictionScraper
from PolygraphScraper import PolygraphScraper
from PolitifactScraper import PolitifactScraper
from GossipCopScraper import GossipCopScraper
from ClimateFeedbackScraper import ClimateFeedbackScraper
from FactScanScraper import FactScanScraper
import unittest


class TestScrapers(unittest.TestCase):

    def test_snopes_scraper(self):
        self.snopes_scraper = SnopesScraper()
        try:
            claims_info_arr = self.snopes_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 12)
        except:
            self.assertTrue(False)

    def test_polygraph_scraper(self):
        self.polygraph_scraper = PolygraphScraper()
        try:
            claims_info_arr = self.polygraph_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 12)
        except:
            self.assertTrue(False)

    def test_truth_or_fiction_scraper(self):
        self.truth_or_fiction_scraper = TruthOrFictionScraper()
        try:
            claims_info_arr = self.truth_or_fiction_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 10)
        except:
            self.assertTrue(False)

    def test_politifact_scraper(self):
        self.politifact_scraper = PolitifactScraper()
        try:
            claims_info_arr = self.politifact_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 20)
        except:
            self.assertTrue(False)

    def test_gossip_cop_scraper(self):
        self.gossip_cop_scraper = GossipCopScraper()
        try:
            claims_info_arr = self.gossip_cop_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 15)
        except:
            self.assertTrue(False)

    def test_climate_feedback_scraper(self):
        self.climate_feedback_scraper = ClimateFeedbackScraper()
        try:
            claims_info_arr = self.climate_feedback_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 10)
        except:
            self.assertTrue(False)

    def test_fact_scan_scraper(self):
        self.fact_scan_scraper = FactScanScraper()
        try:
            claims_info_arr = self.fact_scan_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 5)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
