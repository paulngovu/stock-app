from django.shortcuts import render
from .models import Company
import requests                     # for calling API
import ast                          # for turning str into list

# ==============================================================================
# VIEWS
# ==============================================================================

def viewDashboard(request):
    # Get all saved companies
    companies = Company.objects.all()

    errormsg = "You are not watching any companies" if not companies else ""

    context = {
        "title": "Dashboard",
        "companies": companies,
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
    if request.method == "POST":
        company = ast.literal_eval(request.POST.get("company"))
        print(company)
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
    return r.json()

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
