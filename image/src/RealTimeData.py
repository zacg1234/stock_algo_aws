import requests


class RealTimeData:

    def __init__(self) -> None:
        self.url = "https://real-time-finance-data.p.rapidapi.com/stock-quote"


    def get_current_price(self, ticker):
        querystring = {"symbol":f"{ticker}:NASDAQ","language":"en"}

        headers = {
            "X-RapidAPI-Key": "d4793386efmsh95311b7170fe13bp190c9ajsn4dab09858a8e",
            "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
        }

        response = requests.get(self.url, headers=headers, params=querystring)
        response_json = response.json()
        if response_json["status"] == "OK":
            response_data = response_json["data"]
            return response_data["price"]
        return -1


if __name__ == "__main__":
    # Test get_user function
    data_dao = RealTimeData()
    print(data_dao.get_current_price("AAPL"))


