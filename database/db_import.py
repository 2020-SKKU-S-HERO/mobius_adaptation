import pandas as pd
import pymysql.cursors

data = pd.read_csv('CO2_emission_datasheet.csv', sep=',', header=0, names=['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum', 'coal', 'carbon_dioxide', 'date'])

columns = ['acid', 'caco3', 'co2', 'date']


for index, row in data.iterrows():
    print('Limestone : ', row['limestone'])
    print('Clay : ', row['clay'])
    print('Silica_stone : ', row['silica_stone'])
    print('index : ', index)

    if(index > 5):
        break

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
        sql = "INSERT INTO test (date_time, acid, caco3, co2) VALUES ('"+str(row['date'])+"',"+str(row['acid']) + "," + str(row['caco3']) + "," + str(row['co2']) + ");"
        cursor.execute(sql)
    testDB.commit()
finally:
    testDB.close()
"""