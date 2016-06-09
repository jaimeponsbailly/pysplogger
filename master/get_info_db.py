#!/usr/bin/python3.4

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
	try:
		#query="""SELECT executors->"$[0].id" FROM data """
		#query="""SELECT app_footprint->"$.attempts[0].endTime" FROM data """
		query="""SELECT id, app_footprint->"$.id", app_footprint->"$.name", app_footprint->"$.attempts[0].startTime", app_footprint->"$.attempts[0].endTime" FROM data WHERE id > %d """ % (lastId)
		#query="""SELECT * FROM data """
		print (query)
		cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,host=DB_HOST,database=DB_NAME)
		cursor = cnx.cursor()
		cursor.execute(query)
		data=cursor.fetchall() 
		cursor.close()
		cnx.close()
		print (data)
		if len(data) == 0:
			lastID=lastId
		else:
			lastID=print_result(data)
			print("LAST ID---------"+str(lastID))
		time.sleep(5)
		get_info(lastId=lastID)
	except:
		print ("Error creating the query to get JSON data")



def print_result(data):
	for row in data:
		print("{", end="")
		fin=len(row)
		toNumber= (fin - 1)
		inicio=0
		ret=row[0]
		for y in row:
			inicio += 1
			if toNumber <= inicio:
				y = '\"'+str(dateToTimestamp(y.strip('\"')))+'\"'
				
			#	y="\""+dateToTimestamp(y)+"\""
			
			if inicio == fin:
				print(str(y), end="")
			else:
				print(str(y)+",", end="")
		print("}")
		#print()
	return ret

def dateToTimestamp(fecha_orig): 
	datetime1 = datetime.strptime(fecha_orig, "%Y-%m-%dT%H:%M:%S.%fGMT")
	#print(datetime1)
	timestamp1=datetime1.timestamp()
	timestamp1*=1000
	return int(timestamp1)



def main(args):
	try:
		get_info()
	except KeyboardInterrupt:
        	print ("Ctrl-C")

if __name__ == '__main__':
    main(argv)


