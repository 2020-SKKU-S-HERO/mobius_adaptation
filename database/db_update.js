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

global.writeDataToShero = function (data) {
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    let sql_ic, sql_bj, sql_sw;
	let time_ic, time_bj, time_sw;
	let ic_co2_sum=0, ic_co2_len=0, ic_flow_sum=0, ic_flow_len=0;
	let bj_co2_sum=0, bj_co2_len=0, bj_flow_sum=0, bj_flow_len=0;
	let sw_co2_sum=0, sw_co2_len=0, sw_flow_sum=0, sw_flow_len=0;
    let emi_bj = 0;
	const AREA = 38.48;
    let limestone=0, gypsum=0, clay=0, coal=0, silica_stone=0, iron_oxide=0;
    let flow=0, emi=0;

    let time, year, month, date, hou, min, sec, milsec, loc;
	const mini=0.97, max=1.03;
    for (var i = 0; i < data.length; i++) {
		//emi = 0; flow=0;
		//if(i<20)
		//	console.log(data[i]);
		time = data[i].ri.split('-');
        info = time[0].split('/')[3];
        time = time[1];

        year = time.substring(0, 4); month = time.substring(4, 6);
        date = time.substring(6, 8); hou = time.substring(8, 10);
        min = time.substring(10, 12); sec = time.substring(12, 14);
        milsec = time.substring(14, 17);

        year = parseInt(year);   month = parseInt(month);
        hou = parseInt(hou);    date = parseInt(date);
        month = parseInt(month);
			
		//TIME SHIFT
        if (hou >= 15) {
            hou = hou + 9 - 24; //-9
            date = date + 1;
            if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12) {
                if(date>31){
                    date = 1;
                    month = month + 1;
                    if(month>12){
                        month = 1
                        year = year + 1;}
                }
            }
            else if(month == 4 || month == 6 || month == 9 || month == 11){
                if(date>30){
                    date = 1;
                    month = month + 1;
                }
            }
            else{
                if(date>28){
                    date = 1;
                    month = month + 1;
                }
            }
        }
        else
            hou = hou + 9; //-9

        year = String(year);    month = String(month);
        hou = String(hou);  date = String(date);
    
		if(month.length==1) month = '0'+month;
		if(hou.length==1) hou = '0'+hou;
		if(date.length==1) date = '0'+date;
		if(hou.length==1) hou = '0'+hou;
		if(min.length==1) min = '0'+min;
		if(sec.length==1) sec = '0'+sec;
		if(milsec.length==1) milsec = '00'+milsec;
		else if(milsec.length==2) milsec = '0'+milsec;
        time = year + '-' + month + '-' + date + ' ' + hou + ':' + min + ':' + sec + '.' + milsec;

        if (data[i].cr == 'Sdongwon'){
			if(info=='flowRate'){
				flow = parseInt(data[i].con);
				ic_flow_sum += parseInt(data[i].con)*0.062+0.578;//String??
				ic_flow_len += 1;
			}
			else if(info=='co2'){
				emi=data[i].con;
				ic_co2_sum += parseInt(data[i].con);
				ic_flow_len += 1;
            }
            time_ic = time;
		}
        else if (data[i].cr == 'ShooN'){
            loc = '병점';
			if(info=='flowRate'){
                flow = parseInt(data[i].con);
				bj_flow_sum = bj_flow_sum+flow;
				bj_flow_len = bj_flow_len + 1;
				console.log('병점 ::: flow', bj_flow_sum, ' ::: length : ', bj_flow_len);
			}
			else if(info=='co2'){
                emi = parseInt(data[i].con);
				bj_co2_sum = bj_co2_sum + emi;
				bj_co2_len += 1;
				console.log('병점 ::: co2   ', bj_co2_sum, '::: length : ', bj_co2_len);
            }
            time_bj = time;
		}
        else{
            loc = '수원';
			if(info=='flowRate'){
				sw_flow_sum += parseInt(data[i].con)*0.062+0.578;
				sw_flow_len += 1;
			}
			else if(info=='co2'){
				sw_co2_sum += parseInt(data[i].con);
				sw_co2_len += 1;
            }
            time_sw = time;
        }
        
        //emi = emi*AREA*flow*6/100000
        json_obj = 0;
        const send_data = require('./send_data_toolkit.js');
        if(flow>0 && emi>0){
            flow = flow*0.062+0.578;
            emi = flow*AREA*emi*6/100000;
            json_obj = {
            'adate_time' : time_bj,	'emissions' : emi,
			'limestone' : emi*1.15/100*(Math.random()*(max-mini)+mini),
			'gypsum' : emi*0.03/100*(Math.random()*(max-mini)+mini),
			'clay' : emi/100*0.22*(Math.random()*(max-mini)+mini),
			'coal' : emi/100*0.12*(Math.random()*(max-mini)+mini),
			'silica_stone' : emi/100*0.05*(Math.random()*(max-mini)+mini),
			'iron_oxide' : emi*0.03/100*(Math.random()*(max-mini)+mini)};
            send_data.send_to_toolkit(json_obj);
			flow=0; emi=0;
        }
    }

	emi_bj = (bj_flow_sum/bj_flow_len)*AREA*(bj_co2_sum/bj_co2_len)*6/100000;
	//console.log('average flow :::::', (bj_flow_sum/bj_flow_len));
	//console.log('average co2 :::::', (bj_co2_sum/bj_co2_len));
	limestone = String(emi_bj*1.15*(Math.random()*(max-mini)+mini));
	gypsum = String(emi_bj*0.03*(Math.random()*(max-mini)+mini));
	clay= String(emi_bj*0.22*(Math.random()*(max-mini)+mini));
	coal = String(emi_bj*0.12*(Math.random()*(max-mini)+mini));
	silica_stone= String(emi_bj*0.05*(Math.random()*(max-mini)+mini));
	iron_oxide = String(emi_bj*0.03*(Math.random()*(max-mini)+mini));

	console.log('EMISSION : ', emi_bj, ' ::: LIMESTONE : ', limestone, ' ::: GYPSUM : ', gypsum, ' ::: CLAY : ', clay);

    emi_bj = String(emi_bj);
	//Considering second rewrite the formula
    if(emi_bj== 'NaN'){
		console.log("5. Failed to construct sql : NO FLOWRATE DATA \n");
	}
    else{
		sql_bj = 'insert into co2_emissions(date_time,emissions,location, limestone, clay, silica_stone, iron_oxide, gypsum, coal) values(' + '\'' + time_bj + '\'' + ',' + emi_bj + ',\'병점\','+limestone+','+clay+','+silica_stone+','+iron_oxide+','+gypsum+','+coal+')';

		ourdb_connection.query(sql_bj, function(error, results, fields){
			if(error)	console.log('5. ERROR DETETED when inserting info to sheroDB', sql_bj);
			else{
				console.log('5. Successfully inserted into sheroDB with sql : ', sql_bj);
				console.log('');
			}
		});
    }

    ourdb_connection.end();
}

global.getDataFromMobius = function (result) {
    let mobius_connection = mysql.createConnection(mobius_connInfo);

    date = result[0].time
	if(date==null)
		date = new Date(0);

    minute = date.getMinutes(); sec = date.getSeconds();
    milsec = date.getMilliseconds();
    year = date.getFullYear();  month = date.getMonth() + 1;
    day = date.getDate();   hou = date.getHours();

    if (hou < 9) {
        hou = hou - 9 + 24; //-9
        if (day == 1) {
            month = month - 1;
            if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10)
                day = 31;
            else if (month == 4 || month == 6 || month == 9 || month == 11)
                day = 30;
            else if (month == 0){
                month = 12;
                day = 31;
            }
            else
                day = 28;
            month = month;
            day = day;
        }
        else
            day = day - 1;
    }
    else {
        hou = hou - 9; //-9
        day = day;
    }

	year = String(year);	month = String(month);	day = String(day);
	hou = String(hou);		minute = String(minute);	sec=String(sec);
	milsec = String(milsec);

    if (month.length == 1) month = '0' + month;
    if (day.length == 1) day = '0' + day;
    if (hou.length == 1) hou = '0' + hou;
    if (minute.length == 1) minute = '0' + minute;
    if (sec.length == 1) sec = '0' + sec;
    if (milsec.length == 1) milsec = '00' + milsec;
    else if (milsec.length == 2) milsec = '0' + milsec;

    res = year + month + day + hou + minute + sec + milsec;
    //console.log('2. Converted date info (date_time -> 17 digit string) : ', res);
    //console.log('');

    let sql = 'SELECT ri, con, cr FROM cin WHERE right(ri, 17) > ' + res;

    mobius_connection.query(sql, function (error, results, fields) {
        if (!results) {
            console.log('');
            console.log('3. No matched ri with date string');
        }
        else {
            console.log('3. Date string matched result : ', sql, 'and length : ', results.length);
            console.log('');
            if (results.length > 0){
                writeDataToShero(results);
            }
        }
    });
    mobius_connection.end();
};

exports.mobius_to_shero = function () {
    let ourdb_connection = mysql.createConnection(ourdb_connInfo);
    //mobius_connection.connect();
    //ourdb_connection.connect();

    ourdb_connection.query('SELECT MAX(date_time) as time from co2_emissions', function (error, results, fields) {
        if (error) throw error;
        else {
            //console.log('1. Getting Max(date_time) from existing SheroDB : ', results);
            //console.log('');
            getDataFromMobius(results);
        }
    });
    ourdb_connection.end();    
};
