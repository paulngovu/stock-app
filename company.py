import requests

# ==============================================================================

class Company:
    ############################################################################
    #
    #   Company class with candlestick data
    #
    #   DATA MEMBERS:
    #       - symbol: Company symbol
    #       - candlesticks: List of candlestick data
    #
    #   METHODS:
    #       - addCandlestick() -> None: adds candlestick data to Company
    #           candlesticks
    #
    ############################################################################

    class Candlestick:
        ########################################################################
        #
        #   Candlestick class to record daily prices.
        #
        #   DATA MEMBERS:
        #       - date: date
        #       - open: opening price
        #       - high: high price
        #       - low: low price
        #       - close: closing price
        #       - volume: volume
        #
        #   METHODS:
        #       - __str__() -> str: get all candlestick data with print()
        #       - getYear() -> str: returns year
        #       - getMonth() -> str: returns month
        #       - getDay() -> str: returns day
        #
        ########################################################################

        def __init__(self, date: str, open: str, high: str, low: str, close: str, volume: str):
            self.date = date
            self.open = open
            self.high = high
            self.low = low
            self.close = close
            self.volume = volume

        def __str__(self) -> str:
            # Print Candlestick data directly
            return "Date: {}\nOpen: {}\nHigh: {}\nLow: {}\nClose: {}\nVolume: {}"\
                    .format(self.date, self.open, self.high, self.low, self.close, self.volume)

        def getYear(self) -> str:
            return self.date[:4]

        def getMonth(self) -> str:
            return self.date[5:7]

        def getDay(self) -> str:
            return self.date[-2:]


    def __init__(self, symbol: str):
        self.symbol = symbol
        self.candlesticks = []

    def addCandlestick(self, date: str, open: str, high: str, low: str, close: str, volume: str) -> None:
        self.candlesticks.append(self.Candlestick(date, open, high, low, close, volume))

# ==============================================================================

# Create a new company with complete Candlestick data
def createCompany(symbol: str, function: str, apiKey: str) -> Company:
    company = Company(symbol)
    payload = {"function": function, "symbol": symbol, "apikey": apiKey}
    r = requests.get("https://www.alphavantage.co/query", params=payload)
    data = r.json()
    for date, prices in data["Time Series (Daily)"].items():
        vals = []
        for type, val in prices.items():
            # print("{}, {}".format(type, val))
            vals.append(val)
        company.addCandlestick(date, vals[0], vals[1], vals[2], vals[3], vals[4])
    return company

def main():
    apiKey = "MXZJD1EMBPG49Y9U"

    companies = []
    companies.append(createCompany("AAPL", "TIME_SERIES_DAILY", apiKey))
    companies.append(createCompany("GOOG", "TIME_SERIES_DAILY", apiKey))

    for company in companies:
        for c in company.candlesticks:
            print(repr(c))
            print(company.symbol)
            print(c)
            print("===")

if __name__ == "__main__":
    main()
