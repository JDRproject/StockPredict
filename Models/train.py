#%%
from itertools import dropwhile
import numpy as np
from db import DB
import pandas as pd
import os
from keras.callbacks import EarlyStopping

def make_dataset(data, label, window_size=20):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size):
        feature_list.append(np.array(data.iloc[i:i+window_size]))
        label_list.append(np.array(label.iloc[i+window_size]))
    return np.array(feature_list), np.array(label_list)




CODE = 5930
TEST_SIZE = 150


#DB에서 데이터 가져와서 데이터프레임 만들기
db = DB()
df = db.getTable("sise", "where code = {}".format(CODE))
df = df.sort_values(by='date' ,ascending=True)
drop = df[df['date'] <= "2019.04.04"].index
df = df.drop(drop)
df.index = list(range(len(df)))
df = df[['date','open','low','high','close','diff','volume']]
#print(df)


#0~1 값으로 스케일링
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scale_cols = ['open', 'high', 'low', 'close', 'volume']
df_scaled = scaler.fit_transform(df[scale_cols])
print(df_scaled)
df_scaled = pd.DataFrame(df_scaled)
df_scaled.columns = scale_cols

#
print(df_scaled)



train = df_scaled[:-TEST_SIZE]
test = df_scaled[-TEST_SIZE:]
#
feature_cols = ['open', 'high', 'low', 'volume']
label_cols = ['close']

train_feature = train[feature_cols]
train_label = train[label_cols]

train_feature, train_label = make_dataset(train_feature, train_label, 20)

# train, validation set 생성
from sklearn.model_selection import train_test_split
x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.2)

#print(x_train.shape, x_valid.shape)

test_feature = test[feature_cols]
test_label = test[label_cols]


# test dataset (실제 예측 해볼 데이터)
test_feature, test_label = make_dataset(test_feature, test_label, 20)
#print(test_feature.shape, test_label.shape)
# ((180, 20, 4), (180, 1))

from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM
from keras.layers import Dropout

model = Sequential()
model.add(LSTM(16, 
               input_shape=(train_feature.shape[1], train_feature.shape[2]), 
               activation='relu', 
               return_sequences=False)
          )
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
early_stop = EarlyStopping(monitor='val_loss', patience=5)
filename = ('tmp_checkpoint.h5')
checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')

history = model.fit(x_train, y_train, 
                    epochs=200, 
                    batch_size=16,
                    validation_data=(x_valid, y_valid), 
                    callbacks=[early_stop, checkpoint])


# weight 로딩
model.load_weights(filename)

# 예측
pred = model.predict(test_feature)
pred_train = model.predict(train_feature)

import matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 9))
plt.plot(test_label, label='actual')
plt.plot(pred, label='prediction')
plt.legend()
plt.show()

plt.plot(train_label, label='actual')
plt.plot(pred_train, label='prediction')
plt.show
# %%
