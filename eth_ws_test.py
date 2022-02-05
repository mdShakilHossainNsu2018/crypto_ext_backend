from web3 import Web3


# wss://mainnet.infura.io/ws/v3/d54488de03624315ac354d4acd95e344
ws_url1 = "wss://mainnet.infura.io/ws/v3/d54488de03624315ac354d4acd95e344"
ws_url2 = "wss://mainnet.infura.io/ws/v3/30f7ab5b0ddf405e94ad370215c07e90"

web3 = Web3(Web3.WebsocketProvider(ws_url2))

print(web3.isConnected())

