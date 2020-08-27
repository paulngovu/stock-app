from django.shortcuts import render
from .models import Company
import requests                     # for calling API
import ast                          # for turning str into list

# ==============================================================================
# VIEWS
# ==============================================================================

def viewDashboard(request):
    # Remove a company from watchlist
    if request.method == "POST":
        deleteCompany(request.POST.get("companyName"))

    # Get all saved companies
    companies = Company.objects.all()

    # Create list of companies with name, symbol, recommendation
    companiesList = []
    for company in companies:
        # Add dictionary to list
        companiesList.append({  "name": company.name,
                                "symbol": company.symbol,
                                "recommendation": getRecommendation(company)})
    # companiesList.sort(key = lambda x: x["name"])

    errormsg = "You are not watching any companies" if not companies else ""

    context = {
        "title": "Dashboard",
        "companies": companiesList,
        "errormsg": errormsg,
    }
    return render(request, 'dashboard.html', context)

def viewSearch(request):
    context = {
        "title": "Company Search",
    }
    return render(request, 'search.html', context)

def viewSearchResults(request):
    keyword = request.GET.get("search")
    errormsg = "No results found"
    if keyword:
        companies = searchCompanies(keyword)["bestMatches"]
        errormsg = ""

    # Create list of lists to send
    companiesList = []
    if keyword:
        for company in companies:
            companiesList.append([company["1. symbol"], company["2. name"]])

    context = {
        "title": "Company Search Results",
        "companies": companiesList,
        "errormsg": errormsg,
    }
    return render(request, 'search_results.html', context)

def viewCompanies(request):
    # Add company to watchlist
    if request.method == "POST":
        # req comes back as string, convert to list
        company = ast.literal_eval(request.POST.get("company"))
        # print(company)
        if company[1] not in [company.name for company in Company.objects.all()]:
            addCompany(company[1], company[0])

    companies = Company.objects.all()

    context = {
        "title": "Followed Companies",
        "companies": companies,
    }
    return render(request, 'companies.html', context)



# ==============================================================================
# Other functions because i couldn't figure out how to split files
# ==============================================================================

def getPrices(symbol):
    """
    Call daily price of specified company

    symbol: str
    return value: dict
    """

    function = "TIME_SERIES_DAILY"
    sym = symbol
    apiKey = "MXZJD1EMBPG49Y9U"
    payload = {"function": function, "symbol": sym, "apikey": apiKey}
    url = "https://www.alphavantage.co/query"

    r = requests.get(url, params=payload)
    return r.json() if r.status_code == 200 else None

def searchCompanies(keywords):
    """
    Search for companies based on keywords

    keywords: str
    return value: list
    """

    function = "SYMBOL_SEARCH"
    kw = keywords
    apiKey = "MXZJD1EMBPG49Y9U"
    payload = {"function": function, "keywords": kw, "apikey": apiKey}
    url = "https://www.alphavantage.co/query"

    r = requests.get(url, params=payload)
    return r.json()

def addCompany(name, symbol):
    """
    Add company to watch for in Django database

    name: str
    symbol: str
    return value: None
    """

    c = Company(name=name, symbol=symbol)
    c.save()

def deleteCompany(name):
    """
    Delete company from Django database

    name: str
    return value: None
    """

    c = Company.objects.filter(name=name)
    if c:
        c.delete()

def getRecommendation(company):
    """
    Searches prices of company, return recommendation

    company: Company obj
    return value: str
    """

    prices = getPrices(company.symbol)
    if not prices:
        return "NO DATA"

    # Get 3 most recent days
    firstThreeDays = []
    index = 0
    for price in prices['Time Series (Daily)'].values():
        if index >= 3:
            break
        firstThreeDays.append(price)
        index += 1
    # print(firstThreeDays)

    res = "HOLD"
    # Consider action if volume of most recent day exceeds 10% of oldest day
    if int(firstThreeDays[0]['5. volume']) * 1.1 >= int(firstThreeDays[2]['5. volume']):
        # If price goes up, everyone is buying
        if float(firstThreeDays[2]['4. close']) - float(firstThreeDays[0]['4. close']) > 0:
            res = "BUY"
        # If price goes down, everyone is selling
        else:
            res = "SELL"

    return res
