import pandas as pd
import requests
import re
from bs4 import  BeautifulSoup

import pymysql
from sqlalchemy import create_engine
import chardet
from sympy import false
from datetime import datetime

class Stock :

    base_url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}"
    def __init__(self) -> None:
        pass

    
    def crawling(self, code) :

        df = pd.DataFrame(columns = {'date','open', 'close', 'high','low', 'volume', 'diff', 'code'})

        url = self.base_url.format(code, 1)
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        req = requests.get(url, headers= headers)
        soup =  BeautifulSoup(req.text, 'html.parser')
        lastPage = soup.find("td", {"class":"pgRR"})
        if lastPage : 
            lasthref = lastPage.find("a")["href"]
            match = re.search('page=',lasthref).end()
            lastPage = int(lasthref[match:])
            print(lastPage)
            if lastPage > 150 :
                lastPage = 150
        else :
            lastPage = 1


        for idx in range(1,lastPage) :
            url = self.base_url.format(code, idx)
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            req = requests.get(url, headers= headers)
            soup =  BeautifulSoup(req.text, 'html.parser')

            
            trList = soup.find_all("tr", {"onmouseover":"mouseOver(this)"})

            for tr in trList :

                tdList = tr.find_all('td')
                updown = tdList[2].find('img')
                if updown :
                    updown = updown['alt']
                tdList[0] = tdList[0].text.strip()
                if not tdList[0] :
                   break
                for i in range(1,7) :
                   tdList[i] = tdList[i].text.strip().replace(',','')
                   tdList[i] = int(tdList[i])
                if updown == '하락' :
                    tdList[2] *= -1

                temp = pd.DataFrame({'date' : tdList[0],'open' : tdList[3], 'close' : tdList[1], 'high' : tdList[4],'low' : tdList[5], 'volume' : tdList[6], 'diff' : tdList[2], 'code' : code}, index = [0])
                df = df.append(temp)

        return(df)

    def update(self, code, date) :

        df = pd.DataFrame(columns = {'date','open', 'close', 'high','low', 'volume', 'diff', 'code'})

        url = self.base_url.format(code, 1)
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        req = requests.get(url, headers= headers)
        soup =  BeautifulSoup(req.text, 'html.parser')
        
        break_flag = False

        for idx in range(1,150) :
            url = self.base_url.format(code, idx)
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            req = requests.get(url, headers= headers)
            soup =  BeautifulSoup(req.text, 'html.parser')
            trList = soup.find_all("tr", {"onmouseover":"mouseOver(this)"})

            for tr in trList :
                tdList = tr.find_all('td')
                updown = tdList[2].find('img')
                if updown :
                    updown = updown['alt']
                tdList[0] = tdList[0].text.strip()
                if not tdList[0] :
                   break
                for i in range(1,7) :
                   tdList[i] = tdList[i].text.strip().replace(',','')
                   tdList[i] = int(tdList[i])
                if updown == '하락' :
                    tdList[2] *= -1

                temp = pd.DataFrame({'date' : tdList[0],'open' : tdList[3], 'close' : tdList[1], 'high' : tdList[4],'low' : tdList[5], 'volume' : tdList[6], 'diff' : tdList[2], 'code' : code}, index = [0])
                dt = datetime.strptime(tdList[0], '%Y.%m.%d')
                pdt = datetime.strptime(date, '%Y.%m.%d')
                
                if dt<pdt :
                    break_flag = True
                    break

                df = df.append(temp)
            if break_flag :
                break

        return(df)

if __name__ == "__main__":
    df = pd.read_csv("./data/stock_list.csv", encoding='euc-kr')
    print(df)
    stock = Stock()
    df = stock.update("005930","2022.03.20")
    file_name = "005930"
    #df.to_csv(file_name+'.csv', index = False, encoding='utf-8-sig')

    server = '18.182.177.124'
    database = 'stock'
    username = '2zo'
    password = '2zo'

    db_connection_str = 'mysql+pymysql://{}:{}@{}/{}'.format(username,password ,server,database)
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    print(df)