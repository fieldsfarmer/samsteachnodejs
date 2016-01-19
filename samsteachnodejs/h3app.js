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