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

let today = new Date();
let today_date = String(today.getFullYear())+ String(today.getMonth()+1)+ String(today.getDate());


const ep_host = 'https://openapi.kpx.or.kr/openapi/forecast1dMaxBaseDate/';
const ep_CODE = 'getForecast1dMaxBaseDate';
const ep_CODE_today = 'Sukub5mToday';
const ep_serviceKey = 'VbQNuye6GhNGAQ00jwTa6eGyuFnBY%2B9bmGMYEVXsqBY94ARYroVyHA0WxwOse6em%2FdhcrPZUWBvsoCgl6sDrww%3D%3D';

global.electricity_power = function(){
	let url = ep_host + ep_CODE_today + '?serviceKey=' + ep_serviceKey;
	console.log(url);
	let par;
	request(url, function(err, res, body){
		console.log(res);
		console.log(body);
		par = JSON.parse(body);
		console.log(par);
	});
}

//환율 정보를 API로부터 받아 DB에 쓴다.
global.exchange_rate = function(){	

	let url = er_host+'/'+er_token+'/json/kr/'+'1/'+'1/'+er_CODE+'/DD/'+today_date + '/'+today_date+ + '/'+er_dollar;
	let par;

	request(url, function(err, res, body){
		par = JSON.parse(body);
		writeData(par.StatisticSearch.row[0], 'exchage_rate');
	});
}

//DB에 쓰는 부분이다.
global.writeData = function(data, table_name){
	const db_connection = mysql.createConnection(db_connInfo);
	let sql = 'INSERT INTO '+ table_name+'(date_time, dollar) VALUES ('+data.TIME;
	sql = sql + ',' + data.DATA_VALUE + ');';

	db_connection.query(sql, function(error, results, fields){
		if(error){
			console.log(error);
			console.log("DB INSERTION ERROR : ", sql);
		}
		else console.log("SUCCEED ON INSERTING DATA ON DB : ", sql);
	});
}

electricity_power();
//exchange_rate();
