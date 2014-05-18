#!/usr/bin/python

from bs4 import BeautifulSoup as BS
import mechanize

def get_file(filename):
	url = 'ftp://75.10.224.35/AVL_DATA/AVL_RAW/'
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.addheaders = [('user-agent','Chrome')];
	htmlfile = browser.open(url+filename)

	htmltext = str(BS(htmlfile))

	start = 101 - htmltext[100::-1].index('>')
	end = htmltext[-100:-1].index('<')-100

	filename = 'bus_data/' + filename
	file = open(filename,'w')
	file.write(htmltext[start:end])

def main():
	url = 'ftp://75.10.224.35/AVL_DATA/AVL_RAW/'

	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.addheaders = [('user-agent','Chrome')];
	htmlfile = browser.open(url)

	htmltext = str(BS(htmlfile))

	filenames = [f for i,f in enumerate(htmltext.split()) if i%9 == 8]
	
	for f in filenames:
		if f[-3:] != 'zip':
			get_file(f)
	
if __name__ == '__main__':
	main()
