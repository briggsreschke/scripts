"""
--------------------------------------------------------------------
csvm.py - Ver 1.0 - Last updated 5.9.2015

Simple search, merge and delete operations for csv files. 

Use regular expressions to search rows for matches:
	dict = {col_num:pattern, ...}

For column deletion uses a list of column numbers:
	list = [col1, col2, ...]

Merge a list of files:
	files = [file1, file2, ...]

--------------------------------------------------------------------
"""

import sys
import os.path
import re


# ------------------------------------------------------------------	
# Determine is list of cols matches up with the data
def check_cols(data, col_list):

	ncols = len(data)	
	# Make sure number of columns does not exceed the data cols
	if len(col_list) > ncols:
		return False
	
	# Make sure greatest col number isn't greater than number of columns
	if max(col_list) > ncols:
		return False

	return True

# ------------------------------------------------------------------	
#Remove cells (columns) from row
def delete_cells(row, col_list):
	
	for idx, cell in enumerate(cols):
		cell -= idx
		del row[cell]
	return row

# ------------------------------------------------------------------	
#Deletes columns (row[column]) from list of col numbers
def delete_cols(data, col_list, header): 	
	count = 0
	tmp = []

	# Remove duplicate col numbers and sort
	data = list(set(data))
	#Make sure list of columns matches up with the data
	if not check_cols(data, col_list):	
		print 'column list isn\'t consistent with data'
		sys.exit(4)

	# if there is a header
	if header:
		tmp.append(delete_cells(data[0], col_list))
		data = data[1:]
	
	# Now the data
	for row in data:		
		tmp.append(delete_cells(row, col_list))		

	return tmp

# -----------------------------------------------------------------	
# Deletes rows (skips them) if regex do not match cells

def search_rows(data, match_dict, header):

	tmp = []		
	is_match = False
		
	# Make sure the input file had data in it
	if not len(data):
		print 'No data to process in delete_rows()'
		sys.exit(3)

	# Deal with the header
	if header:
		tmp.append(data[0])
		data = data[1:]
	
	for row in data:	
		# iterate through {column number:regex}
		for key, value in match_dict.iteritems():
			# match agains't regex. If no match, skip.
			p = re.compile(value)				
			if not p.match(row[key]):
				is_match = False
				break
			else:
				is_match = True

		# if all matches are good, write the row
		if is_match == True:	
			tmp.append(row)

		is_match = False			

	return tmp


# -------------------------------------------------------------------
# Merge multiple csv files
'''
Todo: check to make sure columns are equal length
'''

def merge_files(file_list, ofile, header):

	if os.path.isfile(ofile):
		print 'Ouput file already exists'
		sys.exit(4)

	try:
		op = open(ofile, 'w+')
	except:
		print "Unable to open output file in merge_files()"
		sys.exit(3)

	count = 0	
	flag = False

	for f in file_list:		
		try:
			ip = open(f)
		except:
			continue		
	
		line = ip.readline()

		# Write the header once
		if header and line:
			if count == 0:
				op.write(line)
			line = ip.readline()

		# append lines to output
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
		print 'Could not open input file in read_data()'
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
	dic = {3:'^(SP|NP|NF)$'}
	data = search_rows(data, dic, False)

	# Write the data
	write_data(data, 'test-out.csv', ',')

	sys.exit(0)


if __name__ == '__main__':	
	
	main()

			
