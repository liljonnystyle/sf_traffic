#!/usr/bin/python

ofile = open('bus_data/output','r')

lines = ofile.readlines()

files = []
count = 0
for line in lines:
	if count%2 == 0:
		files.append(line.split()[1])
	count += 1

for f in files:
	file = open('bus_data/'+f,'r+')
	lines = file.readlines()
	headers = lines[0].split('PREDICTABLE')[0] + 'PREDICTABLE\n'
	firstline = lines[0].split('PREDICTABLE')[1]

	file.seek(0)
	file.write(headers) # separate header from first line
	file.write(firstline[:-3]+'\n')
	for line in lines[1:]:
		file.write(line[:-3]+'\n') # remove /r/r and add /n
