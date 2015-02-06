'''
File: plog.py - (Apache log file parser) - GNU Public License
reschke.briggs@gmail.com

Parse Apache log file. regex pattern may need be altered to suit specfic log format
'''

import sys
import re

# Constants
_VERBOSE_ = True 

# Index values into each logfile record
_HOST_ = 0
_ID_ = None 
_USER_ = None 
_DATE_ = 1
_TIME_ = 1
_TZ_ = 1
_METHOD_ = 2
_PATH_ = 2
_PROTOCOL_ = 2
_STATUS_ = 3
_BYTES_ = 4
_REFERER = 5
_AGENT_ = 6



# ---------------------------------------------------------------------
# Optional routines for individual error checking or manipulation of
# log records

def log_get_host(arr):
	host = arr[_HOST_]
	
	if not host: 
		return 'none'
	return host

def log_get_id(arr):
	id = arr[_ID_]
	
	if id == '-':
		return 'none'
	return id
	
def log_get_user(arr):
	user = arr[_USER_]
	
	if user == '-':
		return 'none'
	return user

# Still need to do date and time parsing
def log_get_date(arr):
	date = arr[_DATE_]
	return date
			
			
def log_get_time(arr):
	time = arr[_TIME_]
	return time
	
def log_get_method(arr):
	method_list = ['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE', 'TRACE', 'CONNECT']
	
	tmp = arr[_METHOD_]
	method = tmp.split(' ')[0]

	if method not in method_list:
		return 'unknown'
	return method	


def log_get_path(arr):
	tmp = arr[_PATH_]
	regex = '[\/(\S*)]+'
	
	pattern = re.compile(regex)
	match = pattern.match(tmp.split(' ')[1])
	
	if not match:
		return 'none'
	return match.group()
	

def log_get_protocol(arr):
	tmp = arr[_PROTOCOL_]
	protocol = tmp.split(' ')[2]


def log_get_status(arr):
	# Could check against a list of all status codes
	status = arr[_STATUS_]
	
	if not status:
		return 'none'
	return status
	

def log_get_bytes(arr):	
	bytes = arr[_BYTES_]
	
	if not long(bytes):
		return '0'
	return bytes


def log_get_referer(arr):	
	referer = arr[_REFERER_]
	
	if referer == '-':
		return 'none'
	return referer


def log_get_agent(arr):
	# Much more to possibly do here
	agent = arr[_AGENT_]
	
	if agent == '-':
		return 'none'
	return agent


# ---------------------------------------------------------------------
	
# Entry point. Main loop

log_regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'

def log_parse(fname):	
	arr = []
	dicts = []
	
	try:
		# Read parse them against regex return them as an array of lists 
		with open(fname, 'r') as f:
			line = f.readline().replace('\n', '')
			while (line):
				result = list(re.match(log_regex, line).groups())
				arr.append(result)
				line = f.readline().replace('\n', '')
			f.close()
	
		return arr
	except:
		if _VERBOSE_:
			print 'Error processing log file: ' + fname
		sys.exit(2)
	

#--------------------------------- main() -----------------------------

_TESTING_ = True

if __name__ == '__main__':
	
	if _TESTING_:
		try:
			records = log_parse('access.log')
		except:
			print 'Unable to proccess log file'
			sys.exit(1)
		
		for line in records:
			#print line
			print log_get_host(line)
			print log_get_method(line)
			
		print 'processed ' + str(len(records)) + ' records' 
	
	sys.exit(0)
