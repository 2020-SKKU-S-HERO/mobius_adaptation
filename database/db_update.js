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

exports.mobius_to_shero = function(){
    let mobius_connection = mysql.createConnection(mobius_connInfo);
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    mobius_connection.connect();
    ourdb_connection.connect();

    const hour = 3600000;
    const minute = 60000;
    const seconds = 1000;
    
    ourdb_connection.query('SELECT MAX(date_time) from co2_emissions', function(error, results, fields){
        if(error) throw error;
        max_time = results;
        console.log("========== The max_time is : ", max_time);
        console.log("========== The type of max_time is : ", typeof(max_time));
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

