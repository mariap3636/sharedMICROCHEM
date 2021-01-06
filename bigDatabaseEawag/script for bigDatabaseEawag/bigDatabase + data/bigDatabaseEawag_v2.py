import csv
import os
import codecs
import sqlite3
import sys


def printHelpCommand():
    print("\n")
    print("Run the script with command 'python3 smallDatabaseEawag.py *args' where '*args' can be:\n")
    print(" - '-help': for printing options without doing anything else\n")
    print(" - 'smilesID' *whatToFind, where smilesID must be always included in the '' and\n")
    print("*whatToFind can be only 'name', only 'eawag_id' or both in any order (without '')\n")
    print(" - you can write into arguments only smilesID without other things, then the output will be")
    print("everything stored in DB for compound of this smile\n")
    print("You can run the script without any *args, then the database will only be created.\n")

def recognizeArgs(listOfArgs):
    if len(listOfArgs) == 2:
        if listOfArgs[1] == "-help":
            printHelpCommand()
        else:
            return listOfArgs[1],
    elif len(listOfArgs) == 3:
        inputSmile = listOfArgs[1]
        output = listOfArgs[2]
        return inputSmile, output
    elif len(listOfArgs) == 4:
        inputSmile = listOfArgs[1]
        output1 = listOfArgs[2]
        output2 = listOfArgs[3]
        return inputSmile, output1, output2
    return None

def filling_kegg_react(conn,path):
    curs = conn.cursor()
    f = open(path + "keggRxn.csv", "r")
    for line in f:
        arr = line.split('\t')
        if len(arr) > 4:
            eawagr = arr[0]
            ec = arr[1]
            input = arr[2]
            output = arr[3]
            listR = []
            for i in range(4,len(arr)):
                listR.append(arr[i])
            for item in listR:
                if "\n" in item:
                    item = item.split("\n")[0]
                curs.execute("select id from eawag_reactions where eawag_reac_id=?", (eawagr,))
                eaw_id = curs.fetchall()[0][0]
                curs.execute("select id from reactions where kegg=?", (item,))
                res = curs.fetchall()
                if len(res) > 0:
                    id = res[0][0]
                    curs.execute("select id from kegg_reactions where eawag_id=? and eawag_reac_id=? and "
                                 "kegg_input_id=? and kegg_output_id=? and kegg_reac_id=? and id_mvc=?",
                                 (eaw_id,eawagr,input,output,item,id))
                    rs = curs.fetchall()
                    if len(rs) == 0:
                        curs.execute(
                            'insert into kegg_reactions (eawag_id, eawag_reac_id, kegg_input_id, kegg_output_id, kegg_reac_id, id_mvc) values (:eawag_id, :eawag_reac_id, :kegg_input_id, :kegg_output_id, :kegg_reac_id, :id_mvc)',
                            {'eawag_id': eaw_id,'eawag_reac_id': eawagr, 'kegg_input_id': input, 'kegg_output_id': output, 'kegg_reac_id': item, 'id_mvc': id})
                        conn.commit()
                else:
                    curs.execute("select id from kegg_reactions where eawag_id=? and eawag_reac_id=? and "
                                 "kegg_input_id=? and kegg_output_id=? and kegg_reac_id=?",
                                 (eaw_id, eawagr, input, output, item))
                    rs = curs.fetchall()
                    if len(rs) == 0:
                        curs.execute(
                            'insert into kegg_reactions (eawag_id, eawag_reac_id, kegg_input_id, kegg_output_id, kegg_reac_id) values (:eawag_id, :eawag_reac_id, :kegg_input_id, :kegg_output_id, :kegg_reac_id)',
                            {'eawag_id': eaw_id, 'eawag_reac_id': eawagr, 'kegg_input_id': input, 'kegg_output_id': output,
                            'kegg_reac_id': item})
                        conn.commit()
    f.close()
#
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
#             if ec == "":
#                 for item in listR:
#                     curs.execute("select id from reactions where kegg=?", (item,))
#                     res = curs.fetchall()
#                     if len(res) > 0:
#                         id = res[0][0]
#                         curs.execute("select id from eawag_reactions where eawag_reac_id=?", (eawagr,))
#                         eaw_id = curs.fetchall()[0][0]
#                         curs.execute(
#                             'insert into kegg_reactions (eawag_id, eawag_reac_id, kegg_input_id, kegg_output_id, kegg_reac_id, id_mvc) values (:eawag_id, :eawag_reac_id, :kegg_input_id, :kegg_output_id, :kegg_reac_id, :id_mvc)',
#                             {'eawag_id': eaw_id,'eawag_reac_id': eawagr, 'kegg_input_id': input, 'kegg_output_id': output, 'kegg_reac_id': item, 'id_mvc': id})
#                         conn.commit()
#             else:
#                 for item in listR:
#                     curs.execute("select id from reactions where kegg=?", (item,))
#                     res = curs.fetchall()
#                     if len(res) > 0:
#                         id = res[0][0]
#                         curs.execute("select ec_number from ec_reactions where reaction_id =?", (res[0][0],))
#                         res2 = curs.fetchall()
#                         if len(res2) > 0:
#                             ec2 = res2[0][0]
#                             if ec in ec2:
#                                 curs.execute("select id from eawag_reactions where eawag_reac_id=?", (eawagr,))
#                                 eaw_id = curs.fetchall()[0][0]
#                                 curs.execute('insert into kegg_reactions (eawag_id, eawag_reac_id, kegg_input_id, kegg_output_id, kegg_reac_id, id_mvc) values (:eawag_id, :eawag_reac_id, :kegg_input_id, :kegg_output_id, :kegg_reac_id, :id_mvc)',
#                                     {'eawag_id': eaw_id,'eawag_reac_id': eawagr, 'kegg_input_id': input, 'kegg_output_id': output, 'kegg_reac_id': item, 'id_mvc': id})
#                                 conn.commit()
#                         else:
#                             curs.execute("select id from eawag_reactions where eawag_reac_id=?", (eawagr,))
#                             eaw_id = curs.fetchall()[0][0]
#                             curs.execute('insert into kegg_reactions (eawag_id, eawag_reac_id, kegg_input_id, kegg_output_id, kegg_reac_id, id_mvc) values (:eawag_id, :eawag_reac_id, :kegg_input_id, :kegg_output_id, :kegg_reac_id, :id_mvc)',
#                             {'eawag_id': eaw_id,'eawag_reac_id': eawagr, 'kegg_input_id': input, 'kegg_output_id': output, 'kegg_reac_id': item, 'id_mvc': id})
#                             conn.commit()
#     f.close()


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
    try:
        filling_kegg_react(conn,path)
    except:
        print(path)
        raise RuntimeError


def addColumn(conn):
    list = []
    curs = conn.cursor()
    curs.execute("select id_mvc from kegg_reactions")
    res = curs.fetchall()
    for item in res:
        if item[0] not in list:
            list.append(item[0])
    try:
        curs.execute("ALTER TABLE reactions ADD eawag_flag bit")
        for item in list:
            curs.execute("update reactions set eawag_flag = 1 where id =?", (item,))
            conn.commit()
    except:
        pass

def findBySmiles(smiles, whatToFind1=None, whatToFind2=None):
    conn = openDb()
    curs = conn.cursor()
    if ((whatToFind2 == None) and (whatToFind1 != None)):
        find_query = "select " + str(whatToFind1) + " from compounds where smiles=?"
    elif ((whatToFind2 != None) and (whatToFind1 != None)):
        find_query = "select " + str(whatToFind1) + ", " + str(whatToFind2) + " from compounds where smiles=?"
    elif whatToFind1 == None:
        find_query = "select * from eawag_compounds where smiles=?"
    curs.execute(find_query, (smiles,))
    result = curs.fetchall()
    if len(result) > 0:
        list = []
        for item in result[0]:
            list.append(item)
        return list
    else:
        return None


def openDb():
    conn = sqlite3.connect("mvc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def main():
    conn = openDb()
    initdb(conn)
    conn = sqlite3.connect("mvc.db")
 #   with open('eawagSmallDbDump.db', 'w') as f:
 #       for line in conn.iterdump():
 #           f.write('%s\n' % line)
    try:
        addColumn(conn)
    except:
        raise RuntimeError
    res = recognizeArgs(sys.argv)
    if res != None:
        if len(res) == 1:
            found = findBySmiles(res[0])
            for item in found:
                print(item)
        if len(res) == 2:
            found = findBySmiles(res[0],res[1])
            print(found)
        elif len(res) == 3:
            found = findBySmiles(res[0],res[1],res[2])
            for item in found:
                print(item)


def initdb( conn ):
    curs = conn.cursor()
    create_cmp_query = "create table if not exists eawag_compounds (id integer not null primary key, eawag_id text not null, " \
                   "smiles text, name text, is_in_reaction bit, bestHitKeggID text, cutoff float," \
                   "alternativeKeggID text)"
    curs.execute(create_cmp_query)
    create_rxn_query = "create table if not exists eawag_reactions (id integer not null primary key, eawag_reac_id text not null," \
                       "eawag_enz_id text, expasyEC text, input_id integer references eawag_compounds (id), output_id integer references eawag_compounds (id))"
    curs.execute(create_rxn_query)
    create_kegg_rxn_query = "create table if not exists kegg_reactions (id integer not null primary key, eawag_id integer references eawag_reactions (id), eawag_reac_id text, kegg_input_id text, kegg_output_id text, kegg_reac_id text, id_mvc integer references reactions (id))"
    curs.execute(create_kegg_rxn_query)
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