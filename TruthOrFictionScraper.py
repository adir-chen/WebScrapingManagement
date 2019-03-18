from AbstractScraper import AbstractScraper
from datetime import datetime


class TruthOrFictionScraper(AbstractScraper):

    def __init__(self, scraper_name='TruthOrFiction', scraper_url='https://www.truthorfiction.com/category/fact-checks/page/'):
        self.scraper_name = scraper_name
        self.scraper_url = scraper_url
        super().__init__()

    def extract_claims_info(self, num_of_pages):
        page_num = 1
        claims_info_arr = []
        while page_num <= num_of_pages:
            page_soup = super().open_fact_check_page(self.scraper_url + str(page_num))
            container = page_soup.findAll('div', class_='container')[3]
            contents = container.findAll('a', class_='tt-post-title')
            for element in contents:
                # title
                title = element.text.strip()

                # url
                url = element['href']

                # open article page
                article_page = super().open_fact_check_page(url)

                # description
                description = article_page.find('meta', attrs={'name': 'description'})['content']

                # verdict date
                verdict_datetime = datetime.strptime(article_page.find('span', class_='tt-post-date-single').text.strip(), '%B %d, %Y')
                verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                # category
                category = 'Fact Checks'
                all_categories = article_page.find('div', class_='tt-blog-category post-single text-center').find_all('a')
                for categ in all_categories:
                    if categ.text.strip() != 'Disinformation' and categ.text.strip() != 'Fact Checks':
                        category = categ.text
                        break

                # label
                label = article_page.find('div', class_='rating-description').text.strip()

                # claim
                claim = article_page.find('div', class_='claim-description').text.strip()

                # tags
                tags = []
                tags_content = article_page.find('ul', class_='tt-tags').find_all('li')
                for tag_content in tags_content:
                    tags.append(tag_content.text.strip())
                # tags = ','.join(tags)
                tags = ','.join(super().extract_tags(' '.join(tags)))

                # img_src
                img_src = article_page.find('a', class_='tt-thumb')['href']

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
                break
            page_num += 1
            break
        return claims_info_arr
