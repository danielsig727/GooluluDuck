#!/usr/bin/env python

from slackbot.bot import Bot
import logging

from slackbot import settings

if getattr(settings, 'LOGGING_FORMAT', None):
    logging.basicConfig(format=settings.LOGGING_FORMAT, level=logging.INFO)

logging.basicConfig(level=logging.INFO)

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
