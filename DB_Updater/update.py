from pandas import DataFrame
from stock import Stock 
from db import DB
from exchange import Exchange
from interest import Interest
from model import Model
from discuss import Discuss
def updateSise() : 
    print("Updating Stock sise datas.")
    db = DB()
    
    stock = Stock()
    top10 = db.getTable("item_10" , "")
    total = DataFrame()

    stock_last = db.getLastUpdate("sise")["max"][0]
    db.deleteDate("sise",stock_last)

    for code in top10['CODE'] :
        df = stock.update(str(code).zfill(6), stock_last)
        total = total.append(df)
    
    db.addDataframe(total, "sise")
    print("A total of {} stock price data has been updated.".format(len(total)))

def updateDiscuss() : 
    print("Updating discuss datas.")

    db = DB()
    
    discuss = Discuss()
    top10 = db.getTable("item_10" , "")
    total = DataFrame()

    for code in top10['CODE'] :
        df = discuss.update(code)
        total = total.append(df)
    
    db.replaceDataframe(total, "discuss")
    print("A total of {} discuss data has been updated.".format(len(total)))

def updateExchange() :
    print("Updating Exchange datas.")
    ex = Exchange()
    ex.update()

def updateInterest() :
    print("Updating Interest datas.")
    interest = Interest()
    interest.update()

def updatePredict() :
    print("Updating Predict datas.")
    model = Model(5930)
    model.predict()

if __name__ == "__main__":
     updateSise()
     updateExchange()
     updateInterest()
     updateDiscuss()
