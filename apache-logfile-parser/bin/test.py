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
