import threading
import websocket
import logging
import json
from channel import Channel

MINUTE          = 60
FIVE_MINUTES    = 60*5
FIFTEEN_MINUTES = 60*15
THIRTY_MINUTES  = 60*30
HOUR            = 60*60
FOUR_HOURS      = HOUR*4
DAILY           = HOUR*24

class QuotesChannel(Channel):

    def __init__(self, interval=FIVE_MINUTES,
                       endpoint="ws://127.0.0.1:3000/cable/",
                       on_quotes=None):
        Channel.__init__(self, "QuotesChannel", endpoint)
        self.interval = interval
        self.on_quotes = on_quotes
        self._start_timer()
        self.connect()

    def _start_timer(self):
        self.timer = threading.Timer(self.interval, self.on_timer)
        self.timer.start()

    def on_message(self, message):
        if "message" in message and type(message["message"]) is dict:
            if message["message"]["type"] == 'quote':
                if self.on_quotes:
                    self.on_quotes(message["message"]["quotes"])

    def on_timer(self):
        self.get_quotes()
        self._start_timer()

    def get_quotes(self):
        self.logger.debug("get_quotes")
        self.perform("request_for_quote", { "symbol":"*" })


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    def _print_quotes(quotes):
        print("Received %s quotes" % len(quotes))
    qc = QuotesChannel(5, on_quotes=_print_quotes)

