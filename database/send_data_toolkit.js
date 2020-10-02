//exports
exports.send_to_toolkit = function(data){
    const options = {
        url : 'http://129.254.221.107:8895',
        headers : 'Content=Type:application/json',
        json : true,
        body : data
    }

    request = require('request');

    request.post(options, function(error, res, body){
        if(error)
            console.log(error);
        else{
            console.log(body);
        }
    });
}