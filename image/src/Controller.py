import math

BUY_SIGNAL = 1
SELL_SIGNAL = -1
DECIMAL_PRECISION = 3

def get_user_net_worth(user, stock_price):
    return round((user.asset_amount * stock_price) + user.cash)

def cash_to_shares(cash_amount, stock_price):
    return round(cash_amount / stock_price)

def round(number):
    factor = 10 ** DECIMAL_PRECISION 
    return math.floor(number * factor) / factor

class Controller:

    # bot has a method getSignal that returns a trade signal
    # user is the data access object for the database of users
    # data is the inflow of market data - IN TESTING THE DATA MUST MATCH THE USER HELD ASSET
    def __init__(self, bot, user_obj, data, broker):
        self.bot = bot
        self.user_obj = user_obj
        self.data = data
        self.broker = broker

   
    def run_the_bot(self):

        # TODO:
        #self.broker.cancel_pending_orders()
    
        # User object with user data
        user = self.user_obj
        buy_sell_max_index = len(self.bot.buyThresholds) - 1
        ticker = user.asset_name

        ##  UPDATE USER PROFILE
        user.cash = self.broker.get_user_cash()
        user.asset_amount = self.broker.get_user_asset_qty(ticker)

        if not user.initialized:
            # Current share price - from 3rd party (not broker)
            share_price = self.data.get_current_price(ticker)
            if user.asset_amount <= 0:
                shares_to_buy = cash_to_shares(user.cash / 2, share_price)
                self.broker.place_market_order(ticker, shares_to_buy, BUY_SIGNAL)
            # A check to make sure that user was properly initialized
            else: 
                user.buy_threshold_index = int((buy_sell_max_index / 2))
                user.last_touch_price = share_price
                user.initialized = True

            # Upload the initialized user
            return (user, share_price)
                
        
        # Current share price - from broker
        share_price = round(self.broker.get_user_asset_price(ticker))
        # User net worth
        user_net_worth = get_user_net_worth(user, share_price)

        # Shares to buy or sell if there is a signal
        shares_to_buy_or_sell = cash_to_shares( user_net_worth * 0.1, share_price )
        signal = self.bot.get_signal(None, None, share_price, user.last_touch_price, user.buy_threshold_index, user.sell_threshold_index)
        
        if signal == BUY_SIGNAL :
            if user.cash >= shares_to_buy_or_sell * share_price: 
                # User has enough cash
                self.broker.place_market_order(ticker, shares_to_buy_or_sell, BUY_SIGNAL)
                user.last_touch_price = share_price

                user.sell_threshold_index = 0
                if user.buy_threshold_index < buy_sell_max_index:
                    user.buy_threshold_index = user.buy_threshold_index + 1

        elif signal == SELL_SIGNAL:
            if user.asset_amount >= shares_to_buy_or_sell: 
                # User has enough shares to sell
                self.broker.place_market_order(ticker, shares_to_buy_or_sell, SELL_SIGNAL)
                user.last_touch_price = share_price

                user.buy_threshold_index = 0
                if user.sell_threshold_index < buy_sell_max_index:
                    user.sell_threshold_index = user.sell_threshold_index + 1

        ## RETURN UPDATED USER
        return (user, share_price)