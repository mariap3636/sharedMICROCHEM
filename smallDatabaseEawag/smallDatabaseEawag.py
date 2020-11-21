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


def fillDatabase(conn, path):
    curs = conn.cursor()
    f = open(path, "r")

    for line in f:
        name = ""
        smiles = ""
        eawag_id = str(line.split("\n")[0])
        path2 = path[:-2]
        htmlfile = codecs.open(path2 + eawag_id + '.html', "r")
        for line2 in htmlfile:
            if "<h1>" in line2:
                name = line2[line2.find("<h1>") + 4:line2.find("</h1>")]
            if "SMILES" in line2:
                smiles = line2[line2.find("SMILES String:") + 15:line2.find("<p>")]
        if ((name != "") and (smiles != "")):
            control_query = "select eawag_id from compounds where smiles=? and name=?"
            curs.execute(control_query, (smiles, name))
            result = curs.fetchall()
            if len(result) == 0:
                insert_query = "insert into compounds (eawag_id, smiles, name) values (:eawag_id, :smiles, :name)"
                curs.execute(insert_query, {'eawag_id': eawag_id, 'smiles': smiles, 'name': name})
                conn.commit()
            # else:
            #     print("attemp to add duplicate compound into compounds table")


def findBySmiles(smiles, whatToFind1=None, whatToFind2 = None):
    conn = openDb()
    curs = conn.cursor()
    if ((whatToFind2 == None) and (whatToFind1 != None)):
        find_query = "select " + str(whatToFind1) + " from compounds where smiles=?"
    elif ((whatToFind2 != None) and (whatToFind1 != None)):
        find_query = "select " + str(whatToFind1) + ", " + str(whatToFind2) + " from compounds where smiles=?"
    elif whatToFind1 == None:
        find_query = "select * from compounds where smiles=?"
    curs.execute(find_query, (smiles,))
    result = curs.fetchall()
    if len(result) > 0:
        if len(result[0]) == 1:
            return result[0][0]
        elif len(result[0]) == 2:
            return result[0][0], result[0][1]
        elif len(result[0]) == 3:
            return result[0][0], result[0][1], result[0][2]
    else:
        return None


def openDb():
    conn = sqlite3.connect("eawagSmallDb.dat")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def main():
    conn = openDb()
    initdb(conn)
    conn = sqlite3.connect("eawagSmallDb.dat")
    with open('eawagSmallDbDump.db', 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
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
    create_query = "create table if not exists compounds (eawag_id text not null, " \
                   "smiles text not null primary key, name text not null)"
    curs.execute(create_query)
    conn.commit()

    rootdir = os.getcwd()
    for root, dirs, files in os.walk(rootdir):
        for dir in dirs:
            if dir != ".idea" and dir !="venv":
                path1 = str(os.path.join(dir)) + "/c1"
                fillDatabase(conn,path1)
                path2 = str(os.path.join(dir)) + "/c2"
                fillDatabase(conn,path2)


if __name__ == '__main__':
    main()