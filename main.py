# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import os
import binance
import pandas as pd
from tqdm import tqdm
from binance.client import Client
apiKey = os.environ.get('binance_api')
secret = os.environ.get('binance_secret')
client = Client(apiKey, secret)
info = client.get_exchange_info()

symbols = [x['symbol'] for x in info['symbols']]

exclude = ['UP', 'DOWN', 'BEAR', 'BULL']
non_lev = [symbol for symbol in symbols if all(exclude not in symbol for exclude in exclude)]
relevant = [symbol for symbol in non_lev if symbol.endswith('USDT')]
klines={}

for symbol in tqdm(relevant):
    klines[symbol] = client.get_historical_klines(symbol, '1m', '1 hour ago UTC')


returns, symbols = [], []

for symbol in relevant:
    if len(klines[symbol]) > 0:
        cumret = (pd.DataFrame(klines[symbol])[4].astype(float).pct_change()+1).prod()-1

        returns.append(cumret)
        symbols.append(symbol)


retdf = pd.DataFrame(returns, index=symbols, columns=['ret'])

print(retdf.ret.nlargest(10))





