from WebScrapingManage import WebScrapingManage
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    w_s_m = WebScrapingManage()
    w_s_m.extract_claims_from_scrapers(1)# @ToDo: add true
    #scheduler = BlockingScheduler()
    #scheduler.add_job(w_s_m.extract_claims_from_scrapers, 'interval', hours=12)
    #scheduler.start()


if __name__ == '__main__':
    main()


