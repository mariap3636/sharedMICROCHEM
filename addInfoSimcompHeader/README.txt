v4:
 - script modified so it doesn't include kegg compounds with cutoff lower than 0.9 in the abb_new.csv files
 - cutoff between 0.9 - 0.6 is still written in the _simComp.txt files

v2:
 - in the first round running this script, it controls every _simComp.txt file and if its empty, script looks for another kegg id for cutoff 0.6

 - if another kegg id is found, script writes this kegg id into the _simComp.txt file with the cutoff and in the second round running this script, it doesnt need to search again

 - in either case, whenever the script reads keggId from _simComp.txt, whose cutoff is different than 1.0, it writes in the output this exceptionality (the different cutoff is not written into the columns yet, just to the output)

 - whenever is enzyme eawag id or compound eawag id missing, it is written in the output and the respectively columns are empty strings

 - the output is the file "abb_new.csv" table delimitered by \t
 
 - tested on 11 pollutants from data folder + ethb2, gly and van
