from AbstractScraper import AbstractScraper
from datetime import datetime


class GossipCopScraper(AbstractScraper):

    def __init__(self, scraper_name='GossipCop', scraper_url='https://www.gossipcop.com/page/'):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            try:
                page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
                contents = page_soup.find('div', {'id': 'posts'}).findAll('div', class_='post')
                for element in contents:
                    try:
                        # title
                        title = element.find('h2').find('a').text.strip()

                        # url
                        url = element.find('h2').find('a')['href']

                        # open article page
                        article_page = super().open_fact_check_page(url)

                        # description
                        description = article_page.find('meta', attrs={'name': 'description'})['content']

                        # verdict date
                        verdict_date_full = article_page.find('span', class_='dateline').text.split(',')
                        verdict_date = verdict_date_full[1].split()[0].strip() + ' ' + verdict_date_full[1].split()[1].strip() + ', ' + verdict_date_full[2].strip()
                        verdict_datetime = datetime.strptime(verdict_date, '%B %d, %Y')
                        verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                        # category
                        category = 'Entertainment'

                        # claim
                        claim = title.split('?')[0].strip()

                        # label
                        label = article_page.select('div[class^=meter]')[0].find('span').text.split(':')[1].strip()

                        # tags
                        tags = []
                        tags_list = article_page.find('p', class_='tags').findAll('a')
                        for tag in tags_list:
                            tags.append(tag.text.strip())
                        # tags = ','.join(tags)
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
                    except Exception as e:
                        continue
                print(page_num)
                page_num += 1
            except Exception as e:
                print(page_num)
                page_num += 1
                continue
        return claims_info_arr
