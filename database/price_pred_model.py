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
    return wti_after_2015


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

    #KAU
    kau = pd.read_excel('data/KAU_20150112_20201029.xlsx',
        names=['date', 'price', 'diff', 'diff_per', 'start_price','high_price',
               'low_price', 'volume', 'transaction_price', 'total_price', 'un', 'un2'])
    kau.drop(['un', 'un2'], axis='columns', inplace=True)
    kau_price = kau[['date', 'price']]
    #print(kau_price.head())
    return (elec_after_2015, kau_price)

def scale(df):
    print('')

def struct_data(wti, elec, kau):
    print("WTI")
    print(wti.describe())
    print(wti.head())

    print("ELEC")
    print(elec.describe())
    print(elec.head())

    print("KAU")
    print(kau.describe())
    print(kau.head())

    #df = pd.concat([wti, elec, kau], ignore_index=True )
    #print(df.head())
    #print(df.describe())

if __name__ == "__main__":
    wti = data_from_csv()
    elec, kau = data_from_xls()
    struct_data(wti, elec, kau)
