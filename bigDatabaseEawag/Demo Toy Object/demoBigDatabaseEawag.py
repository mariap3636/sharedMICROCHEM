import csv
import os
import sqlite3
from datetime import datetime
import sys


def printHelpCommand():
    print("\n")
    print("Run the script with command 'python3 demoBigDatabaseEawag.py *args' where '*args' can be:\n")
    print(" - '-help': for printing options without doing anything else\n")
    print(" - 'smiles='Oc1ccccc1O' name bestHitKeggID is_in_reaction': where smiles must be always included and in "
          "addition you can write which columns do you want to print from: \n"
          "eawag_id, smiles, name, is_in_reaction, bestHitKeggID, cutoff, alternativeKeggID\n"
          "or none of them = it will print all columns from db\n")
    print(" - 'kegg=C05270': this will print the connection with eawag of your chosen cmp from chemical_species "
          "table and its cutoff (1.0 or >= 0.9)\n")
    print(" - 'kegg100' or 'kegg90': for printing all flagged cmps from table chemical_species into a csv\n"
          " file with date and time specifications\n")
    print("You can run the script without any *args, then the database will only be created.\n")

def recognizeArgs(listOfArgs):
    if len(listOfArgs) >= 2:
        if listOfArgs[1] == "-help":
            printHelpCommand()
            return None

        a = []
        for i in range(1, len(listOfArgs)):
            a.append(listOfArgs[i])
        return a
    return None


def filling_react(conn):
    curs = conn.cursor()
    csvfile = open("eawag_reac.csv", "r")
    csvfile.readline()
    for line in csvfile:
        query = 'insert into eawag_reactions (eawag_reac_id, eawag_enz_id, expasyEC'
        arr = line.split('\t')
        curs.execute('select id from eawag_compounds where eawag_id=?', (arr[3],))
        res1 = curs.fetchall()
        if len(res1) > 0:
            input = res1[0][0]
            query = query + ", input_id"
        else:
            input = 0
        curs.execute('select id from eawag_compounds where eawag_id=?', (arr[4].split("\n")[0],))
        res2 = curs.fetchall()
        if len(res2) > 0:
            output = res2[0][0]
            query = query + ", output_id"
        else:
            output = 0
        query = query + ") values (:eawag_reac_id, :eawag_enz_id, :expasyEC"
        dic = {'eawag_reac_id': arr[0], 'eawag_enz_id': arr[1], 'expasyEC': arr[2]}
        if input != 0:
            query = query + ", :input_id"
            dic['input_id'] = input
        if output != 0:
            query = query + ", :output_id"
            dic['output_id'] = output
        query = query + ")"
        curs.execute(query, dic)
        conn.commit()
    csvfile.close()



def filling_cmp(conn):
    curs = conn.cursor()
    csvfile = open("eawag_comp.csv", "r")
    for line in csvfile:
        arr = line.split('\t')
        if "\n" in arr[6]:
            arr[6] = arr[6].split("\n")[0]
        insert_query = "insert into eawag_compounds (eawag_id, smiles, name, is_in_reaction, bestHitKeggID, " \
                       "cutoff, alternativeKeggID) values (:eawag_id, :smiles, :name, :is_in_reaction, " \
                       ":bestHitKeggID, :cutoff, :alternativeKeggID)"
        curs.execute(insert_query, {'eawag_id': arr[0], 'smiles': arr[1], 'name': arr[2], 'is_in_reaction': 1,
                                    'bestHitKeggID': arr[4],'cutoff': float(arr[5]), 'alternativeKeggID': arr[6]})
        conn.commit()
    csvfile.close()


def filling_cmp_kegg(conn):
    curs = conn.cursor()
    csvfile = open("chem_species.csv", "r")
    for line in csvfile:
        arr = line.split('\t')
        arr = fillingArr(arr)
        insert_query = "insert into chemical_species (name, mnxm, bigg, chebi, envipath, hmdb, kegg, " \
                       "lipidmaps, metacyc, reactome, sabiork, seed, slm, inchi_key, eawag_flag_100, " \
                       "eawag_flag_90) values (:name, " \
                       ":mnxm, :bigg, :chebi, :envipath, :hmdb, :kegg, :lipidmaps, :metacyc, :reactome, " \
                       ":sabiork, :seed, :slm, :inchi_key, :eawag_flag_100, :eawag_flag_90)"
        curs.execute(insert_query, {'name': arr[0], 'mnxm': arr[1], 'bigg': arr[2], 'chebi': int(arr[3]), 'envipath': arr[4],
                                    'hmdb': arr[5], 'kegg': arr[6], 'lipidmaps': arr[7], 'metacyc': arr[8], 'reactome': int(arr[9]),
                                    'sabiork': int(arr[10]), 'seed': arr[11], 'slm': int(arr[12]), 'inchi_key': arr[13],
                                    'eawag_flag_100': arr[14], 'eawag_flag_90': arr[15]})
        conn.commit()
    csvfile.close()


def fillingArr(arr):
    if "\n" in arr[len(arr) - 1]:
        item = arr.pop()
        item = item.split("\n")[0]
        arr.append(item)
    if len(arr) < 16:
        for i in range(len(arr),16):
            arr.append("")
        assert len(arr) == 16
    if arr[3] == "":
        arr[3] = 0
    if arr[10] == "":
        arr[10] = 0
    if arr[12] == "":
        arr[12] = 0
    if arr[9] == "":
        arr[9] = 0
    return arr


def fillDatabase(conn):
    try:
        filling_cmp(conn)
    except:
        raise RuntimeError
    try:
        filling_cmp_kegg(conn)
    except:
        raise RuntimeError
    try:
        filling_react(conn)
    except:
        raise RuntimeError


def findBySmiles(res):
    conn = openDb()
    curs = conn.cursor()
    smiles = res[0].split("smiles=")[1]
    if len(res) == 1:
        find_query = "select * from eawag_compounds where smiles=?"
    elif len(res) > 1:
        find_query = "select " + res[1]
        for i in range(2,len(res)):
            find_query = find_query + ", " + res[i]
        find_query = find_query + " from eawag_compounds where smiles=?"
    else:
        raise RuntimeError("some error in arguments")
    curs.execute(find_query, (smiles,))
    re = curs.fetchall()
    for item in re:
        print(*item)



def openDb():
    conn = sqlite3.connect("mvc_demo.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def controlIfExists(conn):
    curs = conn.cursor()
    curs.execute("PRAGMA table_info(eawag_compounds)")
    res1 = curs.fetchall()
    curs.execute("PRAGMA table_info(eawag_reactions)")
    res2 = curs.fetchall()
    if ((len(res1) == 0) or (len(res2) == 0)):
        return False
    else:
        return True

def main():
    conn = openDb()
    if not controlIfExists(conn):
        initdb(conn)
        conn = sqlite3.connect("mvc_demo.db")

    res = recognizeArgs(sys.argv)
    if res is not None:
        if "smiles" in res[0]:
            findBySmiles(res)
        elif "kegg100" == res[0] or "kegg90" == res[0]:
            findAll(res)
        elif "kegg=" in res[0]:
            findByKegg(res)


def findByKegg(res):
    if len(res) == 1:
        arg = res[0].split("=")
        query = "select eawag_flag_100, eawag_flag_90 from chemical_species where " + arg[0] + "=?"
        conn = openDb()
        curs = conn.cursor()
        curs.execute(query, (arg[1],))
        re = curs.fetchall()
        help = False
        if len(re) > 0:
            st = "Kegg cmp: " + arg[1] + " is connected with eawag with cutoff "
            if re[0][0] == 1:
                help = True
                st = st + str(1.0) + " "
            if re[0][1] == 1:
                if help is True:
                    st = st + "and cutoff "
                help = True
                st = st + ">=" + str(0.9) + " "
            if help is False:
                st = "Kegg cmp: " + arg[1] + " is not connected with any eawag"
            print(st)
        else:
            print("There is no cmp with this kegg in the table chemical_species")
    else:
        raise RuntimeError("some error in arguments")


def findAll(res):
    if len(res) == 1:
        if res[0] == "kegg100":
            query = "select * from chemical_species where eawag_flag_100 = 1"
        elif res[0] == "kegg90":
            query = "select * from chemical_species where eawag_flag_90 = 1"
        else:
            raise RuntimeError("some error in arguments")
        conn = openDb()
        curs = conn.cursor()
        curs.execute(query)
        re = curs.fetchall()
        list_f = []
        for item in re:
            list = []
            for i in range(0, len(item)):
                list.append(item[i])
            list_f.append(list)
        path = "result_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
        with open(path, 'w') as f_final:
            wr = csv.writer(f_final, delimiter='\t')
            wr.writerows(list_f)
        f_final.close()
        print("File " + path + " successfully created")


def initdb( conn ):
    curs = conn.cursor()
    create_cmp_query = "create table if not exists eawag_compounds (id integer not null primary key, eawag_id text not null, " \
                   "smiles text, name text, is_in_reaction bit, bestHitKeggID text, cutoff float," \
                   "alternativeKeggID text)"
    curs.execute(create_cmp_query)
    create_rxn_query = "create table if not exists eawag_reactions (id integer not null primary key, eawag_reac_id text not null," \
                       "eawag_enz_id text, expasyEC text, input_id integer references eawag_compounds (id), output_id integer references eawag_compounds (id))"
    curs.execute(create_rxn_query)
    create_chemspec = "create table if not exists chemical_species (id integer not null primary key, name text," \
                      " mnxm text, bigg text, chebi integer, envipath text, hmdb text, kegg text, lipidmaps text," \
                      " metacyc text, reactome integer, sabiork integer, seed text, slm integer, inchi_key text, eawag_flag_100 bit," \
                      "eawag_flag_90 bit)"
    curs.execute(create_chemspec)
    conn.commit()
    fillDatabase(conn)

if __name__ == '__main__':
    main()