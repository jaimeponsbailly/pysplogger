#!/usr/bin/python3.4
'''
Created 2016-04-25

Author Jaime Pons

'''

import json
import time
from sys import argv
from urllib.request import urlopen
from pprint import pprint
from datetime import date
from datetime import datetime
import mysql.connector
from configPySpLogger import *

def create_insert():
	data=recupera_json("")
	numberApps=len(data)
	for i in range(numberApps):
		#print (data[i])
		name=data[i]["id"]
		time.sleep(0.8)
		data_jobs=recupera_json(name+"/jobs")
		#print ("JOBS: "+str(data_jobs))
		time.sleep(0.8)
		data_executors=recupera_json(name+"/executors")
		time.sleep(0.8)
		data_stages=recupera_json(name+"/stages")
		number_stages=len(data_stages)
		for k in range(number_stages):
			cadena=name+"/stages/"+str(k)
			time.sleep(0.8)
			if k > 0:
				iter(data_stages_json).next()[k]=recupera_json(name+"/stages/"+str(k))
			else:
				data_stages_json=recupera_json(name+"/stages/"+str(k))
		
		try:
			cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS,host=DB_HOST,database=DB_NAME)
			cursor = cnx.cursor()
			query="""SELECT app_footprint->"$.id" FROM data WHERE app_footprint->"$.id" = '%s'  """ % (data[i]["id"])
			cursor.execute(query)
			datos=cursor.fetchall()              # Hacer efectiva la escritura de datos 
			if len(datos) == 0:
				query="""INSERT INTO data (app_footprint,executors,jobs,stages) VALUE ( %s, %s, %s, %s )"""
				cursor.execute(query,(json.dumps(data[i]),json.dumps(data_executors),json.dumps(data_jobs),json.dumps(data_stages_json)))
				cnx.commit()              # Hacer efectiva la escritura de datos 
			cursor.close()
			cnx.close()
		except:
			print ("Error creating the query to insert JSON data type")
	

def recupera_json(path):
	data = ""
	try:
		url = 'http://'+IP_SERVER+':'+PORT+URL_GENERAL+path
		response = urlopen(url).read()
		response = response.decode('utf8')
		data = json.loads(response)
	except:
		print ("Error trying to get the JSON REST data from Spark interface.")
		
	return data



def main(args):
	try:
		create_insert()
	except KeyboardInterrupt:
        	print ("Ctrl-C")

if __name__ == '__main__':
    main(argv)
