var all_tags = {};
var all_tags_1 = {};
var word_list = [
        // {text: "MTVStars", weight: 11, link: "https://jquery.com"},
      ];
var word_list_1 = [];
var geocoder;
var map;
var address_list = {};

$(document).ready(function(){
    $("#toggleView").toggle(function(){
        $("#tag_cloud_rate").hide();
        $("#tag_cloud_tweets").show();
        $("#cloud_title").text("Tag Cloud on Tweets Number");
    }, function(){
        $("#tag_cloud_rate").show();
        $("#tag_cloud_tweets").hide();
        $("#cloud_title").text("Tag Cloud on Tweets Controversial Rate");
    });

    $(window).on('hashchange', function() {
       if (window.location.hash == '') {
            goBack();
       }
    });

    //get the location for all tags and save them in a JSON object
    $.get('text/test.txt', function(data) {
        // console.log(address_list);
        var array = data.split('\n');

        for(var i = 0; i < array.length; i++){
            var line = array[i];
            var tagName = line.split(':')[0];
            var cities = line.split(':')[1];
            // console.log(value);

            tagName = parseTagName(tagName);
            // console.log(tagName);

            if(!address_list.hasOwnProperty(tagName)){
                address_list[tagName] = cities;
            }
        }
    });

    // show the tag cloud based on Controversial Rate
    $.get('text/result.txt', function(data) {

        var array = data.split('\n');

        for(var i = 0; i < array.length; i++){
            var line = array[i];
            var tags = line.split(':')[0];

            getTagList(all_tags, tags, line);
        }

        for(var tag in all_tags){
            var obj = {text: tag, weight: all_tags[tag], link: {href: '#' + tag + '_' + all_tags[tag],
            onclick:    'showTagPage($(this).text());' +
                        '$("#tagName").text($(this).text());' +
                        '$("#conRate").text(all_tags[$(this).text()]);' +
                        'initialize($(this).text());'

            }};

            word_list.push(obj);
        }

        $("#tag_cloud_rate").jQCloud(word_list);
    });

    // show the tag cloud based on tweets numbers
    $.get('text/count.txt', function(data) {
        var array = data.split('\n');

        for(var i = 0; i < array.length; i++){
            var line = array[i];
            var tags = line.split(':')[0];
            // console.log(line.split(':')[1]);

            getTagList(all_tags_1, tags, line);
        }

        for(var tag in all_tags_1){
            if(tag.substring(0, 1) === '#'){
                var tag_truncated = tag.substring(1);
            }

            var obj = {text: tag_truncated, weight: all_tags_1[tag], link: {href: '#' + tag_truncated + '_' + all_tags_1[tag],
            onclick:    'showTagPage($(this).text());' +
                        '$("#tagName").text($(this).text());' +
                        '$("#conRate").text(all_tags[$(this).text()]);' +
                        'initialize($(this).text());'

            }};

            word_list_1.push(obj);
        }

        $("#tag_cloud_tweets").jQCloud(word_list_1);
    });

});

//The effect of go back button
function goBack() {
    $("#tag_info").hide();
    $("#tag_cloud_rate").show();
    $("#toggleView").show();
    $("#cloud_title").show();
    $("#cloud_title").text("Tag Cloud on Tweets Controversial Rate");
}

function getTagList(all_tags, tags, line){
    if(!all_tags.hasOwnProperty(tags)){
        all_tags[tags] = line.split(':')[1];
    }
}

//function to show the all the tags on the web
function showTagPage(tag){
    $("#tag_body").empty();
    $("#tag_info").show();
    $("#tag_cloud_tweets").hide();
    $("#tag_cloud_rate").hide();
    $("#toggleView").hide();
    $("#cloud_title").hide();

    $.get('sampled/' + tag, function(data) {
        var tweets = data.split("\n");
        var uniqueTweets = [];
        // $.each(tweets, function(i, el){
        //     if($.inArray(el, uniqueTweets) === -1) uniqueTweets.push(el);
        // });

        for(var i = 0; i < tweets.length - 1; i++){
            $("#tag_body").append('<p style="font-size:20px;">' + (i + 1) + ":\t" + tweets[i] + '</p>');
        }
    });
}

//function to convert the tagName in the text file to the format shown on the web
function parseTagName(tagName){
    if(tagName.substring(0, 1) === '#') {
        tagName = tagName.substring(1);
    }

    var tagArray = tagName.split(" ");

    var parsedName = "";

    for(var i = 0; i < tagArray.length; i++){
        if(i == tagArray.length - 1){
            parsedName += tagArray[i];
        } else {
            parsedName += tagArray[i] + "_";
        }
    }

    return parsedName;
}

//function to display google map using google map API
function initialize(tag) {
    //geocoder = new google.maps.Geocoder();
    var mapOptions = {
        center : new google.maps.LatLng(40.7127, -74.0059),
        zoom : 5,
        mapTypeId : google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);

    codeAddress(tag);
}

//function that tranfer name city to place in the map
function codeAddress(tag) {
    geocoder = new google.maps.Geocoder();
    var locations;

    if(address_list.hasOwnProperty(tag)){
        locations = address_list[tag];
    }

    locations = eval(locations);

    //var address_list = {'Yonkers': '+', 'Clifton': '-', 'New Rochelle': '-', 'Denville': '-', 'Montclair': '+'};
    for(var address in locations) {
        console.log(locations[address]);
        geocoder.geocode({'address': locations[address]}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
                /*if (value == '+') {
                    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png')
                }*/
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }
}





