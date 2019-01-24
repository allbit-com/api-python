import api

api.BASE_URL = "https://api.allbit.com"
wallet = "YOUR_WALLET_ADDRESS"
apiKey = "YOUR_API_KEY"
pwd = "YOUT_WALLET_PASSWORD"

#get market pair list
r = api.coinList()
print(r)

#get order depth
pairId = "PAIR_ID"
r = api.orderList(pairId)
print(r)

#get recent trade
pairId = "PAIR_ID"
r = api.tradeList(pairId)
print(r)

#get my account
r = api.coinAmount(wallet, apiKey)
print(r)

#get my waiting orders
r = api.runOrder(wallet, apiKey)
print(r)

#get order status
orderHash = "ORDER_HASH"
orders = [orderHash]
r = api.orderStatus(orders)
print(r)

#make order raw hash
orders = []
order = {}
order['pair'] = 1
order['isSell'] = True
order['amount'] = "1000000000000000000" #amount * 10 ** token_decimals
order['price'] = "0.52000000" #Number of decimal places supported by Market (ETH,BTC : 8 decimals)
orders.append(order)
r = api.generateOrder(wallet, apiKey, pwd, orders)
print(r)

#make cancel order raw hash
orderHash = "ORDER_HASH"
orders = [orderHash]
r = api.cancelOrder(wallet, apiKey, orders)
print(r)

#submit hash signature (after generateOrder, cancelOrder)
respList = [ORDER_RESP, CANCEL_ORDER_RESP, ...]
r = api.signMessage(wallet, apiKey, respList, pwd)




