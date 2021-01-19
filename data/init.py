import sys
import collections
import json
from scraper import getCurrentPrice, getPriceOfKthDayBefore

# daily
def init():
    with open('historical.json') as f:
        data = json.load(f)

    # replace 21st data with most recent data
    for ticker in data.items():
        try:
            today = getPriceOfKthDayBefore(ticker[0], 1)
            print(str(ticker[0]) + ": " + str(today))
            data[ticker[0]].insert(0, today)
            data[ticker[0]].pop()
        except:
            continue

    with open('historical.json', 'w') as f:
        json.dump(data, f)

# one time (reset) for large files
def reset(file):
    # get tickers
    with open(file + '.json') as f:
        tickers = json.load(f)

    # get historical file contents
    with open('historical.json') as f:
        historical = json.load(f)
    
    # loop through tickers and put into json from most recent (index = 0) to 20th day (index = 19)
    # {"ticker" : [{open, high, low, close, adj close, volume}, {}, ..., {}], ...}
    for ticker in tickers.items():
        tickerData = []
        print("Requesting 20 day data for " + ticker[0])
        for i in range(1, 21):
            tickerData.append(getPriceOfKthDayBefore(ticker[0], i))
        historical[ticker[0]] = tickerData
    
    with open('historical.json', 'w') as f:
        json.dump(historical, f)

init()