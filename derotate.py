#!/usr/bin/python
import os
import re
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
					
		print "files processed: " + str(files_processed)

print "================================= REPORT: ==================================="
print('\n'.join(files_to_derotate)) 