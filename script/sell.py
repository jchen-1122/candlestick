import statistics
import json

def sellTickers():
    with open('../data/historical.json') as f:
        data = json.load(f)
    
    with open('portfolio.json') as f:
        portfolio = json.load(f)

    tickersToSell = []
    for ticker in portfolio.keys():
        # today’s close is lower than yesterday’s low
        # today’s close crosses 20 day simple moving average
        print(ticker)
        sma, sd = getMovingAverage(data[ticker])
        if data[ticker][0][3] < data[ticker][1][2] or data[ticker][0][3] >= (sma + sd):
            tickersToSell.append(ticker)
            portfolio[ticker] = -1  

    with open('portfolio.json', 'w') as f:
        json.dump(portfolio, f)
    
    return tickersToSell

def getMovingAverage(tickerData):    
    closes = [x[3] for x in tickerData]
    return statistics.mean(closes), statistics.pstdev(closes)

print(sellTickers())