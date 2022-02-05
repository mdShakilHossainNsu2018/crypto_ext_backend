import websocket
import _thread
import time
from django.core.management.base import BaseCommand
from django.utils import timezone


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("WS connected")
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())


class Command(BaseCommand):
    help = 'Binance Websocket'

    def handle(self, *args, **kwargs):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)

        ws.run_forever()
        print("All done")

