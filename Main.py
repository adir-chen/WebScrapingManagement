from WebScrapingManage import WebScrapingManage
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    num_of_pages = 1
    w_s_m = WebScrapingManage()
    # w_s_m.validate_scrapers(num_of_pages=1)
    w_s_m.extract_claims_from_scrapers(num_of_pages)
    #scheduler = BlockingScheduler()
    #scheduler.add_job(w_s_m.extract_claims_from_scrapers, 'interval', hours=12)
    #scheduler.start()


if __name__ == '__main__':
    main()


