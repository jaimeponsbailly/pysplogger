#!/usr/bin/python3.4

'''
Created 2016-5-24

Author Jaime Pons

'''

import mysql.connector
from pprint import pprint
from sys import argv
from datetime import date
from datetime import datetime
from configPySpLogger import *

def get_info():
	#try:
		#query="""SELECT executors->"$[0].id" FROM data """
		#query="""SELECT app_footprint->"$.attempts[0].endTime" FROM data """
		query="""SELECT app_footprint->"$.id", app_footprint->"$.name", app_footprint->"$.attempts[0].startTime", app_footprint->"$.attempts[0].endTime" FROM data """
		#query="""SELECT * FROM data """
		cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,host=DB_HOST,database=DB_NAME)
		cursor = cnx.cursor()
		cursor.execute(query)
		data=cursor.fetchall() 
		cursor.close()
		cnx.close()
		print_result(data)
	#except:
	#	print ("Error creating the query to get JSON data")



def print_result(data):
	for row in data:
		print("{", end="")
		fin=len(row)
		toNumber= (fin - 1)
		inicio=0
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


