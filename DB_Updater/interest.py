from html.entities import html5
from db import DB
from urllib.request import Request, urlopen
from datetime import datetime
from bs4 import BeautifulSoup
import json
import pandas as pd 
from pandas import DataFrame, json_normalize

class Interest :

    API_KEY = "7sILquziYCXYoSIjjkrfsso2UGiibiwr"
    API_URL = "https://www.koreaexim.go.kr/site/program/financial/interestJSON?authkey={}&searchdate={}&data=AP0{}"

    def __init__(self) -> None:
        pass

    def update(self) :

        
        db = DB()
        stock = db.getDate("sise", "where code = 5930")
        stock = stock.sort_values(by='date', ascending=False)
        interest = db.getDate("interest", "where sfln_intrc_nm = \'수은채 유통수익률 1개월\'")
        if interest is not None:
            interest = interest.sort_values(by='date', ascending=False)
            index = stock[stock['date'] <= interest['date'].max()].index
            df = stock.drop(index)
        else :
            df = stock

        if df.empty :
            print("Interest date is already up to date.")
            return

        for date in df['date'] :
            date_time_obj = datetime.strptime(date,'%Y.%m.%d')
            dates = date_time_obj.strftime("%Y%m%d")

            url = self.API_URL.format(self.API_KEY, dates, "2")
            response = urlopen(url)
            json_api = response.read().decode("utf-8")
            json_file = json.loads(json_api)

            temp=json_normalize(json_file)
            temp['date'] = date
            db.addDataframe(temp, 'interest')
    
if __name__ == "__main__":
    interest = Interest()
    interest.update()