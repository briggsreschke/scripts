"""
File: aparse.py

GNU Public License

Parse Apache log file. regex pattern may need be altered to suit specfic log format
Includes optional user customizable routines for filtering records or error checking.

"""

import sys
import re
import aparse

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
		

# Optional adaptable routines for error checking or filtering individual log records

def get_host(arr):
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
	dictionaries = []
	dict = {}
	
	for r in arr:
		dict['host'] = get_host(r)
       # Intact unix time stamp
		dict['timestamp'] = get_timestamp(r)
		dict['time'] = get_time(r)
		dict['date'] = get_date(r)
		dict['timezone'] = get_timezone(r)
		dict['method'] = get_method(r)
		dict['path'] = get_path(r)
		dict['protocol'] = get_protocol(r)
		dict['status'] = get_status(r)  
		dict['bytes'] = get_bytes(r)
		dict['referer'] = get_referer(r)
		dict['agent'] = get_agent(r)
		
		dictionaries.append(dict)	
	
	return dictionaries

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
	
	dictionaries = []
		
	try:
		# Parse records
		records = aparse.parse(LOG_FILE)
	except:
		print 'Unable to proccess log file'
		sys.exit(2)
	 
	try:
		# Get list of dicts
		dictionaries = aparse.get_dict(records)
		
		for i in range(len(dictionaries)):
			print dictionaries[i]
		print 'Processed ' + str(len(dictionaries)) + ' records\n'
	except:
		print 'Parsing unsuccessful'
		sys.exit(1)
		
	sys.exit(0)

if __name__ == '__main__':
	
       main()
