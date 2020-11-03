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

    for index, row in wti.iterrows():
        print(row['date'], row['WTI($/bbl)'])
        print("=======")
        print(elec[elec['date']==row['date']].iloc[0, 1])
        print("*******")
        print(kau[kau['date']==row['date']].iloc[0, 1])
        print('')
        new_row = {'date' : row['date'], 'WTI($/bbl)' : row['WTI($/bbl)'],
                   'elec': elec[elec['date']==row['date']].iloc[0, 1],
                   'price' : kau[kau['date']==row['date']].iloc[0, 1]}
        print(new_row)
        df.append(new_row, ignore_index=True)

    print("WTI")
    #print(wti.describe())
    print(wti.head())

    print("ELEC")
    #print(elec.describe())
    print(elec.head())

    print("KAU")
    #print(kau.describe())
    print(kau.head())

    print("SUM")
    print(df.head())

    #df = pd.concat([wti, elec, kau], ignore_index=True )
    #print(df.head())
    #print(df.describe())

if __name__ == "__main__":
    wti, kau = data_from_csv()
    elec = data_from_xls()
    struct_data(wti, elec, kau)
