import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM, Dense, Dropout, Activation
from tensorflow.keras.models import Sequential
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_data_from_db():
    engine = create_engine('mysql+pymysql://root:shero@localhost/sheroDB', echo=True)
    sql = 'select * from co2_emissions where location="병점"'
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
    return scaled_data

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
train = scale(data)
feature, label = feature_label_split(train)
train_feature_3d, train_label_3d = make_3D(feature, label, 30)

def build_model(feature_3d):
    model = Sequential()
    model.add(LSTM(64, input_shape=(feature_3d.shape[1], feature_3d.shape[2]),activation='relu',return_sequences=False  ))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

today = datetime.today()
#print(today)
last_year_day = today - relativedelta(years=1)
last_year_end = last_year_day + timedelta(days=60)
last_year_end = str(last_year_end)[0:10]
last_year_day = str(last_year_day)[0:10]
#print(datetime.strptime(last_year, "%Y-%m-%d").date())
#last_data = train[:][datetime.strptime(last_year, "%Y-%m-%d").date():datetime.strptime(last_year_end, "%Y-%m-%d").date()]

test_feature = pd.concat([feature.iloc[-30:, :], feature.iloc[-365:-305, :]], ignore_index=True)
test_label = label.iloc[-365:-305, :]
test_feature_3d = make_single_3D(test_feature, 30)

model = build_model(train_feature_3d)
hist = model.fit(train_feature_3d, train_label_3d, epochs=100, batch_size=64)
predict_value = model.predict(test_feature_3d)
predict_value = predict_value.flatten()


loc=[]
for i in range(60):
	loc.append(['병점'])
#loc = np.array(loc).flatten()

pred_date = data.iloc[-60:]
pred_date = np.array(pred_date.index)
pred_date = pd.DatetimeIndex(pred_date) + timedelta(days=60)
pred_date = np.array(pred_date)

dic = {'date_time' : pred_date, 'actual_value' : test_label, 'predict_value' : predict_value , 'location' : loc}
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
