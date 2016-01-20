var http = require('http'),
	urls = ['apple.com', 'amazon.com', 'yahoo.com'];

function fetchPage (url) {
	// var start = new Date();
	// http.get({host: url}, function(res){
	// 	console.log("Got respsonse from: "+url);
	// 	console.log('The status code is '+res.statusCode);
	// 	console.log("It took: ", new Date() - start, 'ms');
	// }).on('error', function(e){
	// 	console.log('Got error: '+e.message);
	// });

	// http.get('http://www.google.com/index.html', (res) => {
	http.get({host: url}, (res) => {		
	  console.log(`Got response: ${res.statusCode}`);
	  // consume response body
	  res.resume();
	}).on('error', (e) => {
	  console.log(`Got error: ${e.message}`);
	});
}


for(var i=0; i<urls.length; i++){
	fetchPage(urls[i]);
}