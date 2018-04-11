import csv 
import sys 

file = sys.argv[1]
'''
This is a script that takes a csv file of records about library resources which includes a call number and 
returns a file of those records sorted according to their LC call number.

Benefits of this script:
	No dependencies on non-native Python libraries
	Able to sort both official LC call numbers and local call numbers (provided they conform to LC syntax)
	Can sort CSV file with any number of columns provided the call number is somewhere in the record for each row


How to use:
	Specify the column containing the call number (on line 135). By default it is in the first column.  
	On the command line, type the following command:
		>sort_by_cn.py file_to_sort.csv 
	The script will display the number of errors and you will be prompted to name the output file 


'''
# read csv file into list 
def read_csv(f):
	l = []
	with open(f, 'r', encoding='utf-8') as rf:
		r = csv.reader(rf)
		for i in r:
			l.append(i)
			
	return l 
# write csv of sorted records to file 	
def write_file(l, s):
	with open(s, 'w', encoding='utf-8', newline='') as wf:
		w = csv.writer(wf)
		for i in l:
			w.writerow(i)

# takes a LC call number and returns the alphabetical LC class 		
def get_lc_char(cn):
     cn = cn.strip()
     cn_list = list(cn)
     pref = []
     for i in cn_list: # iterate through call number 
             if i.isalpha():

                     pref.append(i) # add character to list for export 
             else: # at first instance of a non-alphabetic character, list of characters is converted to string and returned 
                     code = ''.join(pref) 
                     return code
# takes an LC call number and returns the digits from the LC class number NOTE: this won't work if the call number does 
#not have a cutter 
def get_lc_num(cn):
     cn = cn.strip()
     code = get_lc_char(cn) # use above function to get and remove the alphabetical code 
     cn = cn.replace(code, '')
     cn_list = list(cn)
     nums = []
     for i in cn_list: 
             try: # iterate through call number until you reach a non-integer character (e.g a space or a period)
                     int_t = int(i)
                     nums.append(i)
             except ValueError: # when exception is raised on non-integer character, return the numbers from the call number 
                     num_code = ''.join(nums)
                     return num_code
					 
# takes a call number and returns a sortable version (used in a tuple for sorting) NOTE: this won't work if the call number does 
#not have a cutter 
def get_simple_sort(cn):
	lc_char = get_lc_char(cn)
	nums = cn.replace(lc_char, '')
	lc_nums = get_lc_num(cn) # retrieve numbers to iterate through 
	exp = []
	for c in nums: # iterate through characters in call number 
		if c.isalpha(): # if call number is an alphabetical letter, replace it with its ordinal 
			o = str(ord(c))
			exp.append(o)
		elif c == ' ': # for spaces and periods, replace them with zeros 
			exp.append('0')
		elif c == '.':
			exp.append('0')
		elif c.isdigit():
			exp.append(c)
	s = ''.join(exp)
	if len(lc_nums) < 4: # adding sorting zeros so that RA393 is sorted before RA1234
		s = '00' + s 
		return s
	if len(lc_nums) == 1:
		s = '0000' + s 
		return s 
	if len(lc_nums) == 2:
		s = '000' + s 
		return s
	else:	
		return s # if it is over 4 digits, we add no sorting zeros 
	
	
# wrapper function for sorting the csv of records, not much to see here  
def sort_file(s):
	rec = read_csv(s) 
	out_dict, sort_list, class_list = simple_sort_list(rec)
	sorted_list = sort_cn_list(sort_list)
	sorted_recs, errs = get_sorted_recs(out_dict, sorted_list, class_list)
	if len(errs) == 0:
		fname = input('Name the output file. \n')
		fname = fname + '.csv'
		write_file(sorted_recs, fname)
	else:
		print('errors found')
		
# takes list of tuples containing call number and sortable call number and returns a list based on the sortable call number 		
def sort_cn_list(cn_list):
	return sorted(cn_list, key=lambda x: x[1])
	
'''
These last two functions are where the sorting really happens and I'm pretty proud of them, so I'm gonna explain what's happening. 

simple_sort_list takes a list of records and grabs the call number. It adds the alphabetical code to a list if it's not already there. 
Then it gets a sortable version of the call number (see above). The record itself is added to a dictionary with 
the key being the regular call number. Then a tuple is created that contains the call number paired with the sortable version. These three are then exported to the
get_sorted_recs function. 

The get_sorted_recs function sorts the list of LC classifications in alphabetical order and then starts iterating through that list. From
there we start going through the list of the tuples containing the actual call number and the sortable call number. We get the LC code
using the get_lc_char function. If the code for a particular record matches the current code being iterated through on the list, we retrieve
the record from the dictionary and add it to a the final list for export. 

Why do I think this is cool? Because the records can be added in any order to the dictionary but using only native sorting methods in Python
we can retrieve them in the call number order without having to deal with the semantics of call numbers at all! 
'''
def get_sorted_recs(out_dict, sort_list, class_list):
	sorted_class = sorted(class_list)
	final_sort = []
	key_errors = []
	for code in sorted_class:
		for c in sort_list:
			try:
				cn = c[0]
				lc_char = get_lc_char(cn)
				if lc_char == code:
					recs = out_dict[cn]
					for i in recs:
						if i not in final_sort:
							final_sort.append(i)
			except KeyError:
				key_errors.append(c)
	print(str(len(key_errors)))		
	return final_sort, key_errors

# function for sorting records from a file 		
def simple_sort_list(rec):
	out_dict = {}
	class_list = [] 
	sort_list = []
	#err_list = []
	for i in rec:
		cn = i[0] 
		# HERE IS WHERE YOU SET THE COLUMN INDEX FOR THE CALL NUMBER. 
		# If the call number is in the first column, set this to 0. Set it 
		# to 1 for the second column, 2 for the third, etc. 
		lc_char = get_lc_char(cn) 
		if lc_char not in class_list:
			class_list.append(lc_char) 
		sort = get_simple_sort(cn)
		tup = (cn, sort)
		if cn not in out_dict:
			out_dict[cn] = [i]
			if tup not in sort_list:
				sort_list.append(tup)
		else:
			out_dict[cn].append(i)
			if tup not in sort_list:
				sort_list.append(tup)
	return out_dict, sort_list, class_list  

def main():
	sort_file(file)
	
main()	
