const request = require('request');

//ER is Exchange Rate
const er_host = 'http://ecos.bok.or.kr/api/StatisticSearch'
const er_CODE = '036Y001';
const er_dollar = '0000001';
const er_token = 'TV0P8YV3A6NS778F0JIZ';

const mysql = require('mysql');
const db_connInfo = {
	host : 'localhost',
	port: '3306',
	user: 'root',
	password: 'shero',
	database: 'sheroDB',
	multipleStatements: true
};

global.get_various_data = function(){
	
	let today = new Date();
	let today_date = String(today.getFullYear())+ String(today.getMonth()+1)+ String(today.getDate());

	let url = er_host+'/'+er_token+'/json/kr/'+'1/'+'1/'+er_CODE+'/DD/'+today_date + '/'+today_date+ + '/'+er_dollar;
	let par;

	request(url, function(err, res, body){
		par = JSON.parse(body);
		writeData(par.StatisticSearch.row[0]);
	});
}

global.writeData = function(data){

	const db_connection = mysql.createConnection(db_connInfo);

	let sql = 'INSERT INTO exchange_rate(date_time, dollar) VALUES (';
	sql = sql + data.TIME;
	sql = sql + ',' + data.DATA_VALUE + ');';

	db_connection.query(sql, function(error, results, fields){
		if(error){
			console.log(error);
			console.log("DB INSERTION ERROR : ", sql);
		}
		else console.log("SUCCEED ON INSERTING DATA ON DB : ", sql);
	});
}

get_various_data();
