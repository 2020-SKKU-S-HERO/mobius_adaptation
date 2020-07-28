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
    database: 'sheroDB'
}

exports.get_from_mobius = function(){
    let mobius_connection = mysql.createConnection(mobius_connInfo);
    mobius_connection.connect();
    
    mobius_connection.query('SELECT * FROM cin', function(error, results, fields){
        if(error) throw error;
        console.log('========== The results is: ', results);
    });
    
    mobius_connection.end();
};

