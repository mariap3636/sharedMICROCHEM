First very simplified testing version of database for eawag, containing only the table "compounds".

I'm using the smiles ID as the primary key identifier in the table (may be changed later), which must be unique for each compound.

The script only needs to sit in the folder, where are the folders for each pollutant, doesn't need to be copied somewhere else.

Run the script with command "python3 smallDatabaseEawag.py *args " where "*args" can be:

 - "-help": for printing options without doing anything else
 
 - "smilesID" *whatToFind, where smilesID must be always included in the "" or '' and *whatToFind can be only "name", only "eawag_id" or both in any order (without ""/'')
 
 - you can write into arguments only smilesID without other things, then the output will be everything stored in DB for compound of this smile
 
You will get your found output into the console.
You can run the script without any *args, then the database will only be created.
 
For now the database is updated/being created each time again when the script is launched (but it is controlling which compounds are already in). After every run it is stored in "eawagSmallDb.dat", or "eawagSmallDbDump.db" in the directory where the script is living. 

It has been tested just for ethb2, gly and van until now and it is using only the downloaded .html files and c1, c2 files.
