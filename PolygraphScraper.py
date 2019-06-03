from AbstractScraper import AbstractScraper
from datetime import datetime


class PolygraphScraper(AbstractScraper):

    def __init__(self, scraper_name='Polygraph', scraper_url='https://www.polygraph.info/z/20382?p='):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
            contents = page_soup.findAll('div', class_='fc-hdr')
            claims_info_arr = []
            for element in contents:
                # title
                title = element.find('a', class_='title').find('h4').text

                # url
                url = self.scraper_url.split('/z/20382?p=')[0] + element.find('a', class_='title')['href']

                # open article page
                article_page = super().open_fact_check_page(url)

                # description
                description = article_page.find('meta', attrs={'name': 'description'})['content']

                # verdict date
                verdict_datetime = article_page.find('span', class_='date').text.strip()
                if 'Last Updated:' in verdict_datetime:
                    verdict_datetime = verdict_datetime.split('Last Updated:')[1].strip()
                verdict_datetime = datetime.strptime(verdict_datetime, '%B %d, %Y')
                verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                # category
                category = article_page.find('div', class_='category').text.strip()

                # claim
                claim = article_page.find('div', class_='wsw').find('p').text.strip()

                # label
                label = article_page.find('div', class_='verdict-head').find('span', class_='').text.strip()

                # tags
                site_tags = []
                tags_content = article_page.find('meta', attrs={'name': 'news_keywords'})['content'].split(',')
                for tag in tags_content:
                    site_tags.append(tag.strip())
                tags = super().clean_site_tags(site_tags)
                tags = super().get_optional_tags(tags, super().extract_tags(claim))

                # img_src
                img_src = article_page.find('div', class_='img-wrap').find('img')['src']

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
