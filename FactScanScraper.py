from AbstractScraper import AbstractScraper
from datetime import datetime


class FactScanScraper(AbstractScraper):

    def __init__(self, scraper_name='FactScan', scraper_url='http://factscan.ca/page/'):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
            contents = page_soup.findAll('article')
            for element in contents:
                # title
                title = element.find('h1').find('a')['title']

                # url
                url = element.find('h1').find('a')['href']

                # open article page
                article_page = super().open_fact_check_page(url)

                # description
                description = article_page.find('meta', attrs={'property': 'og:description'})['content']

                # verdict_date
                verdict_datetime = datetime.strptime(article_page.find('time').text, '%B %d, %Y')
                verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                # category
                category = 'Politics'

                # claim
                claim = title

                # label
                label = article_page.find('div', class_='fact-check-icon').find('img')['alt'].split(':')[1].strip()

                # tags
                site_tags = []
                for tag in article_page.find('span', class_='post-category').findAll('a'):
                    site_tags.append(tag.text.strip())
                tags = super().clean_site_tags(site_tags)
                tags = super().get_optional_tags(tags, super().extract_tags(claim))

                # img_src
                img_src = article_page.find('div', class_='post-content').findAll('img')[1]['src']

                claim_info_dict = {'username': self.scraper_name,
                                   'title': title,
                                   'claim': claim,
                                   'description': description,
                                   'url': url,
                                   'verdict_date': verdict_date,
                                   'tags': tags,
                                   'category': category,
                                   'label': label,
                                   'image_src': img_src}
                claims_info_arr.append(claim_info_dict)
            page_num += 1
        return claims_info_arr
