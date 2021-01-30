Toy database object with 3 tables: pollutants, eawag_compounds and chem_prop
(schema: https://drawsql.app/recetox/diagrams/metanetx#)

Below are all possible combinations of arguments for this script.

Run the script with command 'python3 toyMetanetx.py *args' where '*args' can be:
 - '-help': for printing options without doing anything else
 - smiles='Oc1ccccc10: prints all information from table eawag_compounds
 - smiles='Oc1ccccc10' name eawag_id: or another specified columns from eawag_compounds
 - smiles='Oc1ccccc10' metanetx: prints all information from table chem_prop
 - smiles='Oc1ccccc10' metanetx name charge: or another specified columns from table chem_prop

 - abb=flu info: prints all information from table pollutants
 - abb=flu metanetx
 - abb=flu metanetx name charge

 - name=Fluorene info
 - name=Fluorene metanetx
 - name=Fluorene metanetx name charge

 - eawag=c0388 info
 - eawag=c0388 metanetx
 - eawag=c0388 metanetx name charge