import sys
import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('mysql+pymysql://root:shero@localhost/test', echo=True)

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

sql = 'select * from test'
df = pd.read_sql(sql, engine, index_col = 'date_time')

def norm(x):
	return (x - train_stats['mean'])/train_stats['std']

train_data = df.iloc[0:8000, :]
test_data = df.drop(train_data.index)
train_label = train_data.pop('co2')
test_label = test_data.pop('co2')
train_stats = train_data.describe().transpose()
normed_train_data = norm(train_data)
normed_test_data = norm(test_data)

#print(train_data.head())


class PrintDot(keras.callbacks.Callback):
	def on_epoch_end(self, epoch, logs):
		if epoch % 40 == 0: print('')
		print('.',end='')


def build_model():   
    EPOCHS = 20
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_data.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)
    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
    #print("model summary : ", model.summary())
	
    """
    history = model.fit(
			train_data, train_label, epochs=EPOCHS, validation_split = 0.2, verbose=0, callbacks=[PrintDot()])
    """
    history = model.fit(
		normed_train_data, train_label, epochs=EPOCHS, 
        validation_split = 0.2, verbose=0, callbacks=[PrintDot()]
    )
	
    #hist = pd.DataFrame(history.history)
    #hist['epoch'] = history.epoch
    #print(hist.tail())
    return model


def model_test(model):
    model = build_model()
    
    loss, mae, mse = model.evaluate(normed_test_data, test_label, verbose=2)
    print("mae : {:5.2f} MPG".format(mae))

    test_predictions = model.predict(normed_test_data).flatten()
    difference = test_predictions - test_label
    print("difference ::::: ")
    print(difference)
    return model    

def prediction_write_DB(model, input_data):
    predict_value = model.predict(input_data).flatten()
    #predict_value = model.predict(input_data).flatten()
    #predict_value = predict_value * train_stats['std']['co2'] + train_stats['mean']['co2']
#print()
#print(input_data.head())
#print(predict_value[0:100])
#print(test_label[0:100])
    index = input_data.index
    index = np.array(index)
    print('')
    print("::::::::::::::::::::::::::::::::::")
#print(index)
    dic = {'date_time': index,'predict_value':predict_value}

    predict_value = pd.DataFrame(data=dic, dtype=object)

#print(predict_value.head())
#print(predict_value)
    predict_value.to_sql(name='predict_value', con=engine, if_exists='replace')
    print("Success on database writing")


def return_prediction_value(model, input_data):
    predict_value = model.predict(norm(input_data)).flatten()
    return predict_value

model_hoon = build_model()
prediction_write_DB(model_hoon, normed_test_data)
