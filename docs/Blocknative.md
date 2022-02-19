# Description of Terms
    maxPrice
Highest priced transaction in the mempool

    currentBlockNumber
Block number at the time of prediction

    msSinceLastBlock
Milliseconds since the last block was mined relative to when data was computed

    blockNumber
Block this prediction is for

    baseFeePerGas
Base fee per gas for current block in gwei. (Only type2 transactions Post EIP-1559 have this value and it's burned by the network upon transaction success).

    estimatedTransactionCount
Number of items we estimate will be included in next block based on mempool snapshot
    
    confidence
0-99 likelihood the next block will contain a transaction with a gas price >= to the listed price
    
    Price
Price in Gwei (used for type0 transactions: Pre EIP-1559)

    maxPriorityFeePerGas
Max priority fee per gas in gwei also known as the "tip" (used for type2 transactions: EIP-1559)

    maxFeePerGas
Max fee per gas in gwei (used for type2 transactions: EIP-1559). Our current max fee heuristic is Base Fee * 2 + Priority Fee. This is to protect against a ‘rapid’ rise in the base fee while your transaction fee is pending. In most cases, the actual transaction fee will approximate Base Fee + Priority Fee.

## Example Response Payload

```json
{
  "system": "ethereum",
  "network": "main",
  "unit": "gwei",
  "maxPrice": 123,
  "currentBlockNumber": 13005095,
  "msSinceLastBlock": 3793,
  "blockPrices": [
    {
      "blockNumber": 13005096,
      "baseFeePerGas": 94.647990462,
      "estimatedTransactionCount": 137,
      "estimatedPrices": [
        {
          "confidence": 99,
          "price": 104,
          "maxPriorityFeePerGas": 9.86,
          "maxFeePerGas": 199.16
        },
        {
          "confidence": 95,
          "price": 99,
          "maxPriorityFeePerGas": 5.06,
          "maxFeePerGas": 194.35
        },
        {
          "confidence": 90,
          "price": 98,
          "maxPriorityFeePerGas": 4.16,
          "maxFeePerGas": 193.45
        },
        {
          "confidence": 80,
          "price": 97,
          "maxPriorityFeePerGas": 2.97,
          "maxFeePerGas": 192.27
        },
        {
          "confidence": 70,
          "price": 96,
          "maxPriorityFeePerGas": 1.74,
          "maxFeePerGas": 191.04
        }
      ]
    }
  ]
}
```


