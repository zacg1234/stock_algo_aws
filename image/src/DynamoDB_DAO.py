import boto3
from botocore.exceptions import ClientError
from User_Obj import User

from decimal import Decimal

class DynamoDB:
    def __init__(self):
        # Initialize a DynamoDB client
        self.db = boto3.resource('dynamodb', region_name='us-east-2')

    # Reading from the table
    def get_user(self, event, context, user_name):
        table = self.db.Table('Trade_Bot_Users')
        try:
            response = table.get_item(
                Key={
                    'Username': user_name
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response.get('Item', {})
            
        user = User(item["Username"], item["Cash"])
        user.asset_amount = item["AssetAmount"]
        user.asset_name = item["AssetName"]
        user.buy_threshold_index = item["BuyThresholdIndex"]
        user.initialized = item["Initialized"]
        user.last_touch_price = item["LastTouchPrice"]
        user.sell_threshold_index = item["SellThresholdIndex"]
        user.alpaca_end_point = item["AlpacaEndPoint"]
        user.alpaca_key = item["AlpacaKey"]
        user.alpaca_secret = item["AlpacaSecret"]

        return user

    # Writing to the table
    def put_user(self, event, context, user):
        table = self.db.Table('Trade_Bot_Users')
        try:
            table.put_item(
            Item={
                    'Username': user.name,
                    'AssetAmount': user.asset_amount,
                    'AssetName': user.asset_name,
                    'BuyThresholdIndex': user.buy_threshold_index,
                    'Cash': user.cash,
                    'Initialized': user.initialized,
                    'LastTouchPrice': user.last_touch_price,
                    'SellThresholdIndex': user.sell_threshold_index,
                    'AlpacaEndPoint': user.alpaca_end_point,
                    'AlpacaKey': user.alpaca_key,
                    'AlpacaSecret': user.alpaca_secret
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        # else:
        #     print("Write successful")
        # return {
        #     'statusCode': 200,
        # }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # or use str(obj) if you want to preserve exact precision
    raise TypeError




# if __name__ == "__main__":
#     # Test get_user function
#     dynamoDB = DynamoDB()
#     test_username = "zacg1234"
#     result = dynamoDB.get_user(None, None, test_username)
#     print(result.__dict__)
    # json_string = json.dumps(result['body'], indent=4, default=decimal_default)
    # print(json_string)

#     # user = User("zacg1234", 0)
#     # user.asset = "TSLA"
#     # user.asset_amount = Decimal(str(0.0))
#     # user.buy_threshold_index = 0
#     # user.last_touch_price = 0  
#     # user.sell_threshold_index = 0
#     # user.initialized = False
#     # put_user(None,None, user)
    
#     user = User("paper", 100000)
#     user.asset = "TSLA"
#     user.asset_amount = Decimal(str(0.0))
#     user.buy_threshold_index = 0
#     user.last_touch_price = 0  
#     user.sell_threshold_index = 0
#     user.initialized = False
#     user.alpaca_end_point = "https://paper-api.alpaca.markets"
#     user.alpaca_key = "PK403VGBTVGM48SQE7GK"
#     user.alpaca_secret = "n5EaA80zDKVa0wx99gf2KZ9NXrlekTNN49iZdWcJ"

#     print(put_user(None,None, user))