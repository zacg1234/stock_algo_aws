from decimal import Decimal, getcontext, ROUND_FLOOR

BUY_SIGNAL = 1
SELL_SIGNAL = -1
DECIMAL_PRECISION = 3

class Controller:

    @staticmethod
    def user_net_worth(user, stock_price):
        return Decimal((user.asset_amount * stock_price) + user.cash)
    
    @staticmethod
    def cash_to_shares(cash_amount, stock_price):
        return Decimal(Decimal(cash_amount) / Decimal(stock_price))

    # bot has a method getSignal that returns a trade signal
    # users is the data access object for the database of users
    #   data is the inflow of market data - IN TESTING THE DATA MUST MATCH THE USER HELD ASSET
    def __init__(self, bot, user_obj, data, broker):
        self.bot = bot
        self.user_obj = user_obj
        self.data = data
        self.broker = broker

   
    def run_the_bot(self):

        getcontext().prec = DECIMAL_PRECISION
        getcontext().rounding = ROUND_FLOOR
    
        # User object with user data
        user = self.user_obj
        buy_sell_max_index = len(self.bot.buyThresholds) - 1
        ticker = user.asset_name

        asset_qty = Decimal(self.broker.get_user_asset_qty(ticker))

        if not user.initialized:
            # Current share price - from 3rd party (not broker)
            share_price = Decimal(self.data.get_current_price(ticker))
            if asset_qty <= 0:
                shares_to_buy = Controller.cash_to_shares(user.cash / 2, share_price)
                self.broker.place_market_order(ticker, shares_to_buy, BUY_SIGNAL)
            else: # A check to make sure that user was properly initialized
                user.asset_amount = asset_qty
                user.buy_threshold_index = int((buy_sell_max_index / 2))
                user.initialized = True
                user.last_touch_price = share_price
            return user
        
        # Current share price - from broker
        share_price = Decimal(self.broker.get_user_asset_price(ticker))

        ##  UPDATE USER PROFILE
        user.cash = Decimal(self.broker.get_user_cash())
        user.asset_amount = asset_qty
        # User net worth
        user_net_worth = Controller.user_net_worth(user, share_price)

        # Shares to buy or sell if there is a signal
        shares_to_buy_or_sell = Controller.cash_to_shares( Decimal(user_net_worth * 0.1), share_price )
        signal = self.bot.get_signal(None, None, share_price, user.last_touch_price, user.buy_threshold_index, user.sell_threshold_index)
        
        if signal == BUY_SIGNAL :
            if user.cash >= shares_to_buy_or_sell * share_price: 
                # User has enough cash
                self.broker.place_market_order(self, ticker, shares_to_buy_or_sell, BUY_SIGNAL)
                user.last_touch_price = share_price

                user.sell_threshold_index = 0
                if user.buy_threshold_index < buy_sell_max_index:
                    user.buy_threshold_index = user.buy_threshold_index + 1

        elif signal == SELL_SIGNAL:
            if user.asset_amount >= shares_to_buy_or_sell: 
                # User has enough shares to sell
                self.broker.place_market_order(self, ticker, shares_to_buy_or_sell, SELL_SIGNAL)
                user.last_touch_price = share_price

                user.buy_threshold_index = 0
                if user.sell_threshold_index < buy_sell_max_index:
                    user.sell_threshold_index = user.sell_threshold_index + 1


        # user.cash = self.broker.get_user_cash()
        # asset_qty = self.broker.get_user_asset_qty(ticker)
        ## RETURN UPDATED USER
        return user


# @staticmethod
# def investment_quantity(user, stock_price):
#     return Controller.user_net_worth(user, stock_price) / 10 

# def sell_shares(self, user, shares_to_sell, share_price):
#     if user.asset_amount > shares_to_sell: 
#         # User has enough shares to sell
#         user.last_touch_price = share_price
#         self.user_dao.increment_sell_threshold_index(user.name)
#         return True #success
#     return False #failure

# def buy_shares(self, user, shares_to_buy, share_price):
#     required_cash = shares_to_buy * share_price
#     user_cash = self.user_dao.get_cash(user.name, required_cash)
#     if user_cash > 0: #user has enough cash
#         self.user_dao.add_asset(user.name, user.asset_name, shares_to_buy)
#         user.last_touch_price = share_price
#         if user.initialized:
#             self.user_dao.increment_buy_threshold_index(user.name)
#         return True #success
#     return False #failure
    