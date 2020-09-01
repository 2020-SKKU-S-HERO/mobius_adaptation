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

    let time, year, month, date, hou, min, sec, milsec, loc;

    for(var i=0; i<data.length; i++){
        time = data[i].ri.split('-');
        info = time[0].split('/')[3];
        console.log('4. inserted info (mobius -> shero): ', info);

        //time = time[1];
        console.log('before :',time[1]);
        time = String(parseInt(time[1])+32400000);
        console.log('after time: ', time);
        year = time.substring(0, 4);    month = time.substring(4, 6);
        date = time.substring(6, 8);    hou = time.substring(8, 10);
        min = time.substring(10, 12);   sec = time.substring(12, 14);
        milsec = time.substring(14, 17);

        time = year + '-' + month + '-' + date + ' ' + hou + ':' + min + ':' + sec +'.' + milsec;

        if(data[i].cr=='Sdongwon')
            loc = "인천";
        else if(data[i].cr=='ShooN')
            loc = '병점';
        else
            loc = '수원';

        if(info=='temp'){
            sql = 'insert into temperature(date_time,temperature,location) values('+'\''+ time + '\''+ ','+ String(data[i].con) + ',' + '\''+ loc +'\'' + ')';
		    //console.log(":::::::::: DB row temp is inserted in temp ");
        }
        else if(info=='flowRate'){
            sql = 'insert into flow_velocity(date_time,flow_velocity,location) values('+'\''+ time + '\''+ ','+ String(data[i].con) + ',' + '\''+ loc +'\'' + ')';
		    //console.log(":::::::::: DB row flowRate is inserted in flowRate ");
        }
        else{
            sql = 'insert into co2_emissions(date_time,emissions,location) values('+'\''+ time + '\''+ ','+ String(data[i].con) + ',' + '\''+ loc +'\'' + ')';
		    //console.log(":::::::::: DB row co2 is inserted in co2 ");
        }

        ourdb_connection.query(sql, function(error, results, fields){
            if(error){
              //  console.log('5. ERROR DETECTED when inserting info to sherdoDB', sql);
            }
            else{
                console.log('5. Successfully inserted into sheroDB with sql :', sql);
                console.log('');
            }
        });
    }

    ourdb_connection.end();
}

global.getDataFromMobius = function(result){
    let mobius_connection = mysql.createConnection(mobius_connInfo);

    date = result[0].time
    console.log('Maximum date from sherodb : ', date);
    console.log('');

    year = String(date.getFullYear());  month = String(date.getMonth()+1);
    day = String(date.getDate());   hou = String(date.getHours());
    minute = String(date.getMinutes());    sec = String(date.getSeconds());
    milsec = String(date.getMilliseconds());
/*
   if(date.getHours()-9<0){
      hou = String(date.getHours()-9+24); //-9
      day = String(date.getDate()-1);
   }
   else{
     hou = String(date.getHours()-9); //-9
     day = String(date.getDate());
   }
*/
    if(month.length==1) month='0'+month;
    if(day.length==1) day='0'+day;
    if(hou.length==1) hou='0'+hou;
    if(minute.length==1) minute='0'+minute;
    if(sec.length==1) sec='0'+sec;
    if(milsec.length==1) milsec='00'+milsec;
    else if(milsec.length==2) milsec='0'+milsec;

    res = year + month + day + hou + minute + sec + milsec;
    console.log('2. Converted date info (date_time -> 17 digit string) : ', res);
    console.log('');

    let sql = 'SELECT ri, con, cr FROM cin WHERE right(ri, 17) > '+ res;

    mobius_connection.query(sql, function(error, results, fields){
        if(!results){
            console.log('');
            console.log('3. No matched ri with date string');
        }
        else{
            //console.log('');
            //console.log('SUCCESS on get Data From Mobius ********************', sql);
            console.log('');
            console.log('3. Date string matched result : ', results, 'and length : ',results.length);
            console.log('');
            //console.log('-------------------------------DATA LENGTH : ', results.length);
            //console.log('');
            if(results.length > 0)
                writeDataToShero(results);
        }
    });
    mobius_connection.end();
};

exports.mobius_to_shero = function(){
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    //mobius_connection.connect();
    //ourdb_connection.connect();

    ourdb_connection.query('SELECT MAX(date_time) as time from co2_emissions', function(error, results, fields){
        if(error)throw error;
        else{
            console.log('1. Getting Max(date_time) from existing SheroDB : ', results);
            console.log('');
            getDataFromMobius(results);
        }
    });
    ourdb_connection.end();
};
