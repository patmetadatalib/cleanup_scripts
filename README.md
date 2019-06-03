# cleanup_scripts

This repository has general cleanup and management scripts that were developed to deal with local metadata issues at Polk Library but which seemed like they might be useful to a broader library audience or to anybody. I have learned Python recently so I don't pretend to be a great coder, but I am happy to share anything that might help others. 

The file_splitter.py script takes a csv file and splits it into smaller files of a size specified by the user.

The get_oclc.py script takes a csv file that has a bunch of different values from the MARC21 035 field and returns a list of only the OCLC numbers in the list.

get_oclc-no-csv.py takes a MARC binary file and returns a list of OCLC numbers formatted for batch processing using OCLC Connexion. 

The marc-to-oclc.py script takes a binary MARC file and returns the OCLC numbers formatted for use in the OCLC Connexion client

The sort_by_cn script takes a csv file and returns a sorted CSV sorted by LC call number. NOTE: in testing it does not work with call numbers that do not have cutters, which might come up if you are exporting from the MARC 050 field. Based on testing it's also more likely to incorrectly sort if all the records you are sorting are under the same LC classification code (RA, PQ, etc.). It will likely sort all records with a complex call call number together and in the correct order, but they will not be sorted correctly relative to the rest of the call number range. Apologies for any headaches. 

All scripts were generated using Python 3.6 and tested/used on Windows.
