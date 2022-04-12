from pandas import DataFrame
from db import DB
import sys
import json
from DB_Updater.stock import Stock
def updateSise() : 
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

def getStockPrice(CODE):
    db = DB()
    df = db.getTable("sise","where code = {}".format(CODE))
    df.sort_values(by='date', ascending=False)
    drop = df[df['date'] <= "2019.04.04"].index
    df = df.drop(drop)
    df.index = list(range(len(df)))
    temp = df['date'].values.tolist()
    temp2 = df['close'].values.tolist()

    df = db.getTable("item_10","where code = {}".format(CODE))
    name = df['CONM'][0]
    dic = {"date" : temp, "close" : temp2, "name" : name}
   
    json_val = json.dumps(dic,  ensure_ascii=False)
    print(json_val)
    #print(df.to_json(orient = 'index'))

def getPredictPrice(CODE) :
    db = DB()
    df = db.getTable("predict","where code = {}".format(CODE))
    df.sort_values(by='date', ascending=False)
    df.index = list(range(len(df)))
    temp = df['date'].values.tolist()
    temp2 = df['predict'].values.tolist()

    df = db.getTable("item_10","where code = {}".format(CODE))
    name = df['CONM'][0]
    dic = {"date" : temp, "close" : temp2, "name" : name}

    json_val = json.dumps(dic,  ensure_ascii=False)
    print(json_val)


def main(argv):


    if len(argv) == 3:
        CODE = argv[1]
        FUNC = int(argv[2])
    elif len(argv) == 2:
        CODE = argv[1]
        FUNC = 1
    else:
        return
    if FUNC == 1 :
        getStockPrice(CODE)
    elif FUNC == 2 :
        getPredictPrice(CODE)

if __name__ == "__main__":
    main(sys.argv)