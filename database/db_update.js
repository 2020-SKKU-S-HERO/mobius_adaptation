let mysql = require('mysql');
let os = require('os');
const { sendAcksForNonConfirmablePackets } = require('coap/lib/parameters');

const mobius_connInfo = {
    host: 'localhost',
    port: '3306',
    user: 'root',
    password: 'shero',
    database: 'mobius',
    multipleStatements: true
}

const ourdb_connInfo = {
    host: 'localhost',
    port: '3306',
    user: 'root',
    password: 'shero',
    database: 'sheroDB',
    multipleStatements: true
}

global.select_via_time = function(date){
    let mobius_connection = mysql.createConnection(mobius_connInfo);
    const hour = 3600000;
    const minute = 60000;
    const seconds = 1000;

    date = Date(date)
    date = new Date(date);

    year = date.getFullYear();  month = date.getMonth()+1;
    day = date.getDate();   hou = date.getHours();
    min = date.getMinutes();    sec = date.getMinutes();
    milsec = date.getMilliseconds();

    res_milsec = hou*hour + min*minute + sec*seconds + milsec;
    res_milsec = String(res_milsec);
    month = String(month);
    day = String(day);

    if(month.length==1) month='0'+month;
    if(day.length==1) day='0'+day;

    for(var i=res_milsec.length; i<9; i++){
        res_milsec = '0'+res_milsec;
    }

    res = String(year)+month+day+res_milsec
    let sql = 'SELECT ri, con, cr FROM cin WHERE right(ri, 17) > '+ res;

    mobius_connection.query(sql, function(error, results, fields){
        console.log("======================before results : ", results);
        return results;
    });
    mobius_connection.end();
};
/*
global.mili_to_time = function(time){

};
*/
exports.mobius_to_shero = function(){
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    //mobius_connection.connect();
    //ourdb_connection.connect();

    ourdb_connection.query('SELECT MAX(date_time) from co2_emissions', async function(error, results, fields){
        if(error) throw error;

        console.log('===================== results : ', results);
        finalresult = await select_via_time(results);
        console.log("22222222222222222222final result : ", finalresult);
    });

    ourdb_connection.end();
};
