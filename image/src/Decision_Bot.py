
SKIP_SELL_SIGNAL = -2
SELL_SIGNAL = -1
BUY_SIGNAL = 1
SKIP_BUY_SIGNAL = 2
    
class Bot:
    def __init__(self, buyThresholds, sellThresholds ): # constructor
        self.buyThresholds = buyThresholds
        self.sellThresholds = sellThresholds

    #
    #  TODO: add engulfing candle differentiation 
    # 
    def get_signal (self, prev_open_price, open_price, close_price, last_touch_price, buy_threshold_index, sell_threshold_index) :
        percent_change = 100 * (close_price - last_touch_price)/last_touch_price

        if(close_price - last_touch_price > 0) : # Stock moving higher
            # engulfing candle 
            # if prev_open_price < close_price: 
            #     return 0
            if( percent_change > self.sellThresholds[sell_threshold_index]) :
                return SELL_SIGNAL
            
        elif (close_price - last_touch_price < 0): # Stock moving lower 
            # engulfing candle 
            # if prev_open_price > close_price: 
            #     return 0
            if(percent_change < self.buyThresholds[buy_threshold_index]) :
                return BUY_SIGNAL
            
        return 0