//This would be locally
//npm install [module] 
//This would be globally
//npm install -g [module]

// h1
var http = require('http');
http.createServer(function(req, res){
	res.writeHead(200, {'Content-Type':'text/plain'});
	res.end('Hello world!\n');
}).listen(3000, '127.0.0.1');
console.log('Server is running at http://127.0.0.1:3000/');

// h3 calculate the time of fetching webpages from some urls
var http = require('http'),
	urls = ['apple.com', 'amazon.com', 'yahoo.com'];

function fetchPage (url) {
	var start = new Date();
	http.get({host: url}, function(res){
		console.log("Got respsonse from: "+url);
		console.log("It took: ", new Date() - start, 'ms');
	});
}
for(var i=0; i<urls.length; i++){
	fetchPage(urls[i]);
}


