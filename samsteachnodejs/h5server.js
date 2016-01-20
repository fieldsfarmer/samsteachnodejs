var http = require('http');
http.createServer((req, res)=>{
	res.writeHead(301, {
		location: 'http://www.google.com'
	});
	res.end();
}).listen(3000, '127.0.0.1');
console.log('server running at http://127.0.0.1:3000/');