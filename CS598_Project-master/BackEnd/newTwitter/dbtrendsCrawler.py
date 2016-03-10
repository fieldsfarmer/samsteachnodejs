import mysql.connector
from twitter import *
import string
from datetime import date, datetime
import time

consumer_key = 'HLrxMgREPf045FIJtRz3WQAb8'
consumer_secret = 'atZvODDN2gysB61gfKBsCEnqBe1TV1jbSGvnleaUAoqx7ewGsg'
access_token = '2257147508-SuL04e6ZNka4zfYug4siBoOxTGfjXGoSkGU2knC'
access_token_secret = 'wvBGZHgV60zUSmRfrmE2oljKZIv9ZixaooHYNDxU1sTsN'

con = mysql.connector.connect(host='mysql-instance2.clmkxxojx4h6.us-west-2.rds.amazonaws.com', port='10001', user='tar', password='uiuctar598', database='598', autocommit=True)
twitter = Twitter(auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

def get_trends():
	query_cursor = con.cursor(buffered=True)
	update_cursor = con.cursor(buffered=True)
	query = ("SELECT * FROM city")
	query_cursor.execute(query)
	for (WEOID, name) in query_cursor:
		print WEOID, name
		results = twitter.trends.place(_id = WEOID)
		for location in results:
		 	print location	
			for trend in location["trends"]:
				print " - %s" % trend["name"]
				add_trend = ("INSERT INTO trends (trend, WEOID, city_name, query_time) VALUES (%s, %s, %s, %s)") 
				data_trend = (trend["name"], WEOID, name, datetime.now())	
				#update_cursor.execute(add_trend, data_trend)
			#time.sleep(100);
	#con.commit()
	query_cursor.close()
	update_cursor.close()
	con.close()

if __name__ == '__main__':
    get_trends()
