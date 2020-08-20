import pandas as pd
import pymysql.cursors

data = pd.read_csv('testdata.csv', sep=',', header=0, names=['acid', 'caco3', 'co2', 'date'])

columns = ['acid', 'caco3', 'co2', 'date']

"""
for index, row in data.iterrows():
    print('Acid(ml) : ', row['acid'])
    print('CaCO3(g) : ', row['caco3'])
    print('CO2 : ', row['co2'])
    print('index : ', index)
"""

testDB = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = 'shero',
    database = 'test',
    charset = 'utf8'
)

try:
    cursor = testDB.cursor()
    for index, row in data.iterrows():
        sql = "INSERT INTO test (date_time, acid, caco3, co2) VALUES ("+str(row['date']+","+str(row['acid']) + "," + str(row['caco3']) + "," + str(row['co2']) + ");"
        cursor.execute(sql)
    testDB.commit()
finally:
    testDB.close()
