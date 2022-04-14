import pandas as pd
from db import DB
import numpy as np
import os
import json
from pathlib import Path
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def make_dataset(data, label, window_size=20):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size):
        feature_list.append(np.array(data.iloc[i:i+window_size]))
        label_list.append(np.array(label.iloc[i+window_size]))
    return np.array(feature_list), np.array(label_list)

class Model : 
    

    def __init__(self, code) :
        self.code = code
        self.db = DB()
        df = self.db.getTable("sise","where code = {}".format(code))
        df.sort_values(by='date', ascending=True)
        drop = df[df['date'] <= "2019.04.04"].index
        
        df = df.drop(drop)
        df.index = list(range(len(df)))
        df = df[-150:]
        self.date = df['date'].values.tolist()
        self.date = self.date[-130:]
        self.df = df

    def predict(self, units) :


        from sklearn.preprocessing import MinMaxScaler
        from keras.models import Sequential
        from keras.layers import Dense
        from keras.callbacks import EarlyStopping, ModelCheckpoint
        from keras.layers import LSTM
        from keras.layers import Dropout

        scaler = MinMaxScaler()
        scaler_close = MinMaxScaler()
        scale_cols = ['open', 'high', 'low', 'volume']
        scale_cols_close = ['close']
        cols = ['open', 'high', 'low', 'volume' , 'close']
        self.df[scale_cols] = scaler.fit_transform(self.df[scale_cols])
        self.df[scale_cols_close] = scaler_close.fit_transform(self.df[scale_cols_close])
        df_scaled = self.df[cols]

        df_scaled = pd.DataFrame(df_scaled)
        df_scaled.columns = cols

        feature_cols = ['open', 'high', 'low', 'volume']
        label_cols = ['close']
        test_feature = df_scaled[feature_cols]
        test_label = df_scaled[label_cols]
        test_feature, test_label = make_dataset(test_feature, test_label, 20)

        model = Sequential()
        model.add(LSTM(units, 
                    input_shape=(test_feature.shape[1], test_feature.shape[2]), 
                    activation='relu', 
                    return_sequences=False)
                )
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')

        

        path = Path(os.getcwd()).parent
        filename = str(self.code)
        print(str(path) + "/news_crawler/Models/"+filename+".h5")
        model.load_weights(str(path) + "/news_crawler/Models/"+filename+".h5")
        print("load weight from {}.h5".format(filename))

        # 예측
        pred = model.predict(test_feature)
        pred = scaler_close.inverse_transform(pred)
        pred = pred.reshape((130,)).tolist()
        pred = np.around(pred)
        pred = list(map(int, pred))

        df = self.db.getTable("item_10","where code = {}".format(self.code))
        name = df['CONM'][0]
        columns = ['date','predict','name']
        dic = {"date" : self.date, "predict" : pred, "code" : self.code}
        df = pd.DataFrame(dic)
        self.db.deleteCode("predict",self.code)
        self.db.addDataframe(df, "predict")

        

if __name__ == "__main__":
    #삼성전자
    model = Model(5930)
    model.predict(16)
    #sk하이닉스
    model = Model(660)
    model.predict(16)
    #NAVER
    model = Model(35420)
    model.predict(16)
    #삼성바이오로직스
    model = Model(207940)
    model.predict(16)
    #현대자동차
    model = Model(5380)
    model.predict(16)
    #LG화학
    model = Model(51910)
    model.predict(16)
    #삼성SDI
    model = Model(6400)
    model.predict(16)
    #POSCO홀딩스
    model = Model(5490)
    model.predict(16)
    #KB금융
    model = Model(105560)
    model.predict(50)
