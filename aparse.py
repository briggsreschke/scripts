"""
File: aparse.py

GNU Public License

Parse Apache log file. regex pattern may need be altered to suit specfic log format
Includes optional, adaptable routines for filtering log file records.

"""

import sys
import re

LOG_REGEX = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'

#Field index values into each logfile record
HOST = 0
DATE = 1
TIME = 1
TZ = 1
METHOD = 2
PATH = 2
PROTOCOL = 2
STATUS = 3
BYTES = 4
REFERER_ = 5
AGENT = 6
		

# Optional, adaptable routines for filtering purposes

def host(arr):
	host = arr[HOST]
	return host

# Return the intact Unix time stamp
def get_timestamp(arr):
	timestamp = arr[TIME]     
	return timestamp

def get_time(arr):
	regex =  '^(\d+\/\w+\/\d+)((:\d\d)+)\s'
	
	pattern = re.compile(regex)
	match = pattern.match(arr[TIME])
	
	if not match:
		return 'unknown'
	return match.group(2)[1:]

def get_date(arr):
	regex = '^(\d+\/\w+\/\d+)'
	
	pattern = re.compile(regex)
	match = pattern.match(arr[DATE])
	
	if not match:
		return 'unknown'
	return match.group()		
	
def get_timezone(arr):
	regex =  '^(.+)(.+)(\s\S\d+)'
	
	pattern = re.compile(regex)
	match = pattern.match(arr[TZ])
	
	if not match:
		return 'unknown'
	return match.group(3)
	
def get_method(arr):
	# Could filter specific methods in the list
	method_list = ['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE', 'TRACE', 'CONNECT']
	tmp = arr[METHOD]
	method = tmp.split(' ')[0]
	
 	if not method:
 		return 'unknown'
	return method	
	
def get_path(arr):
	tmp = arr[PATH]
	regex = '[\/(\S*)]+'
	
	pattern = re.compile(regex)
	match = pattern.match(tmp.split(' ')[1])
	
	if not match:
		return 'unknown'
	return match.group()
	
def get_protocol(arr):
	tmp = arr[PROTOCOL]
	protocol = tmp.split(' ')[2]
	
	if not protocol:
		return 'unknown'
	return protocol

def get_status(arr):
	# Could filter only specific status codes
	status = arr[STATUS]

	if not status:
		return 'unknown'
	return status
	
def get_bytes(arr):	
	bytes = arr[BYTES]
	
	if not long(bytes):
		return '0'
	return bytes

def get_referer(arr):	
       # Possibly more to do here
	referer = arr[REFERER]
	
	if referer == '-':
		return 'unknown'
	return referer

def get_agent(arr):
	# Much more to possibly do here
	agent = arr[AGENT]
	
	if agent == '-':
		return 'unknwon'
	return agent

# Get dictionary of log records
def get_dict(arr):
	dic = {}
	

	#ip address of host
	dic['host'] = get_host(arr)
  	# Intact unix time stamp
	dic['timestamp'] = get_timestamp(arr)
	#Parsed timestamp string
	dic['time'] = get_time(arr)
	dic['date'] = get_date(r)
	dic['timezone'] = get_timezone(arr)
	#Parsed method, path, protocol string
	dic['method'] = get_method(arr)
	dic['path'] = get_path(r)
	dic['protocol'] = get_protocol(arr)
	#Everything else
	dic['status'] = get_status(arr)  
	dic['bytes'] = get_bytes(arr)
	dic['referer'] = get_referer(arr)
	dic['agent'] = get_agent(arr)	
	
	return dic

def parse(fname):	
	arr = []

	try:
		# Read in records and parse them against regex 
		with open(fname, 'r') as f:
			line = f.readline().replace('\n', '')
			while (line):
				result = list(re.match(_LOG_REGEX_, line).groups())
				arr.append(result)
				line = f.readline().replace('\n', '')
			f.close()
		return arr
	except:
		return []

#!/usr/bin/python

import sys
import aparse

# Path to log file on mac
LOG_FILE = '/private/var/log/apache2/access.log'

def main():
	
	dic = {}
	cnt = 0
		
	try:
		# Parse records
		arr = parse(LOG_FILE)
	except:
		print 'Unable to proccess log file'
		sys.exit(2) 
	try:
		# Print records
		for r in arr		
			dict = get_dict(r)
			for key, value in iteritems(dict):
				print key + ' : ' + value + '\n'
			cnt += 1
		
		print 'Processed ' + str(cnt) + ' records\n'
	except:
		print 'Parsing unsuccessful'
		sys.exit(1)
		
	sys.exit(0)

if __name__ == '__main__':
	
       main()
