import mysql.connector
from twitter import *
import string
from datetime import date, datetime
import time
import paramiko

consumer_key = 'HLrxMgREPf045FIJtRz3WQAb8'
consumer_secret = 'atZvODDN2gysB61gfKBsCEnqBe1TV1jbSGvnleaUAoqx7ewGsg'
access_token = '2257147508-SuL04e6ZNka4zfYug4siBoOxTGfjXGoSkGU2knC'
access_token_secret = 'wvBGZHgV60zUSmRfrmE2oljKZIv9ZixaooHYNDxU1sTsN'

def get_trends():
	twitter = Twitter(auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))
	con = mysql.connector.connect(host='localhost', user='root', password='admin', database='598tar', autocommit=True)
	query_cursor = con.cursor(buffered=True)
	update_cursor = con.cursor(buffered=True)
	query_cursor.execute("SELECT * FROM city")
	for (WEOID, name) in query_cursor:
		print WEOID, name
		results = twitter.trends.place(_id = WEOID)
		for location in results:
			for trend in location["trends"]:
				print " - %s" % trend["name"]
				add_trend = ("INSERT INTO trend (text, WEOID, city_name, query_time) VALUES (%s, %s, %s, %s)")
				data_trend = (trend["name"], WEOID, name, datetime.now())
				update_cursor.execute(add_trend, data_trend)
			time.sleep(100);
	query_cursor.execute("SELECT text FROM trend GROUP by text")
	data = ''
	for (trend,) in query_cursor:
		data += trend + '\n'
	put_file('52.25.245.7', 'ubuntu', '/Users/Evan/.ssh/aws_pk/qifanwu.pem', '/home/ubuntu/cs598TAR-tweets-crawler/newTwitter', 'trends', data)
	query_cursor.close()
	update_cursor.close()
	con.close()

def put_file(hostname, username, keypath, dirname, filename, data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, key_filename=keypath)
    sftp = ssh.open_sftp()
    try:
        sftp.mkdir(dirname)
    except IOError:
        pass
    f = sftp.open(dirname + '/' + filename, 'w')
    f.write(data)
    f.close()
    ssh.close()

if __name__ == '__main__':
    get_trends()
