from django.shortcuts import render
import requests

def dashboard(request):
    # make API call
    function = "TIME_SERIES_DAILY"
    symbol = "GOOG"
    apiKey = "MXZJD1EMBPG49Y9U"
    payload = {"function": function, "symbol": symbol, "apikey": apiKey}
    url = "https://www.alphavantage.co/query"

    r = requests.get(url, params=payload)
    data = r.json()

    # dailyPrices = []
    # for date, prices in data["Time Series (Daily)"].items():
    #     dailyPrice = [date]
    #     for type, price in prices.items():
    #         dailyPrice.append(price)
    #     dailyPrices.append(dailyPrice)
    # for i in dailyPrices:
    #     print(i)

    dailyPrices = data["Time Series (Daily)"]
    # print(dailyPrices)

    context = {
        "symbol": symbol,
        "dailyPrices": dailyPrices,
    }
    return render(request, 'dashboard.html', context)
