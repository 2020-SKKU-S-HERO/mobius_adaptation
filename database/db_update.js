let mysql = require('mysql');
let os = require('os');

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

global.time_to_mili = function(date){
    const hour = 3600000;
    const minute = 60000;
    const seconds = 1000;

    year = date.getFullYear();  month = date.getMonth()+1;
    day = date.getDate();   hou = date.getHours();
    min = date.getMinutes();    sec = date.getMinutes();
    milsec = date.getMilliseconds();

    res_milsec = hou*hour + min*minute + sec*seconds + milsec;
    res_milsec = String(res_milsec);

    for(var i=res_milsec.length; i<9; i++){
        res_milsec = '0'+res_milsec;
    }
    
    res = String(year)+String(month)+String(day)+res_milsec
    return res;
};
/*
global.mili_to_time = function(time){

};
*/
exports.mobius_to_shero = function(){
    let mobius_connection = mysql.createConnection(mobius_connInfo);
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    mobius_connection.connect();
    ourdb_connection.connect();

    ourdb_connection.query('SELECT MAX(date_time) from co2_emissions', function(error, results, fields){
        if(error) throw error;

        console.log('********************* results get Full Year : ', results);
        console.log('********************* results get Full Year : ', Date(results));
        
        time = time_to_mili(Date(results));
        console.log('======== hooN : ', time);
    });

    /*
    mobius_connection.query('SELECT * FROM cin', function(error, results, fields){
        if(error) throw error;
        console.log('========== The results is: ', results);
    });
    */
    
    ourdb_connection.end();
    mobius_connection.end();
};

