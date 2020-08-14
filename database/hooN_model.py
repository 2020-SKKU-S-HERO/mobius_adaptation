import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pymysql.cursors

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

train_data = df.sample(frac=0.8, random_state=0)
test_data = df.drop(train_data.index)
train_label = train_data.pop('co2')
test_label = test_data.pop('co2')
train_stats = train_data.describe().transpose()

def norm(x):
    return (x - train_stats['mean'])/train_stats['std']

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
    return model

model = build_model()
print(model.summary())

example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
for i in range(len(example_result)):
    example_result[i] = (example_result[i] + train_stats['mean'])*train_stats['std']

print('example_result : ', example_result)
