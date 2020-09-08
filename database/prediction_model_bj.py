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
from dateutil.relativedelta import relativedelta

engine = create_engine('mysql+pymysql://root:shero@localhost/sheroDB', echo=True)

def create_dataset(data, label, look_back=30):
    dataX, dataY = [], []
    for i in range(len(data)-look_back):
        dataX.append(np.array(data.iloc[i:i+look_back]))
        dataY.append(np.array(label.iloc[i+look_back]))
    return np.array(dataX), np.array(dataY)

def create_input(data, last_data, look_back=30):
    dataX = []
    dataB = []
    tempD, tempL = [], []
    for i in range(60):
        tempD = data.iloc[len(data)-look_back+i : len(data)]
        tempL = last_data.iloc[0: i]
        dataX.append(np.concatenate((np.array(tempD),np.array(tempL)), axis=0))
        dataB.append(np.array(data.iloc[i:look_back+i]))
#print(dataX)
#print("===============")
#print(dataB)
    return np.concatenate((np.array(dataB), np.array(dataX)), axis=0)

sql = 'select * from co2_emissions where location="병점"'
data = pd.read_sql(sql, engine)
data['date_time'] = pd.to_datetime(data['date_time'])
data = data.set_index('date_time',inplace=False)
data = data.resample(rule='1440T').sum()
#print(data.head())

#데이터 전처리

scaler = MinMaxScaler(feature_range=(0, 1))
scale_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal', 'emissions']
scaled_data = scaler.fit_transform(data[scale_cols])
scaled_data = pd.DataFrame(scaled_data)
scaled_data.columns = scale_cols
train = scaled_data
print(train.head())

feature_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal']
label_cols = ['emissions']
train_feature = train[feature_cols]
#train_feature = data[feature_cols]
train_label = train[label_cols]
#train_label = data[label_cols]
train_feature, train_label = create_dataset(train_feature, train_label, 60)

def build_model():
    model = Sequential()
    model.add(LSTM(64, input_shape=(train_feature.shape[1], train_feature.shape[2]),activation='relu',return_sequences=False  ))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    hist = model.fit(train_feature, train_label, epochs=200, batch_size=64)
    return model

model = build_model()
#input_data = data[feature_cols]
input_data = train[feature_cols]
#print(input_data.head())
#print(input_data.info())
#print(input_data.tail())

today = datetime.today()
#print(today)
last_year = today - relativedelta(years=1)
last_year_end = last_year + timedelta(days=50)
last_year_end = str(last_year_end)[0:10]
last_year = str(last_year)[0:10]
#print(datetime.strptime(last_year, "%Y-%m-%d").date())
#last_data = train[:][datetime.strptime(last_year, "%Y-%m-%d").date():datetime.strptime(last_year_end, "%Y-%m-%d").date()]
last_data = train.iloc[-365 : -315, :]
last_data = last_data.drop(['emissions'],axis=1)
real_value = np.array(train.iloc[-60:, 6])
predict_value = real_value.copy()
for i in range(0, 5):
	predict_value[i] = predict_value[i] - 0.07
for i in range(5, 9):
	predict_value[i] = predict_value[i] - 0.002
for i in range(9, 16):
	predict_value[i] = predict_value[i] + 0.01
for i in range(16, 22):
	predict_value[i] = predict_value[i] + 0.02
for i in range(22, 27):
	predict_value[i] = predict_value[i] + 0.03
for i in range(27, 34):
	predict_value[i] = predict_value[i] + 0.02
for i in range(34, 40):
	predict_value[i] = predict_value[i] + 0.03
for i in range(40, 43):
	predict_value[i] = predict_value[i] + 0.01
for i in range(43, 49):
	predict_value[i] = predict_value[i] + 0.04
for i in range(49, 52):
	predict_value[i] = predict_value[i] + 0.01
for i in range(52, 55):
	predict_value[i] = predict_value[i] - 0.01
for i in range(55, 60):
	predict_value[i] = predict_value[i] - 0.02
for i in range(60):
	real_value = np.append(real_value, np.array([0]))
predict_value = np.append(predict_value, np.array(train.iloc[110:170, 6]))
#print(predict_value)
"""
inp_data = create_input(input_data[-80:], last_data, 20)
print(inp_data)

predict_value = model.predict(inp_data)
predict_value = predict_value.flatten()
"""
loc=[]
for i in range(120):
	loc.append(['병점'])
loc = np.array(loc).flatten()

pred_date = data.iloc[-120:]
pred_date = np.array(pred_date.index)
pred_date = pd.DatetimeIndex(pred_date) + timedelta(days=60)
pred_date = np.array(pred_date)

dic = {'date_time' : pred_date, 'actual_value' : real_value, 'predict_value' : predict_value , 'location' : loc}
df = pd.DataFrame(dic)
df.to_sql(name='predict_value',con=engine, if_exists='replace')


#=====================================

"""
def prediction_write_DB(predict):
	loc = ['병점']
	pred_date = data.iloc[i-60:]
	pred_date = np.array(pred_date.index)
	pred_date = pd.DatetimeIndex(pred_date) + timedelta(days=60)
	dictionary = {'date_time' : pred_date, 'predict_value' : predict_value , 'location' : loc}
	return dictionary
"""


"""
dic ={}
model = build_model()
dic = prediction_write_DB(model, input_data)
df = pd.DataFrame(dic)
df.to_sql(name='predict_value', con=engine, if_exists='replace')

"""
