import sys
import requests
from bs4 import BeautifulSoup

headers = {"User Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

# gets current price of ticker
def getCurrentPrice(ticker):
    summary_url = 'https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker
    page = requests.get(summary_url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    div = soup.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})
    # time = soup.find(id="quote-market-notice").text
    
    if div is not None and len(div) > 0:
        price = div[0].find('span').text

        return float(price.replace(",", ""))
    else:
        return -1

# [open, high, low, close, adj close, volume]
# an index of 1 during after hours is the most recent days' statistics
def getPriceOfKthDayBefore(ticker, k):
    try:
        historical_url = 'https://finance.yahoo.com/quote/' + ticker + '/history?p=' + ticker
        page = requests.get(historical_url, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml')

        info = []
        # find all information of kth day before
        data = soup.find_all('td', {'class': 'Py(10px) Pstart(10px)'})
        for i in range(6):
            try:
                info.append(float(data[i + ((k - 1) * 6)].find('span').text.replace(",", "")))
            except:
                continue

        return info
    except:
        print("error")