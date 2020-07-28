from django.shortcuts import render
from .models import Company
import requests

# VIEWS ========================================================================

def dashboard(request):
    # make API call
    symbol= "GOOG"  # TODO
    data = getPrices(symbol)

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
        "title": "Dashboard",
        "symbol": symbol,
        "dailyPrices": dailyPrices,
    }
    return render(request, 'dashboard.html', context)

def companies(request):
    companies = Company.objects.all()

    context = {
        "title": "Followed Companies",
        "companies": companies,
    }
    return render(request, 'companies.html', context)



# Other functions because i couldn't figure out how to split files =============

def getPrices(symbol_):
    """
    Calls daily price of specified company and returns JSON dictionary

    symbol_: str
    return value: dict
    """

    function = "TIME_SERIES_DAILY"
    symbol = symbol_
    apiKey = "MXZJD1EMBPG49Y9U"
    payload = {"function": function, "symbol": symbol, "apikey": apiKey}
    url = "https://www.alphavantage.co/query"

    r = requests.get(url, params=payload)
    return r.json()

def addCompany(name_, symbol_):
    """
    Add company to watch for in Django database

    name_: str
    symbol_: str
    return value: None
    """

    c = Company(name=name_, symbol=symbol_)
    c.save()
