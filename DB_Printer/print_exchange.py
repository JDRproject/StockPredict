from pandas import DataFrame
from db import DB
import sys
import json
from DB_Updater.stock import Stock



def get_exchange():
    db = DB()
    df = db.getTable("exchange","where cur_unit = \"USD\"")
    df = df.sort_values(by='date', ascending=True)
    drop = df[df['date'] <= "2019.04.04"].index
    df = df.drop(drop)
    df.index = list(range(len(df)))
    #print(df)
    temp = df['date'].values.tolist()
    temp2 = df['ttb'].values.tolist()
    temp3 = df['tts'].values.tolist()
    
    df = db.getTable("interest","where sfln_intrc_nm = \"수은채 유통수익률 1개월\"")
    drop = df[df['date'] <= "2019.04.04"].index
    df = df.drop(drop)
    df = df.sort_values(by='date', ascending=True)
    temp4 = df['int_r'].values.tolist()
 
    df.index = list(range(len(df)))
    #print(df)

    dic = {"date" : temp, "ttb" : temp2, "tts" : temp3, "int_r" : temp4}
   
    json_val = json.dumps(dic,  ensure_ascii=False)
    print(json_val)
    #print(df.to_json(orient = 'index'))

def main(argv):
    get_exchange()

if __name__ == "__main__":
    main(sys.argv)