import websocket
import logging
import json

class Channel:

    def __init__(self, channel, endpoint="ws://127.0.0.1:3000/cable/"):
        self.logger = logging.getLogger(__name__)
        self.endpoint = endpoint
        self.channel = channel
        self.identifier = { 'channel': channel }

    def send_command(self, cmd_type, data={}):
        self.logger.debug('send_command: %s, %s' % (cmd_type, data))
        self.ws.send( json.dumps({'command':cmd_type, 'identifier':json.dumps(self.identifier), 'data':json.dumps(data) }) )

    def send_message(self, data={}):
        self.send_command('message', data)

    def perform(self, action, data={}):
        data['action'] = action
        self.send_message(data)

    def on_open(self, ws):
        self.logger.info("opened")
        self.send_command('subscribe')

    def _on_message(self, ws, message):
        obj = json.loads(message)
        self.on_message(obj)

    def on_message(self, message):
        self.logger.debug("on_message: %s" % message)

    def on_error(self, ws, error):
        self.logger.error("on_error: %s" % error)

    def on_close(self, ws):
        self.logger.info("closed")

    def connect(self):
        self.ws = websocket.WebSocketApp(self.endpoint,
                on_message = self._on_message,
                on_error = self.on_error,
                on_close = self.on_close,
                on_open = self.on_open)
        self.ws.run_forever()

if __name__ == "__main__":
    channel = Channel("QuotesChannel")
    channel.connect()

