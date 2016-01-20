// function havingBreakfast (food, drink, callback) {
// 	console.log('Having breakfast of ' + food + ', ' + drink);
// 	if(callback && typeof(callback)==='function'){
// 		callback();
// 	}
// }

// havingBreakfast('toast', 'coffee', function(){
// 	console.log('Finished breakfast. Now time to go to work!');
// })

////// read files
// var fs = require('fs'),
// 	filename = 'package.json';

// fs.readFile(filename, 'utf8', function(err, data){
// 	if(err) {
// 		// throw err;
// 		console.log('Got err: '+err.message);
// 	}
// 	else{
// 		console.log('File read');
// 		console.log(data);
// 	}
// });


////// synchronous /blocking (operation one at a time)
// function sleep(milliseconds){
// 	var start = new Date().getTime();
// 	while(new Date().getTime() - start < milliseconds){

// 	}
// };
// function fPage(){
// 	console.log('fetching page ...');
// 	sleep(2000);
// 	console.log('Got data from requesting page');
// }

// function fApi(){
// 	console.log('fetching api ...');
// 	sleep(2000);
// 	console.log('Got data from requesting api');
// }

// fPage();
// fApi();

////// asynchronous /none-blocking (because of callback)
// var http = require('http'),
// 	url = 'trafficjamapp.herokuapp.com',
// 	p = '/?delay=2000';

// function fetchPage(){
// 	console.log('fetching page ...');
// 	http.get({host : url, path : p}, function(res){
// 		console.log('Got data from requesting page');
// 	}).on('error', function(e){
// 		console.log('Got error: '+e);
// 	})
// };

// function fetchApi(){
// 	console.log('fetching api ...');
// 	http.get({host : url, path : p}, function(res){
// 		console.log('Got data from the api');
// 	}).on('error', function(e){
// 		console.log('Got error: '+e);
// 	})
// };

// fetchPage();
// fetchApi();