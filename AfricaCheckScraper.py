from AbstractScraper import AbstractScraper
from datetime import datetime


class AfricaCheckScraper(AbstractScraper):

    def __init__(self, scraper_name='AfricaCheck', scraper_url='https://africacheck.org/latest-reports/page/'):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
            contents = page_soup.find('div', class_='col-sm-8 clearfix').findAll('article')
            for element in contents:
                # title
                title = element.find('h2').text.strip()

                # url
                url = element.find('h2').find('a')['href']

                # open article page
                article_page = super().open_fact_check_page(url)

                # description
                description = article_page.find('meta', attrs={'name': 'description'})['content']

                # verdict date
                verdict_date_full = element.find('p', class_='date-published').text.strip().split('| ')[1].split(' ')
                verdict_date = verdict_date_full[1].strip() + ' ' + super().replace_suffix_in_date(verdict_date_full[0].strip()) + ', ' + verdict_date_full[2].strip()
                verdict_datetime = datetime.strptime(verdict_date, '%B %d, %Y')
                verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                # category
                category = element.find('ul', class_='tag-list').find('li').text.strip()

                # claim
                claim = article_page.find('div', class_='report-claim').find('p').text.strip()

                # label
                label = element.find('div', class_='verdict-stamp').text.strip()

                # tags
                tags = []
                for tag in element.find('ul', class_='tag-list').findAll('li')[1:]:
                    tags.append(tag.find('a').text.strip())
                # tags_claim = super().extract_tags(claim)
                # tags = list(set(tags_list + tags_claim))
                tags = ','.join(super().extract_tags(' '.join(tags)))

                # img_src
                img_src = element.find('img')['src']

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
