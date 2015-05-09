'''
csvtool.py - simple delete rows and cols from a csv, and extra build a json document

'''

import sys
import os.path
import re

TESTING = 1

# ------------------------------------------------------------	
#Deletes columns (row[column]) from list of col numbers

def delete_cols(ifile, ofile, cols, header, delimiter): 	
	
	# Open the files		
	try:
		ip= open(ifile)
	except:
		print 'Could not open input file in delete_cols()'
		sys.exit(15)

	# Test to see if out file exists before creating one
	if os.path.isfile(ofile) and not TESTING:
		print 'Output file already exists'
		exit(14)
	else:
		try:
			op = open(ofile,'w+')
		except:
			print 'Could not open output file in delete_cols()'
			sys.exit(13)
	
	count = 0			
	
	# Skip a line and save header if there is one
	try:
		if header:
			line = ip.readline()
			head = line.split(delimiter)
	except:
		print 'Nothing to read.'
		sys.exit(12)
		
	# Is there anything to read
	try:	
		line = ip.readline()
	except:
		print 'Nothing to read.'
		sys.exit(11)
	
	while line:
		# get delimited row into a list
		row = line.split(delimiter)
		
		# Delete rows provided in cols list
		for idx, column in enumerate(cols):
			column -= idx
			del row[column]		
			# Get rid of header labels for deleted cols
			if header:
				del head[column]
	
		# if header, replace with new one
		if header and count == 0:
			op.write(delimiter.join(head))
		
		# write the row with elimnated cols
		op.write(delimiter.join(row))
		
		# next record
		line = ip.readline()
		count += 1
	
	ip.close()
	op.close()				

	return count

# ------------------------------------------------------------	
# Deletes rows (skips them) if regex do not match cells

def delete_rows(ifile, ofile, mdict, header, delimiter):
	
	# Open the files		
	try:
		ip = open(ifile)
	except:
		print 'Could not open input file in delete_rows()'
		sys.exit(10)

	# Test to see if out file exists before creating one
	if os.path.isfile(ofile) and not TESTING:
		print 'Output file already exists'
		sys.exit(9)
	else:
		try:
			op = open(ofile,'w+')
		except:
			print 'Could not open output file in delete_rows()'
			sys.exit(8)
			
	count = 0			
	# innocent until proven guilty
	is_match = True
	
	# Save header skip a line if there is one
	try:
		if header:
			head = ip.readline()
	except:
		print 'Nothing to read.'
		sys.exit(7)
		
	# is there anything to read
	try:	
		line = ip.readline()
	except:
		print 'Nothing to read.'
		sys.exit(6)

	while line:
		# get delimited row into list
		row = line.split(delimiter)
		
		# iterate through key:value pairs {column number:regex}
		for key, value in mdict.iteritems():
			# if cell *does not* match against regex, delete row
			p = re.compile(value)				
			if not p.match(row[key]):
				is_match = False 
				break
		
		# if all matches are good, write the row
		if is_match == True:	
			# put the header back
			if header and count == 0:
				op.write(head)
			# write the row
			op.write(delimiter.join(row))
			
			count += 1
		else:
			# innocent until proven guilty
			is_match = True 
		# next line			
		line = ip.readline()
	
	ip.close()
	op.close()					

	return count

# -----------------------------------------------------------------	
# Inserts a header. Only useful if there never was one

def insert_header(ifile, hlist, delimiter):

	if not os.path.isfile(ifile):
		print 'Input file ' + ifile + ' does not exist'
		sys.exit(5)
	
		
# -----------------------------------------------------------------	
# Make a json document from csv

def to_json(ifile, ofile, header, delimiter):
	# Create utf-8 json from csv
	print
				
def main():
	
	if TESTING:
		cols = [2,3, 7, 8, 9, 10, 13, 14]
		cn = delete_cols('csv-testdata.csv', 'col-test.csv', cols, False, ',')
	
		print '\nProcessed ' + str(cn) + ' records'
	
		dict = {3:'^(SP|NP|NF)$'}
		rn = delete_rows('col-test.csv', 'row-test.csv', dict, False, ',')

		print 'Deleted ' + str(cn-rn) + ' rows'

if __name__ == '__main__':
	
	main()
	sys.exit(0)
			
