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

PythonShell.run('price_scrapping.py',options ,function(err, result){
	if(err) throw err;
	console.log("Python result : ");
	
	console.log(result);
	console.log('finsihed');
});


