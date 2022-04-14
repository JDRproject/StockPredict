from html.entities import html5
from db import DB
from urllib.request import Request, urlopen
from datetime import datetime
from bs4 import BeautifulSoup
import json
import pandas as pd 
from pandas import DataFrame, json_normalize


class Exchange :

    API_KEY = "vPK2uOdoutAUb0ZhGwgDYJdIP9Bp1Wlw"
    API_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={}&searchdate={}&data=AP0{}"

    def __init__(self) -> None:
        pass

    def update(self) :
        db = DB()
        stock = db.getDate("sise", "where code = 5930")
        stock = stock.sort_values(by='date', ascending=False)
        exchange = db.getDate("exchange", "where cur_unit = \"USD\"")
        exchange = exchange.sort_values(by='date', ascending=False)

        index = stock[stock['date'] <= exchange['date'].max()].index
        df = stock.drop(index)
        if df.empty :
            print("Exchange date is already up to date.")

        for date in df['date'] :
            date_time_obj = datetime.strptime(date,'%Y.%m.%d')
            dates = date_time_obj.strftime("%Y%m%d")

            url = self.API_URL.format(self.API_KEY, dates, "1")
            response = urlopen(url) 
            json_api = response.read().decode("utf-8")
            json_file = json.loads(json_api)

            temp=json_normalize(json_file)
            temp['date'] = date
            db.addDataframe(temp, 'exchange')


    
if __name__ == "__main__":
    ex = Exchange()
    ex.update()





"""
for i in range(0,800) : 
    str = df['date'][i]
    date_time_obj = datetime.strptime(str, '%Y.%m.%d')
    date = date_time_obj.strftime("%Y%m%d")

    url = API_URL.format(API_KEY, date, "1")

    response = urlopen(url) 
    json_api = response.read().decode("utf-8")
    json_file = json.loads(json_api)

    temp=json_normalize(json_file)
    temp['date'] = df['date'][i]
    db.addDataframe(temp, 'exchange')
    print(temp)
    #temp = pd.read_json(result, orient ='index')
    #total = total.append(temp)

"""