import unittest
from SnopesScraper import SnopesScraper
from TruthOrFictionScraper import TruthOrFictionScraper
from PolygraphScraper import PolygraphScraper


class TestScrapers(unittest.TestCase):

    def test_snopes_scraper(self):
        self.snopes_scraper = SnopesScraper()
        try:
            claims_info_arr = self.snopes_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 12)
        except:
            self.assertTrue(False)

    def test_truth_or_fiction_scraper(self):
        self.truth_or_fiction_scraper = TruthOrFictionScraper()
        try:
            claims_info_arr = self.truth_or_fiction_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 1)
        except:
            self.assertTrue(False)

    def test_polygraph_scraper(self):
        self.polygraph_scraper = PolygraphScraper()
        try:
            claims_info_arr = self.polygraph_scraper.extract_claims_info(1)
            self.assertTrue(len(claims_info_arr) == 8)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()