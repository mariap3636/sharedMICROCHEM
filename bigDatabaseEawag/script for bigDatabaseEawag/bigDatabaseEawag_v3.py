import csv
import os
import sqlite3
from datetime import datetime
import sys


def printHelpCommand():
    print("\n")
    print("Run the script with command 'python3 bigDatabaseEawag_v3.py *args' where '*args' can be:\n")
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
        for i in range(1,len(listOfArgs)):
            a.append(listOfArgs[i])
        return a
    return None

# def filling_kegg_react(conn,path):
#     curs = conn.cursor()
#     f = open(path + "keggRxn.csv", "r")
#     for line in f:
#         arr = line.split('\t')
#         if len(arr) > 4:
#             eawagr = arr[0]
#             ec = arr[1]
#             input = arr[2]
#             output = arr[3]
#             listR = []
#             for i in range(4,len(arr)):
#                 listR.append(arr[i])
#             for item in listR:
#                 if "\n" in item:
#                     item = item.split("\n")[0]
#                 curs.execute("select id from eawag_reactions where eawag_reac_id=?", (eawagr,))
#                 eaw_id = curs.fetchall()[0][0]
#                 curs.execute("select id from reactions where kegg=?", (item,))
#                 res = curs.fetchall()
#                 if len(res) > 0:
#                     id = res[0][0]
#                     curs.execute("select id from kegg_reactions where eawag_id=? and eawag_reac_id=? and "
#                                  "kegg_input_id=? and kegg_output_id=? and kegg_reac_id=? and id_mvc=?",
#                                  (eaw_id,eawagr,input,output,item,id))
#                     rs = curs.fetchall()
#                     if len(rs) == 0:
#                         curs.execute(
#                             'insert into kegg_reactions (eawag_id, eawag_reac_id, kegg_input_id, kegg_output_id, kegg_reac_id, id_mvc) values (:eawag_id, :eawag_reac_id, :kegg_input_id, :kegg_output_id, :kegg_reac_id, :id_mvc)',
#                             {'eawag_id': eaw_id,'eawag_reac_id': eawagr, 'kegg_input_id': input, 'kegg_output_id': output, 'kegg_reac_id': item, 'id_mvc': id})
#                         conn.commit()
#                 else:
#                     curs.execute("select id from kegg_reactions where eawag_id=? and eawag_reac_id=? and "
#                                  "kegg_input_id=? and kegg_output_id=? and kegg_reac_id=?",
#                                  (eaw_id, eawagr, input, output, item))
#                     rs = curs.fetchall()
#                     if len(rs) == 0:
#                         curs.execute(
#                             'insert into kegg_reactions (eawag_id, eawag_reac_id, kegg_input_id, kegg_output_id, kegg_reac_id) values (:eawag_id, :eawag_reac_id, :kegg_input_id, :kegg_output_id, :kegg_reac_id)',
#                             {'eawag_id': eaw_id, 'eawag_reac_id': eawagr, 'kegg_input_id': input, 'kegg_output_id': output,
#                             'kegg_reac_id': item})
#                         conn.commit()
#     f.close()
#

def filling_react(conn, path):
    curs = conn.cursor()
    csvfile = open(path + path[:-1] + "_new.csv", "r")
 #   f = csv.reader(csvfile)
    csvfile.readline()
    for line in csvfile:
        arr = line.split('\t')
        reactID = arr[0]
        curs.execute('select id from eawag_compounds where eawag_id=?', (arr[1],))
        res1 = curs.fetchall()
        if len(res1) > 0:
            input = res1[0][0]
        else:
            pass

        curs.execute('select id from eawag_compounds where eawag_id=?', (arr[2],))
        res2 = curs.fetchall()
        if len(res2) > 0:
            output = res2[0][0]
        else:
            pass

        enzymeID = arr[3]
        expazyEC = arr[4]
        curs.execute('select id from eawag_reactions where eawag_reac_id=? and input_id=? and output_id=?', (reactID,input,output))
        control = curs.fetchall()
        if len(control) == 0:
            curs.execute('insert into eawag_reactions (eawag_reac_id, eawag_enz_id, expasyEC, input_id, output_id) values (:eawag_reac_id, :eawag_enz_id, :expasyEC, :input_id, :output_id)', {'eawag_reac_id': reactID, 'eawag_enz_id': enzymeID, 'expasyEC': expazyEC, 'input_id': input, 'output_id': output})
            conn.commit()
    csvfile.close()



def filling_cmp(conn, path, pathfile):
    f = open(pathfile, "r")
    curs = conn.cursor()
    for line in f:
        name = ""
        smiles = ""
        eawag_id = str(line.split("\n")[0])
        htmlfile = open(path + eawag_id + '.html', "r", encoding="latin-1")

        for line2 in htmlfile:
            if "SMILES" in line2:
                smiles = line2[line2.find("SMILES String:") + 15:line2.find("<p>")]
                if name != "":
                    break
            if "<h1>" in line2:
                name = line2[line2.find("<h1>") + 4:line2.find("</h1>")]

        try:
            simfile = open(path + eawag_id + "_simcompOut.txt")
            bestHit = simfile.readline()
            if bestHit != "":
                bestHitKeggID = bestHit.split('\t')[0]
                cutoff = bestHit.split("\t")[1]
            else:
                bestHitKeggID = ""
                cutoff = 0
            alternativeKeggID = ""
            for simline in simfile:
                alternativeKeggID = alternativeKeggID + simline.split()[0] + ";"
            alternativeKeggID = alternativeKeggID[:-1]
            simfile.close()
        except:
            bestHitKeggID = ""
            cutoff = 0
            alternativeKeggID = ""

        if (name != ""):
            control_query = "select id from eawag_compounds where eawag_id=? and smiles=? and name=?"
            curs.execute(control_query, (eawag_id, smiles, name))
            result = curs.fetchall()
            if len(result) == 0:
                insert_query = "insert into eawag_compounds (eawag_id, smiles, name, is_in_reaction, bestHitKeggID, cutoff," \
                               "alternativeKeggID) values (:eawag_id, :smiles, :name, :is_in_reaction, :bestHitKeggID, :cutoff, :alternativeKeggID)"
                curs.execute(insert_query, {'eawag_id': eawag_id, 'smiles': smiles, 'name': name, 'is_in_reaction': 1, 'bestHitKeggID': bestHitKeggID,'cutoff': cutoff, 'alternativeKeggID': alternativeKeggID})
                conn.commit()
            # else:
            #     print("attemp to add duplicate compound into compounds table")
    f.close()


def fillDatabase(conn, path):
    pathfile = path + "c1"
    try:
        filling_cmp(conn,path, pathfile)
    except:
        print(path)
        raise RuntimeError
    pathfile = path + "c2"
    try:
        filling_cmp(conn,path,pathfile)
    except:
        print(path)
        raise RuntimeError
    try:
        filling_react(conn,path)
    except:
        print(path)
        raise RuntimeError


def addColumn(conn):
    list1 = []
    list2 = []
    curs = conn.cursor()
    curs.execute("select * from eawag_compounds where cutoff >= 0.9")
    res = curs.fetchall()
    for item in res:
        if item[6] == 1.0:
            if item[5] not in list1:
                list1.append(item[5])
            arr = item[7].split(";")
            for item2 in arr:
                if item2 not in list1:
                    list1.append(item2)
        else:
            if item[5] not in list2:
                list2.append(item[5])

    curs.execute("ALTER TABLE chemical_species ADD eawag_flag_100 bit")
    curs.execute("ALTER TABLE chemical_species ADD eawag_flag_90 bit")
    for item in list1:
        try:
            curs.execute("update chemical_species set eawag_flag_100 = 1 where kegg =?", (item,))
            conn.commit()
        except:
            print('kegg cmp not found in table chemical_species: ' + item)
    for item in list2:
        try:
            curs.execute("update chemical_species set eawag_flag_90 = 1 where kegg =?", (item,))
            conn.commit()
        except:
            print('kegg cmp not found in table chemical_species: ' + item)


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
    if len(re) > 0:
    	for item in re:
        	print(*item)
    else:
    	print("No compound with this smiles in db")


def openDb():
    conn = sqlite3.connect("mvc.db")
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
        conn = sqlite3.connect("mvc.db")
        try:
            addColumn(conn)
        except:
            raise RuntimeError

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
    # create_kegg_rxn_query = "create table if not exists kegg_reactions (id integer not null primary key,
    # eawag_id integer references eawag_reactions (id), eawag_reac_id text, kegg_input_id text, kegg_output_id
    # text, kegg_reac_id text, id_mvc integer references reactions (id))"
    # curs.execute(create_kegg_rxn_query)
    conn.commit()

    rootdir = os.getcwd()
    for root, dirs, files in os.walk(rootdir):
        for dir in dirs:
            if dir != ".idea" and dir !="venv":
                path = str(os.path.join(dir)) + "/"
                fillDatabase(conn,path)
            # filling one pollutant at a time

if __name__ == '__main__':
    main()