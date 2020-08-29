import pandas as pd
import pymysql.cursors

sheroDB = pymysql.connect(
		host = "localhost",
		port = 3306,
		user = "root",
		password = 'shero',
		database = 'sheroDB',
		charset = 'utf8'
)

sheet = ['인천', '수원', '병점']

try:
	cursor = sheroDB.cursor()
	for loc in sheet:
		data = pd.read_excel('CO2_emission_datasheet.xlsx', sheet_name=loc, header=0,
				names=['limestone', 'clay', 'silica_stone', 'iron_oxide', 'gypsum',
				'coal', 'carbon_dioxide', 'date'])
		for index, row in data.iterrows():
			sql = "INSERT INTO input (date_time, location,limestone, clay, silica_stone, iron_oxide, gypsum, coal) VALUES ('"+str(row['date'])+"','"+ loc +"',"+str(row['limestone']) + ","+str(row['clay'])+","+str(row['silica_stone'])+ "," + str(row['iron_oxide']) + "," + str(row['gypsum']) + "," + str(row['coal']) + ");"
#print(sql)            
			cursor.execute(sql)
			sql = "INSERT INTO co2_emissions (date_time, location, emissions) VALUES ('"+str(row['date'])+"','"+loc +"',"+str(row['carbon_dioxide']) + ");"
			cursor.execute(sql)
			sheroDB.commit()
finally:
	sheroDB.close()
"""
	for index, row in data.iterrows():
		print('Limestone : ', row['limestone'])
		print('Clay : ', row['clay'])
		print('Silica_stone : ', row['silica_stone'])
		print('index : ', index)
		print('index : ', loc)

		if(index > 5):
			break
"""
