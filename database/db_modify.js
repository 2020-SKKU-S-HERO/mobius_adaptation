
let {PythonShell} = require('python-shell');

let options = {
    mode: 'text',
    pythonPath : '',
    pythonOptions: ['-u'],
    scriptPath: '',
    args: ['value1', 'value2', 'vlaue3']   
};

PythonShell.run(__dirname+'\\test.py', options, function(err, results){
    if(err) throw err;

    console.log('results: %j', results);

});

/*
PythonShell.end(function(err, code, signal){
    if(err) throw err;

    console.log('The exit code was : ' + code);
    console.log('The exit signal was: '+ signal);
    console.log("end of python shell");
});
*/