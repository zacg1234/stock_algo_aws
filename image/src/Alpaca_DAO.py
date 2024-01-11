from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

BUY_SIGNAL = 1
SELL_SIGNAL = -1

class Alpaca_DAO:

    def __init__(self, api_key, secret_key, endpoint, isPaper):
        #### Might not be needed ######
        self.api_key = api_key       ##
        self.secret_key = secret_key ## 
        self.endpoint = endpoint     ##
        ###############################

        self.trading_client = TradingClient(api_key, secret_key, paper=isPaper)
        self.account = self.trading_client.get_account()
        
        

    def place_market_order(self, ticker, number_of_shares, buy_or_sell):
        buy_or_sell_side = OrderSide.BUY if buy_or_sell == BUY_SIGNAL else OrderSide.SELL
        # preparing orders
        market_order_data = MarketOrderRequest(
                            symbol = f"{ticker}",
                            qty = number_of_shares,
                            side = buy_or_sell_side,
                            time_in_force = TimeInForce.DAY
                            )

        # Market order
        market_order = self.trading_client.submit_order(
                        order_data=market_order_data
                    )
        # Return filled quanity - order is never instantly filled (return 0)
        # return market_order.filled_qty
        
    def get_user_net_worth(self):
        return float(self.account.equity)
    
    def get_user_cash(self):
        return float(self.account.cash)
    
    def get_user_asset_qty(self, ticker):
        positions = self.trading_client.get_all_positions()
        for position in positions:
            #print(position.current_price)
            if position.symbol == ticker:
                return float(position.qty)
        return -1
            
    def get_user_asset_price(self, ticker):
        positions = self.trading_client.get_all_positions()
        for position in positions:
            #print(position.current_price)
            if position.symbol == ticker:
                return float(position.current_price)
        return -1


### API keys and endpoints can be found in users: paper and zacg1234 respectively

if __name__ == "__main__":
    alpaca_DAO = Alpaca_DAO("PKBBMR9398054464GH1G", "qM1KwggH5ePUx5j3vo0Sfah58sykaGlTHLBopdK7", "https://paper-api.alpaca.markets", True)
    # net_worth = alpaca_DAO.get_user_net_worth()
    # print(net_worth)
    #print(f'Market order filled: {alpaca_DAO.place_market_order("TSLA", 1.2, BUY_SIGNAL)}')
    # print(f'User asset qty: {alpaca_DAO.get_user_asset_qty("TSLA")}')
    # print(f'Asset price: {alpaca_DAO.get_user_asset_price("TSLA")}')
    # print(alpaca_DAO.get_user_cash())
    # print(alpaca_DAO.get_user_net_worth())