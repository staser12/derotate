#!/usr/bin/python
import os
import re
import sys
from subprocess import Popen, PIPE, call

curDir = os.getcwd()
files_processed = 0
files_to_derotate = []

for root, dirs, files in os.walk("."):  
    for filename in files:
		files_processed+=1
		p = Popen(["exiftool.exe", "-Orientation", "-n", filename], stdin=PIPE, stdout=PIPE)	
		out, err = p.communicate(input='\n')	
		
		if len(out) > 0:
			#print "OUT: " + out
			regc = re.compile('(Orientation[ ]+?:[ ]+?)([0-9]+?)')
			m = regc.match(out)
			
			if m != None:
				orientation = m.group(2)
				
				try:
					int_orientation = int(orientation)
					
					if int_orientation != 1:
						print "Orientation was changed in exif: " + orientation
						print "Filename: " + filename
						files_to_derotate.append(filename)
				except Exception, e:
					print str(e)
					
		sys.stdout.write('\rScanned: ' + str(files_processed) + '/' + str(len(files)))
		sys.stdout.flush() 
		

print "\n"
print "================================= REPORT: ==================================="
print('\n'.join(files_to_derotate)) 

print('Starting derotation...')

files_processed = 0
for filename in files_to_derotate:
	p = Popen(["exiftool.exe", "-Orientation=1", "-n", filename], stdin=PIPE, stdout=PIPE)	
	out, err = p.communicate(input='\n')
	sys.stdout.write('\rProcessed: ' + str(files_processed) + '/' + str(len(files_to_derotate)))
	sys.stdout.flush() 
	files_processed += 1
print('n')		
print('Completed!')