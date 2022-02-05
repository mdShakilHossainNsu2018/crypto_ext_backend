import asyncio
from binance import AsyncClient, BinanceSocketManager
from decouple import config
import time
from binance import ThreadedWebsocketManager

BINANCE_API_KEY = config("BINANCE_API_KEY")
BINANCE_SECRET_KEY = config("BINANCE_SECRET_KEY")


# def main():
#
#     symbol = 'BNBBTC'
#
#     twm = ThreadedWebsocketManager(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
#     # start is required to initialise its internal loop
#     twm.start()
#
#     def handle_socket_message(msg):
#         print(f"message type: {msg['e']}")
#         print(msg)
#
#     twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
#
#     # multiple sockets can be started
#     twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)
#
#     # or a multiplex socket can be started like this
#     # see Binance docs for stream names
#     streams = ['bnbbtc@miniTicker', 'bnbbtc@bookTicker']
#     twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
#
#     twm.join()

async def main():
    client = await AsyncClient.create(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket('BTCBUSD')
    # ts = bm.trade_socket('BTCUSDT')
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

