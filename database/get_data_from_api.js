const request = require('request');

const host = 'http://ecos.bok.or.kr/api/StatisticSearch'
const CODE_exchange_rate = '036Y001';
const dollar = '0000001';
const token = 'TV0P8YV3A6NS778F0JIZ';

let url = host+'/'+token+'/json/kr/'+'1/'+'1/'+CODE_exchange_rate+'/DD/'+'20200901/'+'20200901/'+dollar;
let par;

request(url, function(err, res, body){
    //console.log(res);
    console.log(body);
    par = JSON.parse(body);
    console.log(par.row);
})

