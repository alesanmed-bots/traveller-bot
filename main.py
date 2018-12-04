# encoding: utf-8

from scrapper import TravelScrapper
from bot import ElViajanteBot
import tools.logger as logger
import configparser

if __name__ == "__main__":
    config = configparser.ConfigParser()

    config.read('config.ini')

    logger.init_logger(config['LOGGING']['logger_name'])

    scrapper = TravelScrapper(
        config['LOGGING']['logger_name'], config['PERSISTENCE']['db_name'])

    scrapper.scrap()

    elviajante = ElViajanteBot(
        config['TELEGRAM']['bot_token'], config['PERSISTENCE']['db_name'],
        config['LOGGING']['logger_name'])

    elviajante.send_unfetched_travels(config['TELEGRAM']['chat_id'])
