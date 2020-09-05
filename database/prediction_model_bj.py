import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM, Dense, Dropout, Activation
from tensorflow.keras.models import Sequential
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('mysql+pymysql://root:shero@localhost/sheroDB', echo=True)

"""
test_DB = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = 'shero',
    database = 'test',
    charset = 'utf8'
)
"""

sql = 'select * from co2_emissions where location="병점"'
data = pd.read_sql(sql, engine)
data['date_time'] = pd.to_datetime(data['date_time'])
data = data.set_index('date_time',inplace=False)
data = data.resample(rule='1440T').sum()

def create_dataset(data, label, look_back=5):
    dataX, dataY = [], []
    for i in range(len(data)-look_back):
        dataX.append(np.array(data.iloc[i:i+look_back]))
        dataY.append(np.array(label.iloc[i+look_back]))
    return np.array(dataX), np.array(dataY)


#데이터 전처리
scaler = MinMaxScaler(feature_range=(0, 1))
scale_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal', 'emissions']
scaled_data = scaler.fit_transform(data[scale_cols])
scaled_data = pd.DataFrame(scaled_data)
scaled_data.columns = scale_cols

train = scaled_data[:-30]
test = scaled_data[-30:]


feature_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal']
label_cols = ['emissions']
train_feature = train[feature_cols]
train_label = train[label_cols]
test_feature = test[feature_cols]
test_label = test[label_cols]

train_feature, train_label = create_dataset(train_feature, train_label,5)
x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.2)
test_feature, test_label = create_dataset(test_feature, test_label,5)



def build_model():
    model = Sequential()
    model.add(LSTM(16, input_shape=(train_feature.shape[1], train_feature.shape[2]),activation='relu',return_sequences=False  ))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    hist = model.fit(x_train, y_train, epochs=200, batch_size=16, validation_data=(x_valid, y_valid))
    return model

def prediction_write_DB(model, input_data):
    predict_value = model.predict(input_data)
	#index = input_data.index
	#index = np.array(index)
	#dic = {'date_time': index,'predict_value':predict_value}
	#predict_value = pd.DataFrame(data=dic, dtype=object)
	#predict_value.to_sql(name='predict_value', con=engine, if_exists='replace')
    print(predict_value)
	print("Success on database writing")

prediction_model = build_model()
prediction_write_DB(prediction_model, test_feature)
