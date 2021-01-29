Temporary Readme.txt for Demo Toy Object

 Run the script with command 'python3 demoBigDatabaseEawag.py *args' where '*args' can be:
    - '-help': for printing options without doing anything else
    - 'smiles='Oc1ccccc1O' name bestHitKeggID is_in_reaction': where smiles must be always included and in addition you can write which columns do you want to print from:
	eawag_id, smiles, name, is_in_reaction, bestHitKeggID, cutoff, alternativeKeggID
    or none of them = it will print all columns from db
    - 'kegg=C05270': this will print the connection with eawag of your chosen cmp from chemical_species table and its cutoff (1.0 or >= 0.9)
    - 'kegg100' or 'kegg90': for printing all flagged cmps from table chemical_species into a csv file with date and time specifications
    
You can run the script without any *args, then the database will only be created.

The script will create small "mvc_demo.db" from a few randomly generated compounds and some of their reactions and a small sample of "chemical_species" table from the original mvc.db.
