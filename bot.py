# encoding: utf-8
"""
bot
 
Created by Donzok on 17/06/2017.
Copyright (c) 2017 . All rights reserved.
"""
from database.transactions import TransactionsEngine
from telegram.ext import Updater
from telegram.ext import CommandHandler
import time


class ElViajanteBot:

    def __init__(self, token, db_name):
        self.updater = Updater(token=token)

        self.dispatcher = self.updater.dispatcher

        # start_handler = CommandHandler('start', self.start)

        # self.dispatcher.add_handler(start_handler)

        # self.updater.start_polling()

        self.transactions_engine = TransactionsEngine(db_name)

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Soy un bot sin comandos :(")

    def send_message(self, chat_id, text, date):
        bot = self.updater.bot

        if date is None:
            date = "Desconocidas"

        text = "{0} \n Fechas: {1}".format(text, date)

        return bot.sendMessage(chat_id=chat_id, text=text, parse_mode='HTML')

    def send_unfetched_travels(self, chat_id):
        travels = self.transactions_engine.get_unfetched_travels()

        for travel in travels:
            sent = self.send_message(chat_id, travel[0], travel[1])

            if sent:
                self.transactions_engine.set_travel_fetched(travel[0])
            
            time.sleep(5)
        
        self.updater.stop()
        
        return 0
