# encoding: utf-8
"""
scrapper.py

Created by Donzok on 17/06/2017.
Copyright (c) 2017 . All rights reserved.
"""
import logging
import requests
from tools.user_agent import get_user_agent
from tools.parse_travel import parse_travel
from database.transactions import TransactionsEngine
from bs4 import BeautifulSoup as bs
import time
import random


class TravelScrapper():
    def __init__(self, log_name, db_name):
        self.URL = "http://www.exprimeviajes.com/"

        self.logger = logging.getLogger(log_name)

        self.transactions_engine = TransactionsEngine(db_name)

    def scrap(self):
        header = {'user-agent': get_user_agent()}

        attempt = 0
        document = None
        for attempt in range(5):
            if document is None:
                try:
                    document = requests.get(self.URL, headers=header).text
                except Exception as e:
                    self.logger.error(e)
                    self.logger.debug("Error loading webpage. Attempt number {0}".format(attempt + 1))
                    time.sleep(random.randrange(3) + 3)

        if document is None:
            self.logger.error("Error loading webpage. Max attempts reached, going to sleep...")
        else:
            web = bs(document, "html.parser")

            last_url = self.transactions_engine.get_last_to_check()
            first = True
            last_reached = False
            for h2 in web.findAll('h2', class_="entry-title"):
                if not last_reached:
                    link = h2.a
                    travel_url = link['href']

                    self.logger.debug("Parsing {0}".format(travel_url))

                    if last_url is not None and travel_url == last_url:
                        last_reached = True
                        self.logger.info("Last travel reached, going to sleep...")
                    else:
                        date = parse_travel(travel_url, self.logger)

                        self.transactions_engine.insert_travel(travel_url, date)

                        time.sleep(5)

                        if first:
                            first = False
                            self.transactions_engine.update_last_to_check(str(travel_url))
        return 0