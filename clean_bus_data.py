#!/usr/bin/python

import os, sys

dirs = os.listdir('bus_data/')

for f in dirs:
	file = open('bus_data/'+f,'r+')
	lines = file.readlines()
	headers = lines[0].split('PREDICTABLE')[0] + 'PREDICTABLE\n'
	firstline = lines[0].split('PREDICTABLE')[1]

	file.seek(0)
	file.write(headers)
	file.write(firstline)
	for line in lines[1:]:
		file.write(line)
