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
    # user = controller.run_the_bot()
    # print(user.cash)
    # dynamoDB.put_user(None, None, user)
    return {"statusCode" : 200, "body" : "Run complete", "user cash" : user.cash} 

if __name__ == "__main__":
    handler()