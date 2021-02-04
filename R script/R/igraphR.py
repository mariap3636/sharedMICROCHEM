import csv
import os
import sqlite3

def main():
    header_list = ["kegg", "eawag", "alam", "kegg", "eawag", "alam"]
    conn = sqlite3.connect("eawagSmallDb.db")
    conn.execute("PRAGMA foreign_keys = ON")

    basic = open("BasicReacSpaceWithoutProblematicCases.csv", "r")
    basic.readline()

    biglist = []
    biglist.append(header_list)

    for line in basic:
        list = []
        arr = line.split("\t")
        list.append(arr[2])
        if searchDB(conn,arr[2]):
            list.append(1)
        else:
            list.append(0)
        if searchAlam(arr[2]):
            list.append(1)
        else:
            list.append(0)
        list.append(arr[3])
        if searchDB(conn,arr[3]):
            list.append(1)
        else:
            list.append(0)
        if searchAlam(arr[3]):
            list.append(1)
        else:
            list.append(0)
        biglist.append(list)

    if os.path.exists("ResultFileForR.csv"):
        os.remove("ResultFileForR.csv")

    with open("ResultFileForR.csv", "w") as f_final:
        wr = csv.writer(f_final, delimiter='\t')
        wr.writerows(biglist)
    f_final.close()
    basic.close()

    runRCommand()


def searchDB(conn,input):
    curs = conn.cursor()
    curs.execute("select cutoff from eawag_compounds where bestHitKeggID=? or alternativeKeggID like ?",
                 (input, "%" + input + "%"))
    result = curs.fetchall()
    if len(result) > 0:
        for item in result:
            if float(item[0]) == 1.0:
                return True
        return False
    return False


def searchAlam(input):
    alam = open("Inhibitors_literature_AlamMT.csv", "r")
    alam.readline()
    for line in alam:
        arr = line.split("\t")
        if arr[2] == input:
            alam.close()
            return True
    alam.close()
    return False


def runRCommand():
    os.system("cd " + os.getcwd())
    os.system("Rscript --vanilla Rscript.R")

if __name__ == '__main__':
    main()