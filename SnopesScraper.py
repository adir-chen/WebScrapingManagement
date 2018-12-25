from AbstractScraper import AbstractScraper
from datetime import datetime


class SnopesScraper(AbstractScraper):

    def __init__(self, scraper_name='Snopes', scraper_url='https://www.snopes.com/fact-check/page/'):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
            contents = page_soup.find('div', class_='list-group').findAll('article')
            for element in contents:
                # title
                title = element.h2.text
                # description
                description = element.find_next('p').text.strip().split('-', 1)[1].strip()
                # url
                url = element.a['href']
                # verdict date
                verdict_datetime = datetime.strptime(element.find_next('p').text.strip().split('-', 1)[0].strip(), '%d %B %Y')
                verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')
                # category
                article_page = super().open_fact_check_page(url)
                article_page_all_categories = article_page.find('ol', class_='breadcrumb').find_all('li')
                # category
                category = article_page_all_categories[len(article_page_all_categories) - 1].a.text.strip()
                # label
                label = article_page.find('div', class_='rating-text').text.strip().split('\n')[0]
                # claim
                claim = article_page.find('p', class_='claim').text.strip()
                # tags
                tags = ' '.join(super().extract_tags(claim))
                img_src = article_page.find('div', class_='featured-asset').find('img', class_='bg-image')['data-lazy-src'].split(
                    '.jpg')[0] + '.jpg'
                if not super().check_if_claim_exists(url):
                    claim_info_dict = {'username': self.scraper_name, 'title': title, 'claim': claim, 'description': description, 'url': url,
                                       'verdict_date': verdict_date, 'tags': tags, 'category': category, 'label': label, 'img_src': img_src}
                    claims_info_arr.append(claim_info_dict)
                page_num += 1

        return claims_info_arr
