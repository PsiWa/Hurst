from valparser import ValParser

def main():
    while(True):
        vp = ValParser()
        for key,value in vp.currencies.items():
            print(f"{key} : {value}")
        id = int(input("ID валюты: "))
        year = int(input("год: "))
        period = int(input("период: "))
        pmax = int(input("pmax: "))
        vp.GetHistoricalExchange(id,year,period)
        vp.MakeExchanhePlot()
        vp.CalcHurst(pmax)


if __name__ == "__main__":
    main()