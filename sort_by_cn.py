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
     for i in cn_list:
             if i.isalpha():

                     pref.append(i)
             else:
                     code = ''.join(pref)
                     return code
# takes an LC call number and returns the digits from the LC class number 
def get_lc_num(cn):
     cn = cn.strip()
     code = get_lc_char(cn)
     cn = cn.replace(code, '')
     cn_list = list(cn)
     nums = []
     for i in cn_list:
             try:
                     int_t = int(i)
                     nums.append(i)
             except ValueError:
                     num_code = ''.join(nums)
                     return num_code
					 
# takes a call number and returns a sortable version (used in a tuple for sorting) 				 
def get_simple_sort(cn):
	lc_char = get_lc_char(cn)
	nums = cn.replace(lc_char, '')
	lc_nums = get_lc_num(cn)
	exp = []
	for c in nums:
		if c.isalpha():
			o = str(ord(c))
			exp.append(o)
		elif c == ' ':
			exp.append('0')
		elif c == '.':
			exp.append('0')
		elif c.isdigit():
			exp.append(c)
	s = ''.join(exp)
	if len(lc_nums) < 4:
		s = '00' + s 
		return s
	if len(lc_nums) == 1:
		s = '0000' + s 
		return s 
	if len(lc_nums) == 2:
		s = '000' + s 
		return s
	else:	
		return s 
# wrapper function for sorting the csv of records 
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
	
# takes the dictionary of actual records, the sorted list, and the list of call number codes and returns a list of sorted records for writing to a file along with a list of any errors 	
def get_sorted_recs(out_dict, sort_list, class_list):
	sorted_class = sorted(class_list)
	final_sort = []
	key_errors = []
	for code in class_list:
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
