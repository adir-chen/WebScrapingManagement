from AbstractScraper import AbstractScraper
from datetime import datetime


class PolitifactScraper(AbstractScraper):

    def __init__(self, scraper_name='Politifact', scraper_url='https://www.politifact.com/truth-o-meter/statements/?page='):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
            contents = page_soup.find('section', class_='scoretable').findAll('div', class_='scoretable__item')
            for element in contents:
                # url
                url = self.scraper_url.split('.com')[0] + '.com' + element.find('a', class_='link')['href']

                # open article page
                article_page = super().open_fact_check_page(url)

                # title
                title = article_page.find('h1', class_='article__title').text

                # description
                description = article_page.find('div', class_='article__text').find('p').text.strip().split('.')[0] + '.'

                # verdict_date
                verdict_date_full = element.find('span', class_='article__meta').text.strip().split(',')
                verdict_date = verdict_date_full[1].strip().split(' ')[0] + ' ' + super().replace_suffix_in_date(verdict_date_full[1].strip().split(' ')[1]) + ', ' + verdict_date_full[2].strip()
                verdict_datetime = datetime.strptime(verdict_date, '%B %d, %Y')
                verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                # category
                category = 'Politics'

                # claim
                claim = element.find('div', class_='statement__source').text.strip() + '-' + element.find('a', class_='link').text.strip()

                # label
                label = element.find('div', class_='meter').find('img')['alt'].strip()

                # tags
                tags = ','.join(super().extract_tags(claim))

                # img_src
                img_src = element.find('div', class_='statement__body').find('img')['src']

                claim_info_dict = {'username': self.scraper_name,
                                   'title': title,
                                   'claim': claim,
                                   'description': description,
                                   'url': url,
                                   'verdict_date': verdict_date,
                                   'tags': tags,
                                   'category': category,
                                   'label': label,
                                   'img_src': img_src}
                claims_info_arr.append(claim_info_dict)
                break
            page_num += 1
        return claims_info_arr
