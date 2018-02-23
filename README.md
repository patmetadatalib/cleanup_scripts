# cleanup_scripts

This repository has general cleanup and management scripts that were developed to deal with local metadata issues at Polk Library but which seemed like they might be useful to a broader library audience or to anybody. I have learned Python recently so I don't pretend to be a great coder, but I am happy to share anything that might help others. 

The file_splitter.py script takes a csv file and splits it into smaller files of a size specified by the user.

The get_oclc.py script takes a csv file that has a bunch of different values from the MARC21 035 field and returns a list of only the OCLC numbers in the list. 

All scripts were generated using Python 3.6.2 and tested/used on Windows.
