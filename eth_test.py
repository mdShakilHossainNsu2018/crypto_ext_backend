from web3 import Web3

api = "https://mainnet.infura.io/v3/30f7ab5b0ddf405e94ad370215c07e90"

w3 = Web3(Web3.HTTPProvider(api))
w3.eth.get_block('latest')
gas_price1 = w3.eth.gasPrice
w3.fromWei(gas_price1, 'gwei')

