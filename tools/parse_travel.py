# encoding: utf-8

from bs4 import BeautifulSoup as bs
import requests
import logging
from tools.user_agent import get_user_agent
import time
import random
import re


def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def parse_travel(travel_url, logger):
    travel_date = None

    if type(travel_url) != str:
        raise ValueError("travel_url is not a String object")

    header = {'user-agent': get_user_agent()}

    attempt = 0
    document = None

    for attempt in range(5):
        try:
            document = requests.get(travel_url, headers=header).text
            break
        except Exception as e:
            logger.error(e)
            logger.debug("Error loading travel page. Attempt number {0}".format(attempt + 1))
            time.sleep(random.randrange(3) + 3)

    if attempt >= 4:
        logger.error("Error loading travel page. Max attempts reached, returning...")
    else:
        travel_page = bs(document, 'html.parser')

        content = travel_page.find(
            "div",
            class_="entry-content").find_all("p")

        for p in content:
            if p.find(text=re.compile("Fechas")):
                travel_date = p.text.split("Fechas:")[-1].strip()

                break

    return travel_date
