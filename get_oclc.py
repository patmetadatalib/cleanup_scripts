import sys
import csv 
import re

f = sys.argv[1]

'''
This script takes a csv export from MarcEdit containing only the 001, 245, and 035 fields and returns a 
text file with only the OCLC numbers from the 035 field. It was developed in order to streamline adding or 
removing holdings in batches in OCLC. I have noted where to change the index if your file is not like this.


This script might help those who need to find only the OCLC numbers from a field where many local and 
network record numbers are also found in the 035 field in MARC. It should be run using the following
command in Command Prompt or other command line interface

>get_oclc.py [input_file].csv


It will save a csv file called "oclc_numbers.csv" in the same directory.
 

'''


def get_file(f):
	a = []
	with open(f, 'r', encoding='utf-8') as f:
		r = csv.reader(f)
		for row in r:
			a.append(row)
	return a
	
def get_oclc(l):
	oclc_list = []
	for i in l:
		number = i[2] # this number should change if your input file has more than three columns or 
					  #if the 035 field isn't in the third column
		split = number.split(';')
		for a in split:
			if '(OCoLC)'in a:
				number = a
				if number not in oclc_list:
					oclc_list.append(number)
			elif 'ocm' in a:
				number = a
				oclc_list.append(number)
				if number not in oclc_list:
					oclc_list.append(number)
			elif 'ocn' in a:
				number = a
				oclc_list.append(number)
				if number not in oclc_list:
					oclc_list.append(number)
	return oclc_list
	
def clean_list(oclc_list):
	for_export = []
	for i in oclc_list:
		number = i
		count = number.count('OCoLC')
		if count > 1:
			x = number.split('(OCoLC)')
			for i in x:
				cleaned = re.sub('\D', '', i)
				if len(cleaned) > 0:
					if cleaned not in for_export:
						cleaned = '#' + cleaned
						for_export.append(cleaned)
		else:
			cleaned = re.sub('\D', '', number)
			if len(cleaned) > 0:
				if cleaned not in for_export:
					cleaned = '#' + cleaned
					for_export.append(cleaned)
	return for_export
	
	
def main():
	record_list = get_file(f)
	oclc_list = get_oclc(record_list)
	for_export = clean_list(oclc_list)
	#print(str(len(for_export))) 
	#print(for_export[0:10])
	with open('oclc_numbers.csv', 'w', encoding='utf-8', newline='') as rf:
		w = csv.writer(rf)
		for i in for_export:
			w.writerow([i])
	
main()