let {PythonShell} = require('python-shell');

let options = {
	mode : 'text',
	pythonPath : '',
	pythonOptions : ['-u'],
	scriptPath : '',
	args : []
};

PythonShell.run('hooN_model.py',options,function(err){
	if(err) throw err;
	console.log('finsihed');
});

/*PythonShell.runString('x=1+1;print(x)',null,function(err){
	if(err) throw err;
	console.log('finished');
});
*/
