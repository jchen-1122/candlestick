import statistics
import json

### HELPER FUNCTIONS
# candlestick [low, open, close, high]
def isHammer(ticker, short=0.015, num_sds=2, handleLen=5):
    with open('../data/historical.json') as f:
        data = json.load(f)
    
    info = data[ticker][0]
    sma, sd = getMovingAverage(data[ticker])
    low = info[2]
    dayOpen = info[0]
    dayClose = info[3]
    high = info[1]

    # negative = red, positive = green
    candle = dayClose - dayOpen
    print(dayClose, dayOpen)

    # how long are the high and lows
    lowlen = min([dayOpen, dayClose]) - low
    highlen = high - max([dayClose, dayOpen])

    # store conditions
    conditions = []
    conditions.append(low < (sma - (num_sds * sd))) 
    conditions.append(candle >= 0) 
    conditions.append(candle <= (short * dayClose))
    conditions.append(((lowlen > (handleLen * abs(candle))) or ((highlen >  (handleLen * abs(candle))))))

    # hammer if low is lower than 2 * sd + sma
    # and green and short box candle 
    if (all(conditions)):
        return {"ticker": ticker, 
                "isHammer": True,
                "closeHammer": False,
                "handle (low)": (lowlen / abs(candle)),
                "handle (high)": (highlen / abs(candle)),
                "price": dayClose, 
                "candle": candle, 
                "lowerBB": sma - (num_sds * sd), 
                "upperBB": sma + (num_sds * sd)
                }
    elif (kTrue(conditions, 3)):
        return {"ticker": ticker, 
                "isHammer": False, 
                "closeHammer": False,
                "handle (low)": (lowlen / abs(candle)),
                "handle (high)": (highlen / abs(candle)),
                "price": dayClose, 
                "candle": candle, 
                "lowerBB": sma - (num_sds * sd), 
                "upperBB": sma + (num_sds * sd)
                }
    else:
        return {"ticker": ticker, 
                "isHammer": False, 
                "closeHammer": False,
                "handle (low)": (lowlen / abs(candle)),
                "handle (high)": (highlen / abs(candle)),
                "price": dayClose, 
                "candle": candle, 
                "lowerBB": sma - (num_sds * sd), 
                "upperBB": sma + (num_sds * sd)
                }

def engulfing(ticker):
    with open('../data/historical.json') as f:
        data = json.load(f)
    
    info = data[ticker][0]
    sma, sd = getMovingAverage(data[ticker])
    low = info[2]
    dayOpen = info[0]
    dayClose = info[3]
    high = info[1]

    # check for three day downtrend
    downtrend = data[ticker][3][3] > data[ticker][2][3] and data[ticker][2][3] > data[ticker][1][3]
    engulfing = min(dayClose, dayOpen) < min(data[ticker][1][0], data[ticker][1][3]) and max(dayClose, dayOpen) > max(data[ticker][1][0], data[ticker][1][3])

    # make sure yesterday's candle is red
    return downtrend and engulfing and (dayClose > dayOpen) and (dayClose < sma + sd) and (data[ticker][1][0] > data[ticker][1][3])

def piercingLine(ticker, thickness=0.015):
    with open('../data/historical.json') as f:
        data = json.load(f)
    
    info = data[ticker][0]
    sma, sd = getMovingAverage(data[ticker])
    low = info[2]
    dayOpen = info[0]
    dayClose = info[3]
    high = info[1]

    # check for three day downtrend
    downtrend = data[ticker][3][3] > data[ticker][2][3] and data[ticker][2][3] > data[ticker][1][3]
    
    prevBigRed = (data[ticker][1][3] < data[ticker][1][0]) and (data[ticker][1][0] - data[ticker][1][3] > thickness * dayClose)
    todayCover = (dayOpen < dayClose) and (dayClose > ((data[ticker][1][0] + data[ticker][1][3]) / 2))

    piercingLine = downtrend and prevBigRed and todayCover
    return piercingLine

def threeLineStrikeBearish(ticker):
    with open('../data/historical.json') as f:
        data = json.load(f)
    
    info = data[ticker][0]
    sma, sd = getMovingAverage(data[ticker])
    low = info[2]
    dayOpen = info[0]
    dayClose = info[3]
    high = info[1]

    # three day strict downtrend (close lower than previous low and high is lower than previous open)
    # see https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp#citation-3
    # or page 757 of encyclopedia
    allThreeRed = (data[ticker][3][3] < data[ticker][3][0]) and (data[ticker][2][3] < data[ticker][2][0]) and (data[ticker][1][3] < data[ticker][1][0])
    # 4dayopen > 3dayhigh and 4dayclose > 3dayclose and 3dayopen > 2dayhigh and 3dayclose > 2dayclose
    downtrend = (data[ticker][3][0] > data[ticker][2][1]) and (data[ticker][3][3] > data[ticker][2][3]) and (data[ticker][2][0] > data[ticker][1][1]) and (data[ticker][2][3] > data[ticker][1][3])
    # dayOpen < dayClose (green) and dayClose > 4dayopen and dayOpen < 2dayclose
    engulfing = (dayOpen < dayClose) and (dayClose > data[ticker][3][0]) and (dayOpen < data[ticker][1][3])
    return allThreeRed and downtrend and engulfing

### UTILS
# k number of days (usually 20)
def getMovingAverage(tickerData):    
    closes = [x[3] for x in tickerData]
    return statistics.mean(closes), statistics.pstdev(closes)

# helper function
def kTrue(arr, k):
    count = 0
    for i in arr:
        if i:
            count += 1
    return count >= k

### MAIN SCRIPTS
def findHammer():
    with open('../tickers/input/sp500.json') as f:
        data = json.load(f)

    res = {}
    for ticker in data.keys():
        try:
            currObj = isHammer(ticker)
            print(currObj)
            if (currObj["isHammer"]):
                res[ticker] = (True, currObj)
            elif (currObj["closeHammer"]):
                res[ticker] = (False, currObj)
        except Exception as e:
            print(e)
            print({"network_error": True})
    with open('../tickers/output/watchlist.json', 'w') as f:
        json.dump(res, f)

def findEngulfing():
    with open('../tickers/input/sp500.json') as f:
        data = json.load(f)
    res = {}

    for ticker in data.keys():
        try:
            isDown = engulfing(ticker)
            print(ticker + ": " + str(isDown))
            if isDown:
                res[ticker] = True
        except:
            print("Error")
    with open('../tickers/output/watchlist.json', 'w') as f:
        json.dump(res, f)

# historically and statistically insignificant (also not written well)
def findPiercingLine():
    with open('../tickers/input/sp500.json') as f:
        data = json.load(f)
    res = {}

    for ticker in data.keys():
        try:
            isPiercing = piercingLine(ticker)
            print(ticker + ": " + str(isPiercing))
            if isPiercing:
                res[ticker] = True
        except:
            print("Error")
    with open('../tickers/output/watchlist.json', 'w') as f:
        json.dump(res, f)

def findThreeStrikeLineBearish():
    with open('../tickers/input/sp500.json') as f:
        data = json.load(f)
    res = {}

    for ticker in data.keys():
        try:
            isThreeStrike = threeLineStrikeBearish(ticker)
            print(ticker + ": " + str(isThreeStrike))
            if isThreeStrike:
                res[ticker] = True
        except:
            print("Error")
    with open('../tickers/output/watchlist.json', 'w') as f:
        json.dump(res, f)

# run
findHammer()