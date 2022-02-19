from web3 import Web3

api_me = "https://mainnet.infura.io/v3/30f7ab5b0ddf405e94ad370215c07e90"
api = "https://mainnet.infura.io/v3/d54488de03624315ac354d4acd95e344"

w3 = Web3(Web3.HTTPProvider(api))
pending = w3.eth.getBlock("pending")

gas_price1 = w3.eth.gasPrice
gwi = w3.fromWei(gas_price1, 'gwei')

print(gwi)

print(pending["number"])
print(len(pending["transactions"]))


