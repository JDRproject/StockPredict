from sqlite3 import Cursor
from django import db
import pandas as pd
import pymysql
from sqlalchemy import create_engine


class DB :
    db = None

    def __init__(self) -> None:
        self.db = pymysql.connect(
            host="18.182.177.124", # 접근 주소
            port=3306,  # 접근 포트 번호
            user="2zo",  # 아이디
            passwd="2zo",  # 비밀번호
            db="stock",  # DB 이름
            charset='utf8',    
            cursorclass = pymysql.cursors.DictCursor,
            init_command='SET NAMES UTF8'   # UTF8 로  가져오기
            )       

    def getDate(self, name, where):
        cursor = self.db.cursor()
        sql = "SELECT date from {} {}".format(name, where)
        try: 
            cursor.execute(sql)
        except Exception as e:
            print(e)
            return None
        data = cursor.fetchall()
        return pd.DataFrame(data)

    def getTable(self, name, where):
        cursor = self.db.cursor()
        sql = "SELECT * from {} {}".format(name, where)
        cursor.execute(sql)
        data = cursor.fetchall()
        return pd.DataFrame(data)

    def addDataframe(self, df, name):
        server = '18.182.177.124'
        database = 'stock'
        username = '2zo'
        password = '2zo'

        db_connection_str = 'mysql+pymysql://{}:{}@{}/{}'.format(username,password ,server,database)
        db_connection = create_engine(db_connection_str, encoding='utf-8')
        conn = db_connection.connect()
        df.to_sql(name=name, con=db_connection, if_exists='append',index=False)

    def replaceDataframe(self, df, name):
        server = '18.182.177.124'
        database = 'stock'
        username = '2zo'
        password = '2zo'

        db_connection_str = 'mysql+pymysql://{}:{}@{}/{}'.format(username,password ,server,database)
        db_connection = create_engine(db_connection_str, encoding='utf-8')
        conn = db_connection.connect()
        df.to_sql(name=name, con=db_connection, if_exists='replace',index=False)

    def deleteDate(self, name, date):
        cursor = self.db.cursor()
        sql = "DELETE from {} WHERE date=\'{}\'".format(name,date)
        cursor.execute(sql)
        ret = self.db.commit()
        return ret

    def deleteCode(self, name, code):
        cursor = self.db.cursor()
        sql = "DELETE from {} WHERE code=\'{}\'".format(name,code)
        cursor.execute(sql)
        ret = self.db.commit()
        return ret
        
    def getLastUpdate(self, name):
        cursor = self.db.cursor()
        sql = "SELECT MAX(date) as max from {}".format(name)
        cursor.execute(sql)
        data = cursor.fetchall()
        return pd.DataFrame(data)



