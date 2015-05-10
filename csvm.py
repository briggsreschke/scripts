'''
csvm.py - simple delete rows and cols from csv files. Additional functionality:  
Merge csv files and or build a json document

For merging large csvfiles, and deleting unwanted rows and columns

For row and column deletion, reads data into a list from the input file 
and then after creating a backup, outputs changed data back to input file name 

Todo:
--------------------------------------------------------------------
insert_header()
to_json()

* other merge operations *
'''

import sys
import os.path
import re
import shutil

TESTING = 1

#--------------------------------------------------------------------
# Get backup file name

def get_bakname(fname):
	cnt = 0
	foo = True
	
	# make backup filename to start with
	bname = fname + '.bak'
	# try backup file names until an unused one
	while(foo):
		if os.path.isfile(bname):
			cnt += 1
			bname = fname + '.bak' + str(cnt) 
		else:
			foo = False
	
	return bname

#--------------------------------------------------------------------
# Create a backup of file data to be deleted or inserted

def create_backup(fname, delimiter):
	
	bname = get_bakname(fname)
	try:
		shutil.copyfile(fname, bname)
	except:
		print "Unable to make backup copy of data"
		sys.exit(8)

#--------------------------------------------------------------------
# Get data from csv file and append it to a list
	
def get_data(fname, delimiter):
	data = []
	
	create_backup(fname, delimiter)
	
	try:
		ip = open(fname)
	except:
		print 'Could not open input file in get_data()'
		sys.exit(7)
	
	#Read data into a list ad return it to delete and insert routines
	line = ip.readline()	
	while(line):
		data.append(line.split(delimiter))
		line = ip.readline()
	
	ip.close()
	return data
		
# ------------------------------------------------------------------	
#Deletes columns (row[column]) from list of col numbers

def delete_cols(fname, cols, header, delimiter): 	
	
	# get list of file data
	data = get_data(fname, delimiter)
		
	# Make sure input file had data in it
	if not len(data):
		print 'No data to process in delete_cols()'
		sys.exit(6)
	
	# Make sure number of columns does not exceed the data cols
	if len(cols) > len(data):
		print 'cols is greater than columns in data.'
		sys.exit(5)
			
	# Open csv file and truncate it	
	try:
		of = open(fname, 'w+')
	except:
		print 'Could not open input file in delete_cols().'
		sys.exit(4)
	
	count = 0
	
	# if there is a header, save it
	if header:
		head = data[count]
	
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
			of.write(delimeter.join(head))
			
		# write the row with elimnated cols
		of.write(delimiter.join(row))
		
		# increment row index
		count += 1
	
	of.close()				

	return count

# -----------------------------------------------------------------	
# Deletes rows (skips them) if regex do not match cells

def delete_rows(fname, mdict, header, delimiter):
	
	# Get data
	data = get_data(fname, delimiter)
	
	# Make sure the input file had data in it
	if not len(data):
		print 'No data to process in delete_rows()'
		sys.exit(3)
			
	# Open the csv file	and truncate it 	
	try:
		of = open(fname,'w+')
	except:
		print 'Could not open file in delete_rows()'
		sys.exit(2)

			
	count = 0			
	is_match = False
	
	# Save header and increment count
	if header:
		head = data[0]
	
	for row in data:
		
		# iterate through key:value pairs {column number:regex}
		for key, value in mdict.iteritems():
			# if cell *does not* match against regex, delete row (skip it)
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
				of.write(delimeter.join(head))
			# write the row
			of.write(delimiter.join(row))
			
			count += 1
			
		is_match = False
	
	of.close()

	return count

# -------------------------------------------------------------------
# Merge multiple csv files

def merge_files(file_list, output_file):
	
	if os.path.isfile(output_file):
		print 'Ouput file already exists'
		sys.exit(4)

	try:
		op = open(output_file, 'w+')
	except:
		print "Unable to open output file in merge_files()"
		sys.exit(3)

	count = 0	
	for input_file in file_list:		
		try:
			ip = open(input_file)
		except:
			print "Unable to input file in merge_files()"
			sys.exit(2)		
		
		ip.readline()
		while(line):
			op.write(line)
			count += 1
		ip.close()

	op.close()
	return count
	

# -------------------------------------------------------------------
# Inserts a header. Only useful if there never was one

def insert_header(input_name, hlist, delimiter):
	# Todo
	head = hlist.split(delimiter)

	try:
		ip = open(input_name)
	except:
		print 'Unable to open file to insert header.'
		sys.xit(2)

	# create a temporary file
	# write header
	# write contents of input to tmp
	# close input
	# delete input file
	# rename tmp file to input file name


	
		
# --------------------------------------------------------------------	
# Make a json document from csv data

def to_json(ifile, ofile, header, delimiter):
	# Todo: Create utf-8 json from csv
	sys.exit(1)


# --------------------------------------------------------------------	
# Main

def main():
	
	if TESTING:
		# Remove columns using column numbers provided by list
		cols = [2, 3, 7, 8, 9, 10, 13, 14]
		ncols = delete_cols('csv-testdata.csv' , cols, False, ',')
		print '\nProcessed ' + str(ncols) + ' records.'
	
		# Delete rows using dict with column num and regex patterns to match against
		dict = {3:'^(SP|NP|NF)$'}
		nrows = delete_rows('csv-testdata.csv' , dict, False, ',')
		print 'Deleted ' + str(ncols-nrows) + ' rows.'


if __name__ == '__main__':
	
	main()
	sys.exit(0)
			
