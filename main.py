import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client
import math
import datetime as dt

load_dotenv("codes.env")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# stock api
av_api_key = os.getenv("AV_API_KEY")
# articles api
news_api_key = os.getenv("NEWS_API_KEY")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# twilio
account_sid= os.getenv("ACCOUNT_SID")
auth_token= os.getenv("AUTH_TOKEN")


# 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "datatype": "json",
    "apikey":av_api_key,

}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in stock_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
# print(yesterday_closing_stock_price)

# 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
# print(day_before_yesterday_closing_stock_price)

# 3. - Find the positive difference between 1 and 2. e.g., 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
stock_price_difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if stock_price_difference > 0 :
    up_down = "🔺"
else:
    up_down = "🔻"
# 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
stock_price_percentage_difference = round((stock_price_difference / yesterday_closing_price)* 100,2)
print(stock_price_percentage_difference)

# 5. - If TODO4 percentage is greater than 5 then print("Get News").
now = dt.datetime.now()
today = now.today()
news_params = {
    "q": COMPANY_NAME,
    "language": "en",
    "from": "2026-04-01",
    "to":f"2026-04-0{today}",
    "apiKey": news_api_key,
}
if abs(stock_price_percentage_difference) > 5:
# 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
# 7. - Use Python slice operator to create a list that contains the first 3 articles. 
    three_articles = articles[:3]
# 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{stock_price_percentage_difference}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
# 9. - Send each article as a separate message via Twilio. 
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
        messaging_service_sid="MGcc344b21de6d7ca6d6421decb7393f45",
        body= article,
        to="+27618580714"
    )
