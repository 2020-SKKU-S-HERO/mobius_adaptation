const {PythonShell} = require('python-shell');

script_path = __dirname;
python_path = '';

let options = {
	mode : 'text',
	pythonPath : python_path,
	pythonOptions : ['-u'],
	scriptPath : script_path,
	args : []
};

PythonShell.run('prediction_model_bj.py',options ,function(err, result){
	if(err) throw err;
	console.log("Python result : ");
	
	console.log(result.length);
	console.log(result[419]);
	console.log('finsihed');
});

/*PythonShell.runString('x=1+1;print(x)',null,function(err){
	if(err) throw err;
	console.log('finished');
});
*/
