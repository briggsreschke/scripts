"""
File: aparse.py

GNU Public License

Parse Apache log file. regex pattern may need be altered to suit specfic log format
Includes optional user customizable routines for filtering log file records.

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
		

# Optional adaptable routines for filtering log records

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
	records = {}
	
	for r in arr:
		#ip address of host
		records['host'].append(get_host(r))
       	# Intact unix time stamp
		records['timestamp'].append(get_timestamp(r))
		#Parsed timestamp string
		records['time'].append(get_time(r))
		records['date'].append(get_date(r))
		records['timezone'].append(get_timezone(r))
		#Parsed method, path, protocol string
		records['method'].append(get_method(r))
		records['path'].append(get_path(r))
		records['protocol'].append(get_protocol(r))
		#Everything else
		records['status'].append(get_status(r))  
		records['bytes'].append(get_bytes(r))
		records['referer'].append(get_referer(r))
		records['agent'].append(get_agent(r))	
	
	return records

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
	
	dicts = {}
		
	try:
		# Parse records
		records = parse(LOG_FILE)
	except:
		print 'Unable to proccess log file'
		sys.exit(2) 
	try:
		# Get list of dicts
		r = get_dict(records)
		cnt = 0

		for key, value in r.iteritems():
			print value + '\n'
			cnt += 1
		
		print 'Processed ' + str(cnt) + ' records\n'
	except:
		print 'Parsing unsuccessful'
		sys.exit(1)
		
	sys.exit(0)

if __name__ == '__main__':
	
       main()
