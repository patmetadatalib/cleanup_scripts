import sys
import csv 
import re
from pymarc import MARCReader

f = sys.argv[1]

'''
This script takes a MARC record file and returns a list of OCLC numbers for use in the OCLC Connexion client


This script might help those who need to find only the OCLC numbers from a field where many local and 
network record numbers are also found in the 035 field in MARC. It should be run using the following
command in Command Prompt or other command line interface

>get_oclc.py [input_file].mrc


You will be prompted to name the output file
 

'''
#returns formatted string from pymarc field 
def format_pymarc(i):
	try:
		text = i[0]
		return text.format_field()
	except AttributeError:
		return ''
	except IndexError:
		return ''

#test to see if a particular marc field is in record 
def presence_test(rec, field, subfield):
	try:
		val = rec[field][subfield]
		if val is not None:
			return val
		else:
			return ''
	except TypeError:
		return ''		
		
def get_file(f):
	a = []
	with open(f, 'r', encoding='utf-8') as f:
		r = csv.reader(f)
		for row in r:
			a.append(row)
	return a
	
def get_oclc(f):
	oclc_list = []
	multi_count = 0
	multi_mms = []
	multi_record = []
	with open(f, 'rb') as rf:
		reader = MARCReader(rf, to_unicode=True)
		for rec in reader:
			oclc = rec.get_fields('035')
			oclc_text = []
			for i in oclc:
				oclc_text.append(i.format_field())
			for a in oclc_text:
				if '(OCoLC)'in a:
					number = a
					if number not in oclc_list:
						oclc_list.append(number)
				if 'ocm' in a:
					number = a
					oclc_list.append(number)
					if number not in oclc_list:
						oclc_list.append(number)
				if 'ocn' in a:
					number = a
					oclc_list.append(number)
					if number not in oclc_list:
						oclc_list.append(number)
	return oclc_list, multi_count, multi_mms, multi_record
	
def clean_list(oclc_list):
	for_export = []
	oclc_list = set(oclc_list)
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
	file_name = input('Name your output files:\n')
	file_name = file_name + '.txt'
	oclc_list, multi_count, multi_mms, multi_record = get_oclc(f)
	for_export = clean_list(oclc_list)
	oclc = 'oclc_' + file_name 
	with open(oclc, 'w', encoding='utf-8', newline='') as rf:
		w = csv.writer(rf)
		for i in for_export:
			w.writerow([i])

	
main()
