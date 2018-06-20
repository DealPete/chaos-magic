var http = require('http');

http.createServer(function(req,res){
    var path = req.url.replace(/\/?(?:\?.*)?$/,'').toLowerCase();
    //res.write(path);
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.write(path+'\n');
    switch(path){
        case '':           
            res.end('hullo everyone');
            break;
        case '/about':
            res.end('about what?');
            break;
        default:
            res.end('duh');
            break;
    }  
}).listen(3000);

console.log('Server at http://localhost:3000; Ctrl-C to end');
