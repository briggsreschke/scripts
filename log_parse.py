'''
File: log_parse - (Apache log file parser) - GNU Public License
reschke.briggs@gmail.com

Parse Apache log file. regex pattern may need be altered to suit specfic log format
Includes optional user adaptable routines for further parsing of each field.
'''

import sys
import re

# Constants
_VERBOSE_ = True 

_LOG_REGEX_ = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'

# Field index values into each logfile record
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

def log_host(arr):
	host = arr[_HOST_]
	
	if not host: 
		return 'none'
	return host

def log_id(arr):
        id = arr[_ID_]
 
        if id == '-':
	       return 'none'
	return id
	
def log_user(arr):
	user = arr[_USER_]
	
	if user == '-':
		return 'none'
	return user

# Still need to do date and time parsing

def log_date(arr):
	date = arr[_DATE_]
	return date

# Need some Regex to parse date and time field	
					
def log_time(arr):
	time = arr[_TIME_]
	return time

# And time zone

def log_tz(arr):
        tz = arr[_TZ_]
        return tz

def log_method(arr):
	method_list = ['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE', 'TRACE', 'CONNECT']
	
	tmp = arr[_METHOD_]
	method = tmp.split(' ')[0]

	if method not in method_list:
		return 'unknown'
	return method	

def log_path(arr):
	tmp = arr[_PATH_]
	regex = '[\/(\S*)]+'
	
	pattern = re.compile(regex)
	match = pattern.match(tmp.split(' ')[1])
	
	if not match:
		return 'none'
	return match.group()

def log_protocol(arr):
	tmp = arr[_PROTOCOL_]
	protocol = tmp.split(' ')[2]

def log_status(arr):
	# Could check against a list of all status codes
	status = arr[_STATUS_]
	
	if not status:
		return 'none'
	return status

def log_bytes(arr):	
	bytes = arr[_BYTES_]
	
	if not long(bytes):
		return '0'
	return bytes

def log_referer(arr):	
	referer = arr[_REFERER_]
	
	if referer == '-':
		return 'none'
	return referer

def log_agent(arr):
	# Much more to possibly do here
	agent = arr[_AGENT_]
	
	if agent == '-':
		return 'none'
	return agent


# ---------------------------------------------------------------------
	
# Entry point. Main loop

def log_parse(fname):	
	arr = []
	dicts = []
	
	try:
		# Read in records and parse them against regex 

		with open(fname, 'r') as f:
			line = f.readline().replace('\n', '')
			while (line):
				result = list(re.match(_LOG_REGEX_, line).groups())
				arr.append(result)
				line = f.readline().replace('\n', '')
			f.close()
	        # return fields as an array of lists. One for each record
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
			print log_host(line)
			print log_method(line)
			
		print 'processed ' + str(len(records)) + ' records' 
	
	sys.exit(0)
