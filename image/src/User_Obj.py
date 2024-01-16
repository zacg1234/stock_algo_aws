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

    def print_self(self):
        print(f"NAME: {self.name}")
        print(f"    CASH: {self.cash}")
        print(f"    ASSET NAME: {self.asset_name}, AMOUNT: {self.asset_amount}")
        print(f"    BUY INDEX: {self.buy_threshold_index}")
        print(f"    SELL INDEX: {self.sell_threshold_index}")
        print(f"    LAST TOUCH PRICE: {self.last_touch_price}")
        print(f"        INITIALIZED ? : {self.initialized}")