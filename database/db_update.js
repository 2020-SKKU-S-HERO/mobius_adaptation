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

global.writeDataToShero = function(data){
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    let sql = '';
    const hour = 3600000;
    const minute = 60000;
    const seconds = 1000;
    let time, year, month, date, mil_second, hou, min, sec;

    for(var i=0; i<data.length; i++){
        time = data[0].ri.split('-')[1];
        year = time.substring(0, 4);    month = time.substring(4, 6);
        date = time.substring(6, 8);    mil_second = Number(time.substring(8, 17));

        hou = String(parseInt(mil_second / hour));  mil_second = mil_second % hour;
        min = String(parseInt(mil_second / minute));    mil_second = mil_second % minute;
        sec = parseInt(mil_second / seconds);   mil_second = mil_second % seconds;

        if(hou.length==1) hou ='0'+hou;
        if(min.length==1) min = '0'+min;

        time = year + '-' + month + '-' + date + ' ' + hou + ':' + min + ':' + String(sec)
        sql = 'insert into co2_emissions(date_time,emissions,location) values('+'\''+ time + '\''+ ','+ String(data[0].con) + ',' + '\''+ String(data[0].cr) +'\'' + ')';

        ourdb_connection.query(sql, function(error, results, fields){
            if(error){
                console.log('ERROR DETECTED ::::::::::::::::::::::', sql);
            };
            console.log('Successss::::::::::::::::::::::', sql);
        });
    }

    ourdb_connection.end();
}

global.getDataFromMobius = function(date){
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
        if(!results){
            console.log('====================================== MOBIUS DATA NULL');
        }
        console.log('SUCCESS on get Data From Mobius *****************************', sql);
        console.log('----------------------------- DATA FROM MOIBUS : ', results);
        writeDataToShero(results);
    });
    mobius_connection.end();
};

exports.mobius_to_shero = function(){
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    //mobius_connection.connect();
    //ourdb_connection.connect();

    ourdb_connection.query('SELECT MAX(date_time) from co2_emissions', function(error, results, fields){
        if(error) throw error;

        console.log('===================== results : ', results);
        getDataFromMobius(results);

    });
    ourdb_connection.end();
};
