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
            contents = page_soup.findAll('article')
            for element in contents:
                # title
                title = element.find('h2').text

                # url
                url = element.find('a')['href']

                # open article page
                article_page = super().open_fact_check_page(url)

                # description
                description = article_page.find('meta', attrs={'name': 'description'})['content']

                # verdict date
                verdict_datetime = datetime.strptime(article_page.find('meta', attrs={'name': 'weibo:article:create_at'})['content'].split()[0], '%Y-%m-%d')
                verdict_date = datetime.strftime(verdict_datetime, '%d/%m/%Y')

                # category
                category = 'Fact Checks'
                all_categories = page_soup.find('span', class_='cat-links').find_all('a')
                for categ in all_categories:
                    if categ.text.strip() != 'Disinformation' and categ.text.strip() != 'Fact Checks':
                        category = categ.text
                        break

                # label
                label = article_page.find('div', class_='rating-description').text.strip()

                # claim
                claim = article_page.find('div', class_='claim-description').text.strip()

                # tags
                site_tags = []
                tags_content = article_page.find('ul', class_='tt-tags')
                if tags_content:
                    tags_content = tags_content.find_all('li')
                    for tag in tags_content:
                        site_tags.append(tag.text.strip())
                tags = super().clean_site_tags(site_tags)
                tags = super().get_optional_tags(tags, super().extract_tags(claim))

                # img_src
                try:
                    img_src = article_page.find('a', class_='tt-thumb')['href']
                except Exception:
                    img_src = ''

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
