import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:shero@localhost/sheroDB', echo=True)

def data_from_csv():
    wti = pd.read_csv('data/WTI_20050630_20200417.csv')
    wti_after_2015 = wti[wti['date'] > '2015-01-11']
    #print(wti_after_2015.head())
    #print(wti_after_2015.describe())

    # KAU
    kau18 = pd.read_csv('data/KAU18.csv', header=0,
        names=['date', 'name', 'price', 'diff', 'diff_per', 'high_price',
        'low_price', 'volume', 'transaction_price', 'weighted_average'])
    kau18_price = kau18[['date', 'price']]
    kau18_price.sort_values(by=['date'], ascending=True, inplace=True,
        kind='mergesort', ignore_index=True)
    day_count = [i for i in range(kau18_price.count()['date'])]
    kau18_price['day'] = day_count
    #print(kau18_price.describe())
    #print(kau18_price.tail())


    kau19 = pd.read_csv('data/KAU19.csv', header=0,
            names=['date', 'name', 'price', 'diff', 'diff_per', 'high_price',
            'low_price', 'volume', 'transaction_price', 'weighted_average'])
    kau19_price = kau19[['date', 'price']]
    kau19_price.sort_values(by=['date'], ascending=True, inplace=True,
            kind='mergesort', ignore_index=True)
    day_count = [i for i in range(kau19_price.count()['date'])]
    kau19_price['day'] = day_count
    #print(kau19_price.describe())
    #print(kau19_price.tail())

    kau1819 = kau18_price.append(kau19_price, ignore_index=True)
    #print(kau1819)

    return (wti_after_2015, kau1819)


def data_from_xls():
    #ELECTRICITY
    elec = pd.read_excel('data/electricity_20140101_20201025.xlsx',
                         names=['date', '1', '2', '3', '4', '5', '6', '7', '8'
                                , '9', '10', '11', '12', '13', '14', '15', '16'
                                , '17', '18', '19', '20', '21', '22', '23', '24'])
    elec_after_2015 = elec[elec['date']>'2015-01-11']
    elec_day = elec_after_2015.sum(axis=1)
    elec_after_2015['elec'] = elec_day
    elec_after_2015.drop(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24' ], axis='columns', inplace=True)
    # print(elec_after_2015.head())

    return (elec_after_2015)

def scale(df):
    print('')

def struct_data(wti, elec, kau):
    #유가는 금융시장에서 매겨지기 때문에 시장이 쉬는 날에는 데이터가 없다.
    #전력은 매일 있다.
    #그래서 유가 데이터가 없는 날의 전력 데이터는 없애야 한다.
    df = pd.DataFrame()

    for index, row in kau.iterrows() :
        if not wti[wti['date']==row['date']].empty :
            #print(wti[wti['date']==row['date']]['WTI($/bbl)'].values[0])
            new_row = { 'date' : row['date'], 'day' : row['day'], 'price' : row['price'],'WTI($/bbl)' : wti[wti['date']==row['date']]['WTI($/bbl)'].values[0] }
            df = df.append(new_row, ignore_index=True)
    df.insert(4,'elec', 0)
    for index, row in df.iterrows() :
        if not elec[elec['date']==row['date']].empty :
            #print(elec[elec['date']==row['date']]['elec'].values[0])
            #new_row = {'elec' : elec[elec['date']==row['date']]['elec'].values[0]}
            #df.loc[index]['elec'] = (elec[elec['date']==row['date']]['elec'].values[0])
            df.loc[index,'elec'] = (elec[elec['date']==row['date']]['elec'].values[0])
    return df
    #print(df.describe())
    #print(df.info())

from keras.models import Sequential
from keras.layers import Dense
def build_model():
    model = keras.Sequential()
    model.add(Dense(16, input_dim = 3, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))




if __name__ == "__main__":
    wti, kau = data_from_csv()
    elec = data_from_xls()
    data = struct_data(wti, elec, kau)
