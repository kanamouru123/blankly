from blankly.exchanges.auth.auth_constructor import AuthConstructor
from blankly.exchanges.futures.futures_exchange import FuturesExchange
from blankly.exchanges.interfaces.ftx.ftx_api import FTXAPI
from blankly.exchanges.interfaces.ftx_futures.ftx_futures_interface import FTXFuturesInterface
from blankly.exchanges.interfaces.futures_exchange_interface import FuturesExchangeInterface


class FTXFutures(FuturesExchange):
    def __init__(self,
                 portfolio_name=None,
                 keys_path="keys.json",
                 preferences_path=None):
        super().__init__("ftx_futures", portfolio_name, preferences_path)

        # Load auth from keys file
        auth = AuthConstructor(keys_path, portfolio_name, 'ftx', ['API_KEY', 'API_SECRET', 'sandbox'])

        if auth.keys['sandbox']:
            raise NotImplementedError('FTX Futures exchange does not support sandbox mode')

        # TODO when FTX tld-fix pull request is merged, this needs to be updated too
        self.__calls = FTXAPI(auth.keys['API_KEY'], auth.keys['API_SECRET'])

        self.__interface = FTXFuturesInterface(self.exchange_type, self.calls)

        self.initialize()

    @property
    def calls(self):
        return self.__calls

    @property
    def interface(self) -> FuturesExchangeInterface:
        return self.__interface

