import sys
import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pymysql.cursors
import matplotlib.pyplot as plt

test_DB = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = 'shero',
    database = 'test',
    charset = 'utf8'
)

sql = 'select * from test'
df = pd.read_sql(sql, test_DB)

def norm(x):
	return (x - train_stats['mean'])/train_stats['std']

train_data = df.sample(frac=0.8, random_state=0)
test_data = df.drop(train_data.index)
train_label = train_data.pop('co2')
test_label = test_data.pop('co2')
train_stats = train_data.describe().transpose()
normed_train_data = norm(train_data)
normed_test_data = norm(test_data)

def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_data.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
    print("model summary : ", model.summary())
    return model

class PrintDot(keras.callbacks.Callback):
	def on_epoch_end(self, epoch, logs):
		if epoch % 20 == 0: print('')
		print('.',end='')

def model_test():
    model = build_model()
    EPOCHS = 20
    history = model.fit(
		normed_train_data, train_label, epochs=EPOCHS, validation_split = 0.2, verbose=0, callbacks=[PrintDot()])

    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print(hist.tail())

    loss, mae, mse = model.evaluate(normed_test_data, test_label, verbose=2)
    print("mae : {:5.2f} MPG".format(mae))

    test_predictions = model.predict(normed_test_data).flatten()

    error = test_predictions - test_label
    print("error ::::: " ,error)
    return model

model_test()
