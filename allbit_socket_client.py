from socketIO_client_nexus import SocketIO, BaseNamespace

ACCESS_TOKEN = None
ACCESS_TOKEN_WALLET_ADDRESS = None
SOCKET_BASE = None
SOCKET_PORT = None
ALLBIT_PEM = 'ssl_cert.pem'

class AllbitEvent(BaseNamespace):


    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    def on_error(self, data):
        print('[Error]', data)

    # Allbit Socket Event
    def on_update(self, data):
        #print('on_update', data)
        #TODO implement

    def on_coin(self, data):
        #print('on_coin', data)
        #TODO implement

    # Login client only
    def on_wallet(self, data):
        #print('on_wallet', data)
        #TODO implement

    def on_root(self, data):
        #print('on_root', data)
        #TODO implement


class AllbitWatcher:

    def __init__(self):
        self.sock = SocketIO(SOCKET_BASE, SOCKET_PORT, AllbitEvent, verify=ALLBIT_PEM, resource='socket')

    def subscribe(self, coin, quote):
        self.sock.emit('subscribe', {'e': 'select', 'coin': coin, 'quote': quote})

    #pairs : [{'coin':'BTC', 'quote':'ETH'}, ...]
    def subscribeList(self, pairs):
        self.sock.emit('subscribe', {'e': 'select', 'pairs': pairs})

    def unsubscribe(self):
        self.sock.emit('subscribe', {'e': 'end'})

    def login(self, accessToken, walletAddress):
        self.sock.emit('user', {'e': 'login', 'addr': walletAddress, 'api': accessToken})
        self.sock.emit('user', {'e': 'wallet', 'addr': walletAddress, 'id': None})

    def logout(self):
        self.sock.emit('user', {'e': 'logout'})

    def start(self, duration):
        if duration == 0:
            self.sock.wait()
        else:
            self.sock.wait(duration)

if __name__ == "__main__":
    allbit = AllbitWatcher()

    # default
    # watch coin info update, price update

    # optional
    # to watch coin order_lsit_change, trade
    allbit.subscribe('ETH', 'BTC')

    # optional
    # to watch all of my address's event
    allbit.login(accessToken=ACCESS_TOKEN, walletAddress=ACCESS_TOKEN_WALLET_ADDRESS)

    allbit.start()