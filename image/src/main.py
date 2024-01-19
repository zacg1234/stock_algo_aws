from Decision_Bot import Bot
from RealTimeData import RealTimeData
from DynamoDB_DAO import DynamoDB
from Controller import Controller
from Alpaca_DAO import Alpaca_DAO

def handler(event, context):
    buyThresholds = [-0.5, -0.5, -1, -1, -1, -1.5, -2, -3] # length = 8
    sellThresholds = [1, 1, 1, 1, 1, 1.5, 2, 3] # length = 8

    bot = Bot(buyThresholds, sellThresholds)
    data = RealTimeData()
    dynamoDB = DynamoDB()


    isPaper = True

    user_name = "paper" if isPaper else "zacg1234"

    user = dynamoDB.get_user(None, None, user_name)
    alpaca_DAO = Alpaca_DAO(user.alpaca_key, user.alpaca_secret, user.alpaca_end_point, isPaper)
    
    controller = Controller(bot, user, data, alpaca_DAO)

    # run_the_bot returns the updated user
    (user, price) = controller.run_the_bot()
    

    dynamoDB.put_user(None, None, user)

    return {"statusCode" : 200, 
            "body" : 
                { 
                    "current_asset_price" : price,
                    "name" : user.name, 
                    "cash" : user.cash, 
                    "asset_name" : user.asset_name,
                    "asset_amount" : user.asset_amount,
                    "current_buy_index" : user.buy_threshold_index,
                    "current_sell_index" : user.sell_threshold_index,
                    "last_touch_price" : user.last_touch_price,
                    "initialized" : user.initialized
                }
            } 


if __name__ == "__main__":
    print("******************* RUN BOT ********************")
    handler()
    #time.sleep(10)#300)  # Sleep for 300 seconds (5 minutes)
   