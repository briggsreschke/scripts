'''
--------------------------------------------------------------------
csvm.py - Ver 1.0 - Last updated 5.9.2015

Simple merge and delete operations for csv files.

Uses regular expressions as delete criteria for columns:
	dict = {colnum:pattern, ...}

For row deletion uses a list of row numbers:
	list = [row1, row2, ...]

--------------------------------------------------------------------
'''

import sys
import os.path
import re

TESTING = 1
		
# ------------------------------------------------------------------	
#Deletes columns (row[column]) from list of col numbers

def delete_cols(data, cols, header): 	
	
	# Make sure input file had data in it
	if not len(data):
		print 'No data to process in delete_cols()'
		sys.exit(6)
	
	# Make sure number of columns does not exceed the data cols
	if len(cols) > len(data):
		print 'cols is greater than columns in data.'
		sys.exit(5)
			
	count = 0
	tmp = [] * len(data)

	# if there is a header, save it
	if header:
		head = data[0]
	
	for row in data:
		# Delete rows provided in cols list
		for idx, column in enumerate(cols):
			column -= idx
			del row[column]		

			# if header delete column name of delete column
			if header:
				del head[column]

		# write header if there is one
		if header and count == 0:
			tmp.append(head)
			#op.write(delimeter.join(head))
		else:	
			# write the row with elimnated cols
			tmp.append(row)

		count += 1			

	return tmp

# -----------------------------------------------------------------	
# Deletes rows (skips them) if regex do not match cells

def delete_rows(data, dic, header):
	
	# Make sure the input file had data in it
	if not len(data):
		print 'No data to process in delete_rows()'
		sys.exit(3)

	tmp = []
	count = 0			
	is_match = False
	
	# Save header and increment count
	if header:
		head = data[0]
	
	for row in data:	
		# iterate through {column number:regex}
		for key, value in dic.iteritems():
			# match agains't regex. If no match, skip.
			p = re.compile(value)				
			if not p.match(row[key]):
				is_match = False
				break
			else:
				is_match = True

		# if all matches are good, write the row
		if is_match == True:	
			# put the header back
			if header and count == 0:
				tmp.append(head)
			# write the row
			else:
				tmp.append(row)
			
			is_match = False		
		count += 1			

	return tmp

# -------------------------------------------------------------------
# Merge multiple csv files

def merge_files(file_list, ofile):
	
	if os.path.isfile(ofile):
		print 'Ouput file already exists'
		sys.exit(4)

	try:
		op = open(ofile, 'w+')
	except:
		print "Unable to open output file in merge_files()"
		sys.exit(3)

	count = 0	
	for f in file_list:		
		try:
			ip = open(f)
		except:
			continue		
		
		line = ip.readline()
		while(line):
			op.write(line)
			count += 1
			line = ip.readline()
		ip.close()
	
	op.close()
	
	return count

#--------------------------------------------------------------------
# Write to new csv file

def write_data(data, fname, delimiter):

	# Check to see if file exists
	if os.path.isfile(fname):
		print 'output file already exists'
		sys.exit(7)
	# Open output file
	try:
		op = open(fname, 'w+')
	except:
		print 'Problem creating output file'
		exit(6)
	# Write data to output 
	for val in data:
		op.write(delimiter.join(val))

	op.close()

#--------------------------------------------------------------------
# Read data into list

def read_data(fname, delimiter):
	data = []
	
	try:
		ip = open(fname)
	except:
		print 'Could not open input file in get_data()'
		sys.exit(7)
	
	#Read data into a list 
	line = ip.readline()	
	while(line):
		data.append(line.split(delimiter))
		line = ip.readline()
	
	ip.close()
	return data		
		

# --------------------------------------------------------------------	
# Main

def main():

	# Read data
	data = read_data('test-in.csv', ',')
	
	# Remove columns using column numbers provided by list
	cols = [2, 3, 7, 8, 9, 10, 13, 14]
	data = delete_cols(data, cols, False)

	# Delete rows - dict with column num and regex pattern for match
	dict = {3:'^(SP|NP|NF)$'}
	data = delete_rows(data, dict, False)

	# Write the data
	write_data(data, 'test-out.csv', ',')


	sys.exit(0)

if __name__ == '__main__':	
	
	main()

			
