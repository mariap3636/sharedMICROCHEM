Latest version of script_for_eawag01, make directories for all 102 pollutants named by their abb and store the long name in the file "longname.txt" in each folder.

The bash_script2.sh in this folder is modified to use the script_for_eawag01_03.py and to count on that the names of folders are now different (only abb), again without running the addInfoSimcompWithHeader_v2.py script in the for cycle (this action needs to be added into bash script).
