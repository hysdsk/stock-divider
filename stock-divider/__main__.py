from configparser import ConfigParser
from datetime import datetime
from . import schedulescraper

def main():
    config = ConfigParser()
    config.read("config.ini")
    ss = schedulescraper.Context(config)
    exists = [symbol["symbol_code"] + str(symbol["right_last_date"]) for symbol in ss.dbconnector.find_all()]
    srclist = [src for src in ss.scraper() if src["symbol_code"] + src["right_last_date"].strftime("%Y%m%d") not in exists]
    for src in srclist:
        src["right_last_date"] = int(src["right_last_date"].strftime("%Y%m%d"))
        ss.dbconnector.save_one(src)
    
    targets = ss.dbconnector.find_by_status("0")
    today = datetime.now().date()
    for target in targets:
        rightlastdate = datetime.strptime(str(target["right_last_date"]), "%Y%m%d").date()
        if today <= rightlastdate:
            continue
        target["status"] = "1"
        ss.dbconnector.apply_divide(target)
        ss.dbconnector.save_one(target)


if __name__ == '__main__':
    main()
