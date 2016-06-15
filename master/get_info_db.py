#!/usr/bin/python3.4 -u

'''
Created 2016-5-24

Author Jaime Pons

'''

import mysql.connector
import time 
import json
from pprint import pprint
from sys import argv
from datetime import date
from datetime import datetime
from configPySpLogger import *

def get_info(lastId=0):
	#try:
		#query="""SELECT executors->"$[0].id" FROM data """
		#query="""SELECT app_footprint->"$.attempts[0].endTime" FROM data """
		query="""SELECT id, app_footprint->"$.id", app_footprint->"$.name", app_footprint->"$.attempts[0].startTime", app_footprint->"$.attempts[0].endTime" FROM data WHERE id > %d """ % (lastId)
		#query="""SELECT * FROM data """
		##print (query)
		cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,host=DB_HOST,database=DB_NAME)
		cursor = cnx.cursor()
		cursor.execute(query)
		data=cursor.fetchall() 
		cursor.close()
		cnx.close()
		#print (data)
		if len(data) == 0:
			lastID=lastId
		else:
			lastID=print_result(data)
			#print("LAST ID---------"+str(lastID))
		time.sleep(5)
		return lastID
	#except:
	#	print ("Error creating the query to get JSON data")



def print_result(data):
	for row in data:
		#print("{", end="")
		start_milli = dateToTimestamp(row[3].strip('\"'))
		end_milli = dateToTimestamp(row[4].strip('\"'))
		start = dateToGoogleDate(row[3].strip('\"'))
		end = dateToGoogleDate(row[4].strip('\"'))
		diff = (int(end_milli) - int(start_milli))
		#json_bourne = ' { "taskId": "' + str(row[0]) +'", "taskName": ' + row[1] +', "resource": ' + row[2] +', "start": ' + str(start) +', "end": ' + str(end) +', "duration": ' + str(diff)  +', "percent_complete": 100, "dependencies": "null" } ' ;
		json_bourne = ' { "taskId": "' + str(row[0]) +'", "taskName": ' + row[1] +', "resource": ' + row[2] +', "start": ' + row[3] +', "end": ' + row[4] +', "duration": ' + str(diff)  +', "percent_complete": 100, "dependencies": "null" } ' ;
		print (json_bourne)

		##fin=len(row)
		##toNumber= (fin - 1)
		##inicio=0
		ret=row[0]
		##for y in row:
		##	inicio += 1
		##	if toNumber <= inicio:
		##		y = '\"'+str(dateToTimestamp(y.strip('\"')))+'\"'
		##	
		##	if inicio == fin:
		##		print(str(y), end="")
		##	else:
		##		print(str(y)+",", end="")
		##print("}")
		#print()
	return ret

def dateToTimestamp(fecha_orig): 
	datetime1 = datetime.strptime(fecha_orig, "%Y-%m-%dT%H:%M:%S.%fGMT")
	#print(datetime1)
	timestamp1=datetime1.timestamp()
	timestamp1*=1000
	return int(timestamp1)

def dateToGoogleDate(orig_date):
	dateTime = datetime.strptime(orig_date, "%Y-%m-%dT%H:%M:%S.%fGMT")
	toMilli=dateTime.strftime("%f") # This value is in microseconds
	toMilli=int(toMilli)/1000
	timeRet= dateTime.strftime("%Y, %m, %d, %H, %M, %S")
	timeRet =timeRet+", "+str(int(toMilli))
	return timeRet


def main(args):
	try:
		lastID=0
		while [1]:
			lastID=get_info(lastID)
	except KeyboardInterrupt:
        	print ("Ctrl-C")

if __name__ == '__main__':
    main(argv)


