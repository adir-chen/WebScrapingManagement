from AbstractScraper import AbstractScraper
from datetime import datetime


class ClimateFeedbackScraper(AbstractScraper):

    def __init__(self, scraper_name='ClimateFeedback', scraper_url='https://climatefeedback.org/claim-reviews/'):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            try:
                page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
                contents = page_soup.findAll('div', class_='row')[1:-1]
                for element in contents:
                    try:
                        # title
                        title = element.find('a').text.strip()

                        # url
                        url = element.find('a')['href']

                        # open article page
                        article_page = super().open_fact_check_page(url)

                        # description
                        description = article_page.find('meta', attrs={'property': 'og:description'})['content']

                        # verdict_date
                        verdict_date_full = article_page.find('p', class_='small').find_next('p').text.strip().split('Published on:')[1].split('|')[0].strip().split(' ')
                        verdict_date = verdict_date_full[1].strip() + ' ' + verdict_date_full[0].strip() + ', ' + verdict_date_full[2].strip()
                        verdict_datetime = datetime.strptime(verdict_date, '%b %d, %Y')
                        verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                        # category
                        category = 'Climate'

                        # claim
                        claim = element.find('div', class_='feedpages-excerpt').text.strip()

                        # label
                        label = element.find('img', class_='fact-check-card__row__verdict__img')['src'].split('HTag_')[1].split('.png')[0]

                        # tags
                        tags = ','.join(super().extract_tags(claim))

                        # img_src
                        img_src = element.find('img', class_='feedpages__claim__container__illustration__screenshot__img')['src'].split('.png')[0]

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
                    except Exception as e:
                        continue
                print(page_num)
                page_num += 1
            except Exception as e:
                print(page_num)
                page_num += 1
                continue
        return claims_info_arr
