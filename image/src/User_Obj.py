class User:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.asset_name = None
        self.asset_amount = 0
        self.buy_threshold_index = 0
        self.last_touch_price = 0  # the last time the stock was bought or sold
        self.sell_threshold_index = 0
        self.alpaca_end_point = ""
        self.alpaca_key = ""
        self.alpaca_secret = ""
        self.initialized = False