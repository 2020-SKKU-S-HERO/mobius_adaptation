import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM, Dense, Dropout, Activation
from tensorflow.keras.models import Sequential
from sqlalchemy import create_engine
from datetime import timedelta

engine = create_engine('mysql+pymysql://root:shero@localhost/sheroDB', echo=True)

def get_data_from_db():
    sql = 'select * from co2_emissions where location="인천"'
    data = pd.read_sql(sql, engine)
    data['date_time'] = pd.to_datetime(data['date_time'])
    data = data.set_index('date_time',inplace=False)
    data = data.resample(rule='1440T').sum()
    return data

def scale(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scale_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal', 'emissions']
    scaled_data = scaler.fit_transform(df[scale_cols])
    scaled_data = pd.DataFrame(scaled_data)
    scaled_data.columns = scale_cols
#print("scaled_data ::::")	
#print(scaled_data.head(31))
    return (scaled_data, scaler)

def denormalize(feature, pred ,scaler):
    denorm_predict = []
    feature["emissions"] = pred
    denorm = scaler.inverse_transform(feature)
    for item in denorm:
        denorm_predict.append(item[6])
    return np.array(denorm_predict)

def feature_label_split(df):
    feature_cols = ['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal']
    label_cols = ['emissions']
    train_feature = df[feature_cols]
    train_label = df[label_cols]
    return (train_feature, train_label)

def make_3D(feature, label, window_size):
    dataX, dataY = [], []
    for i in range(len(feature)-window_size):
        dataX.append(np.array(feature.iloc[i:i+window_size]))
        dataY.append(np.array(label.iloc[i+window_size]))
    return (np.array(dataX), np.array(dataY))

def make_single_3D(feature, window_size):
	dataX = []
	for i in range(len(feature)-window_size):
		dataX.append(np.array(feature.iloc[i:i+window_size]))
	return np.array(dataX)

data = get_data_from_db()
train, scaler = scale(data)
#train = data
feature, label = feature_label_split(train)
train_feature_3d, train_label_3d = make_3D(feature, label, 30)

def build_model(feature_3d):
    model = Sequential()
    model.add(LSTM(64, input_shape=(feature_3d.shape[1], feature_3d.shape[2]),activation='relu',return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

test_feature = pd.concat([feature.iloc[-90:, :], feature.iloc[-365:-305, :]], ignore_index=True)
denom_feature = pd.concat([feature.iloc[-60:, :], feature.iloc[-365:-305, :]], ignore_index=True)
#print(denom_feature.head(20))
#print(denom_feature.info())
#print()

test_label = np.array(label.iloc[-60:, :]).flatten()
test_label = np.append(test_label, np.zeros(60))
test_feature_3d = make_single_3D(test_feature, 30)
#print(train.iloc[-90:-40, :])
#print(test_feature.head())
#print(test_label)

model = build_model(train_feature_3d)
hist = model.fit(train_feature_3d, train_label_3d, epochs=300, batch_size=64)
predict_value = model.predict(test_feature_3d)
predict_value = predict_value.flatten()

denom_predict_value = denormalize(denom_feature, predict_value, scaler)
denom_real_value = np.array(data.iloc[-60:, 0]).flatten()
denom_real_value = np.append(denom_real_value, np.zeros(60))
#print(denom_real_value)
#print(data.head())

loc=[]
for i in range(120):
	loc.append(['인천'])
loc = np.array(loc).flatten()

pred_date = data.iloc[-120:]
pred_date = np.array(pred_date.index)
pred_date = pd.DatetimeIndex(pred_date) + timedelta(days=60)
pred_date = np.array(pred_date)

#dic = {'date_time' : pred_date, 'actual_value' : test_label, 'predict_value' : predict_value , 'location' : loc}
dic = {'date_time' : pred_date, 'actual_value' : denom_real_value, 'predict_value' : denom_predict_value , 'location' : loc}
dff = pd.DataFrame(dic)
dff = pd.DataFrame(dic)
print(dff.head(20))
dff.to_sql(name='predict_value',con=engine, if_exists='append')

