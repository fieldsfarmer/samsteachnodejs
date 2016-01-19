function havingBreakfast (food, drink, callback) {
	console.log('Having breakfast of ' + food + ', ' + drink);
	if(callback && typeof(callback)==='function'){
		callback();
	}
}

havingBreakfast('toast', 'coffee', function(){
	console.log('Finished breakfast. Now time to go to work!');
})