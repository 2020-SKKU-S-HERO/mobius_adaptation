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
from datetime import datetime, timedelta

engine = create_engine('mysql+pymysql://root:shero@localhost/sheroDB', echo=True)
"""
sheroDB = pymysql.connect(
		host = "localhost",
		port = 3306,
		user = "root",
		password = 'shero',
		database = 'sheroDB',
		charset = 'utf8'
)
"""

sql = 'select * from co2_emissions where location="병점"'
data = pd.read_sql(sql, engine)
data['date_time'] = pd.to_datetime(data['date_time'])
data = data.set_index('date_time',inplace=False)
data = data.resample(rule='1440T').sum()

def create_dataset(data, label, look_back=30):
    dataX, dataY = [], []
    for i in range(len(data)-look_back):
        dataX.append(np.array(data.iloc[i:i+look_back]))
        dataY.append(np.array(label.iloc[i+look_back]))
    return np.array(dataX), np.array(dataY)

def create_input(data, look_back=30):
    dataX = []
    for i in range(len(data)-look_back):
        dataX.append(np.array(data.iloc[i:i+look_back]))
    return np.array(dataX)



#데이터 전처리
scaler = MinMaxScaler(feature_range=(0, 1))
scale_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal', 'emissions']
scaled_data = scaler.fit_transform(data[scale_cols])
scaled_data = pd.DataFrame(scaled_data)
scaled_data.columns = scale_cols

train = scaled_data


feature_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal']
label_cols = ['emissions']
train_feature = train[feature_cols]
train_label = train[label_cols]

train_feature, train_label = create_dataset(train_feature, train_label,30)



def build_model():
    model = Sequential()
    model.add(LSTM(16, input_shape=(train_feature.shape[1], train_feature.shape[2]),activation='relu',return_sequences=False  ))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    hist = model.fit(train_feature, train_label, epochs=200, batch_size=16)
    return model
"""
def prediction_write_DB(model, input_data):
	predict_value = model.predict(input_data)
#	predict = []
	loc = ['병점']
#	for i in range(60):
#		predict.append(predict_value[i][0])
#		loc.append('병점');
	#print(data.iloc[-1].name)
	pred_date = data.iloc[-60:]
	pred_date = np.array(pred_date.index)
	pred_date = pd.DatetimeIndex(pred_date) + timedelta(days=60)
	dictionary = {'date_time' : pred_date, 'predict_value' : predict_value , 'location' : loc}
	return dictionary
"""
model = build_model()
input_data = data[feature_cols]
input_data = create_input(input_data[-60:],30)
predict_value = model.predict(input_data)
print(predict_value)
print(predict_value.shape)

"""
dic ={}
model = build_model()
dic = prediction_write_DB(model, input_data)
df = pd.DataFrame(dic)
df.to_sql(name='predict_value', con=engine, if_exists='replace')

"""

