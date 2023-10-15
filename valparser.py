import requests
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import statistics
import numpy as np
import math

class ValParser:
    def __init__(self) -> None:
        self.currencies = dict()
        r = requests.get('https://val.ru/valhistory.asp?tool=1&bd=12&bm=10&by=2023')
        soup = BeautifulSoup(r.text.encode("cp1252"), 'html.parser')
        for option in soup.find("select", {'name' : 'tool'}).findAll("option"):
            self.currencies[int(option["value"])] = option.text
    
    def GetHistoricalExchange(self,currency_id, year, period):
        r = requests.get(f'https://val.ru/valhistory.asp?tool={currency_id}&bd=1&bm=1&by={year}&ed=1&em=1&ey={year+period}&showchartp=False')
        webbrowser.open(f'https://val.ru/valhistory.asp?tool={currency_id}&bd=1&bm=1&by={year}&ed=1&em=1&ey={year+1}&showchartp=False')

        soup = BeautifulSoup(r.text.encode("cp1252"), 'html.parser')
        self.exchange = dict()
        for row in soup.find('div',{'class':'gfcont'}).findAll("tr"):
            cols = row.findAll('td')
            self.exchange[datetime.strptime(cols[0].text, '%d.%m.%Y')] = float(cols[2].text)
        self.exchange = dict(sorted(self.exchange.items()))
        self.exchangedf = pd.DataFrame(self.exchange.values(), index = self.exchange.keys())
        self.exchangedf.Name = self.currencies[currency_id]

    def MakeExchanhePlot(self):
        plt.figure(1)
        plt.plot(self.exchangedf, label=self.exchangedf.Name)
        plt.legend()

    def CalcHurst(self,pmax):
        dX = list()
        exchangelist = list(self.exchange.values())
        for p in range(pmax):
            dXp = list()
            for i in range((len(exchangelist)-pmax)):
                dXp.append(exchangelist[i+p]-exchangelist[i])
            dX.append(dXp)
        
        lnSTDp = list()
        for dxp in dX[1:]:
            STDp = statistics.stdev(dxp)
            lnSTDp.append(math.log(STDp))
        lnSTDp = np.vstack(lnSTDp)

        nums = list()
        for k in range(1,len(dX)):
            nums.append(math.log(k))
        nums = np.vstack(nums)

        A = np.vstack([nums.T, np.ones(len(nums))]).T
        m, c = np.linalg.lstsq(A, lnSTDp, rcond=None)[0]
        print(f"Показатель Хёрста: {float(m)}")
        plt.figure(2)
        plt.plot(nums, lnSTDp, 'o', label='Данные', markersize=10)
        plt.plot(nums, m * nums + c, 'r', label='Аппроксимация')
        plt.legend()
        plt.show()


