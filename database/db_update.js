let mysql = require('mysql');
let os = require('os');
const { sendAcksForNonConfirmablePackets } = require('coap/lib/parameters');
const { min } = require('moment');

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

global.writeDataToShero = function(data){
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    let sql = '';
   
    let time, year, month, date, hou, min, sec, milsec;

    for(var i=0; i<data.length; i++){
        time = data[i].ri.split('-')[1];
        year = time.substring(0, 4);    month = time.substring(4, 6);
        date = time.substring(6, 8);    hou = time.substring(8, 10);
        min = time.substring(10, 12);   sec = time.substring(12, 14);
        milsec = time.substring(14, 17);

        time = year + '-' + month + '-' + date + ' ' + hou + ':' + min + ':' + sec +'.' + milsec;
        sql = 'insert into co2_emissions(date_time,emissions,location) values('+'\''+ time + '\''+ ','+ String(data[0].con) + ',' + '\''+ String(data[0].cr) +'\'' + ')';

        ourdb_connection.query(sql, function(error, results, fields){
            if(error){
                console.log('ERROR DETECTED ::::::::::::::::::::::', sql);
            }
            else{
                console.log('Successss::::::::::::::::::::::', sql);
                console.log('\n');
            }
        });
    }

    ourdb_connection.end();
}

global.getDataFromMobius = function(date){
    let mobius_connection = mysql.createConnection(mobius_connInfo);

    date = Date(date)
    date = new Date(date);

    year = String(date.getFullYear());  month = String(date.getMonth()+1);
    day = String(date.getDate());   hou = String(date.getHours());
    minute = String(date.getMinutes());    sec = String(date.getSeconds());
    milsec = String(date.getMilliseconds());

    if(month.length==1) month='0'+month;
    if(day.length==1) day='0'+day;
    if(hou.length==1) hou='0'+hou;
    if(minute.length==1) minute='0'+minute;
    if(sec.length==1) sec='0'+sec;
    if(milsec.length==1) milsec='00'+milsec;
    else if(milsec.length==2) milsec='0'+milsec;

    res = year + month + day + hou + minute + sec + milsec;
    let sql = 'SELECT ri, con, cr FROM cin WHERE right(ri, 17) > '+ res;

    mobius_connection.query(sql, function(error, results, fields){
        if(!results){
            console.log('====================================== MOBIUS DATA NULL');
        }
        else{
            console.log('SUCCESS on get Data From Mobius *****************************', sql);
            console.log('\n');
            console.log('----------------------------- DATA FROM MOIBUS : ', results);
            console.log('\n');
            writeDataToShero(results);
        }
    });
    mobius_connection.end();
};

exports.mobius_to_shero = function(){
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    //mobius_connection.connect();
    //ourdb_connection.connect();

    ourdb_connection.query('SELECT MAX(date_time) from co2_emissions', function(error, results, fields){
        if(error)throw error;
        else{
            console.log('===================== results : ', results);
            console.log('\n');
            getDataFromMobius(results);
        }
    });
    ourdb_connection.end();
};
