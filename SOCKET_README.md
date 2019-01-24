# Allbit Socket.io

Use socket.io client implementations for your platform to connect.
The examples on this page will be based on [socket.io-client](https://github.com/socketio/socket.io-client), the official javascript implementation.

## Client Initialization

The request URL looks like "https://ws.allbit.com/socket/" (on polling transport) or "wss://ws.allbit.com/socket/"(on websocket transport).
The following example shows how to connect and initialize client in javascript.

~~~
const io = require('socket.io-client')
const client = io('https://ws.allbit.com', {
  path: '/socket'
)
~~~

In this case, it is important not to pass something like 'https://ws.allbit.com/socket/' as the first argument of the function.
If you do such thing, the client will keep trying to connect to URL 'https://ws.allbit.com/socket.io/' with namespace called 'socket' which results in connection failure.

## Emitting Events to Server

There are three types of events that client can emit.

### subscribe

Emitting an event of this type makes client start or stop retrieving information regarding specific cryptocurrency markets.

You can make the client start or stop retrieving information by emitting event like following example.
~~~
client.emit('subscribe', {
  e: 'select',
  coin: 'APOT', // The base coin symbol of market you want to retrieve information
  quote: 'ETH' // The quote coin symbol of market you want to retrieve information
}) // If you want to retrieve information from single market.

client.emit('subscribe', {
  e: 'select',  
  pairs: [{
    coin: 'APOT',
    quote: 'ETH'
  }, ...] // Array of objects that contains base and quote information.
}) // If you want to retrieve information from multiple markets.

client.emit('subscribe', {
  e: 'end'
}) // If you want to stop retrieving market information.
~~~

Whenever you emit subscribe event that contains 'start' as the value of key 'e', existing subscriptions will be cancelled and overwritten by new.

### user

Emitting an event of this type makes client start or stop retrieving information regarding specific cryptocurrency wallet.
~~~
client.emit('user', {
  e: 'login',
  api: 'API KEY', // When logging in with open API.
  token: 'ALLBIT SESSION KEY', // When logging in from allbit.com
}) // user authentication

client.emit('user', {
  e: 'wallet',
  id: 9999, // use if you know wallet id
  addr: '0x0123456789abcdef' // use if you know wallet address
}) // selecting wallet after user authentication

client.emit('user', {
  e: 'logout'
}) // If you want to stop retrieving wallet information.
~~~

### buffer
(to be implemented)

## Handling Events Emitted from Server(편집 및 작성중)

### coin
~~~
eventName : coin
			msg = [
				{e='tx', thash=0x0000}
				{e='trade', sell=true/false, v=volume, p=price, t=timestamp, seller=wallet_address, buyer=wallet_address, base=base_token_name, quote=quote_token_name}
				{e='order', n = 'KKO', q = 'ETH', 
					               d = {
					                    "buyer": [{
					                    "price": "0.10000000",
					                    "amount": "2000000000000000000",
					                    "decAmount": "2.0000"
					                   }, {
					                       "price": "0.00010000",
					                       "amount": "1222000000000000000000",
					                       "decAmount": "1222.0000"
					                   }],
					                   "seller": [{
					                       "price": "0.00040000",
					                       "amount": "1222000000000000000000",
					                       "decAmount": "1222.0000"
					                   }]
		        			       }
				}
			]
~~~

### wallet
~~~
		eventName : wallet
			[

				TxFail			{e='txfail', thash=0x0000}
				TxBind			{e='tx', thash=0x0000}
					Trade			{e='trade', ohash=0x0000, seller=bool, maker=bool, base=KKO, quote=quote_token_name, v=volume, p=price, t=timestamp, }
					OrderChange 	{e='order', ohash=0x0000, sell=bool, base=KKO, quote=quote_token_name, v=amount, p=price, remian=주문 미체결 잔여량, cancel=bool, status=status값, t=timestamp}
					BalanceChange	{e='balance', coin=KKO, v=tokenBalance}

					Withdraw 		{e='withdraw', a = amount, fee = 수수료, coin = EOS}
					Deposit 		{e='deposit', a=amount, coin = EOS}
			]
~~~
### update
~~~
eventName : update
			msg = [
					{e='info',d=[
	                        {
		                        n: info.name,
		                        p: info.price,
		                        dp: info.dailyprice,
		                        rc: info.recent_coin,
		                        i: info.id,
		                        e: info.recent_eth,
		                        l: info.today_low,
		                        h: info.today_high,
		                        d: info.decimal,
		                        pid: pair_id
	                    	}, Array...
	                    ]

	                }
                    {e='price', d={eth_usd='289.90924856', gas_price='46.00000000'}}
				]
~~~

### refresh
~~~
eventName : refresh // flag 가 바뀌거나 wallet_avail 이 바뀌거나 flag,wallet_avail 중 하나 이상이 0 이 아닌상태로 처음 생길때 아래 이벤트 전송, 여러개 동시에 된 경우 여러개가 동시에 전송
			msg = {
			  "OMG": {
			    "id": 3,
			    "name": "OMG",
			    "raw_name": "OmiseGO",
			    "icon": "https://s3.ap-northeast-2.amazonaws.com/allbit-static/coinImage/3_125X125.png",
			    "address": "0x85080dbf2283acd538fd4f4d737bc54cab02ad18",
			    "decimal": 18,
			    "price": "0.00300000000000000000",
			    "dailyprice": "0.00004000000000000000",
			    "today_high": "0.10000000000000000000",
			    "today_low": "0.00010000000000000000",
			    "recent_coin": "0.00000000000000000000",
			    "recent_eth": "0.00000000000000000000",
			    "coin_id": 3,
			    "deal_id": null,
			    "flag": 0,
			    "new_day": 0,
			    "wallet_avail": 1
			  }
			}
~~~