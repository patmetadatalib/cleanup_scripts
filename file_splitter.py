#csv file splitter
import sys
import csv
'''
file_splitter.py takes a csv file as input and divides it into smaller files of whatever length is needed. I prompt the user for input
to make this easier to use for non coders. It should be run in Command Prompt or other command line interfaces as below:

>file_splitter.py [input file].csv

It will save the required number of files into the same directory where the script is run. 
'''
filmDB = sys.argv[1]
filmList = []
fNamePrefix = '_files'
extension = '.csv'
size = -1
listStore = {}

def get_size():
    global size
    size = int(input('how many records would you like per file?\n'))
    print(size)
    
def read_file(file, l1):
    with open(file, 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        for row in r:
            l1.append(row)
            
def split_list(l1, size):
    numberOfRecords = len(l1)
    print('number of records: ' + str(numberOfRecords))
    n = numberOfRecords/size
    n = int(n) 
    r = numberOfRecords%size
    print('remainder: ' + str(r))
    print('records / s: ' + str(n))
    print('number of lists needed: ' + str(n) + ' plus 1')
    nList = n 
    count = 0
    while count <= nList:
        count += 1
        #print(count)
        listStore[count] = []
        
    #print(listStore)
    addCount = 0
    listCount = 1
    sizeCount = 1
    for i in filmList:
        listStore[listCount].append(i)
        addCount += 1
        if len(listStore[listCount]) == size:
            listCount += 1
             
def print_dict(d1):
    global filmDB
    inputN = filmDB.split('.')
    inpName = inputN[0]
    global size
    for k, v in d1.items():
        print('length of list: #' +str(k) + ' : ' + str(len(listStore[k])))
        fName = inpName + str(size) + '_' + str(k) + fNamePrefix + extension
        listOfLists = d1[k]
        with open(fName, 'w', encoding='utf-8', newline='') as wf:
            w = csv.writer(wf)
            #add header row to ensure that outfile has desired number of columns. Removed here for clarity
            for i in listOfLists:
                w.writerow(i)
        
def main():
    get_size()
    read_file(filmDB, filmList)
    split_list(filmList, size)
    print_dict(listStore)


main()
