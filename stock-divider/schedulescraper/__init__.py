from .scraper import Scraper
from .dbconnector import SymbolsConnector

class Context(object):
    def __init__(self, config):
        self.scraper = Scraper(config["schedule"])
        self.dbconnector = SymbolsConnector(config["database"])
