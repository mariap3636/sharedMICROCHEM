Script for preparing "keggRxn.csv" files in every folder. This script takes every row in "abb_new.csv" file and looks for all combinations of kegg cmps and their kegg reactions, compares results with E.C. number if it exists. Every eawag reaction may have more than 1 kegg reactions (if it has multiple kegg cmp alternatives with cutoff 1.0). 
The eawag reactions, whose reactants have kegg cmp with cutoff below 0.9 has no corresponding kegg reaction (some of these "keggRxn.csv" files are even completely empty - it is OK).
These files are than used to fill the database.

Generating these files takes +/- 30-40 minutes.

How to run this script: 
 - put this script + file "kegg.txt" (in this folder) into the folder, where are all 102 folders for pollutants
 - run command "python3 keggReact.py"