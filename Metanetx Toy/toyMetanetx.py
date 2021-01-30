import csv
import os
import sqlite3
from datetime import datetime
import sys


def printHelpCommand():
    print("\n")
    print("Run the script with command 'python3 toyMetanetx.py *args' where '*args' can be:\n")
    print("'-help': for printing options without doing anything else\n")
    print("- smiles='Oc1ccccc10': prints all information from table eawag_compounds\n"
          "- smiles='Oc1ccccc10' name eawag_id: or another specified columns from eawag_compounds\n"
          "- smiles='Oc1ccccc10' metanetx: prints all information from table chem_prop\n"
          "- smiles='Oc1ccccc10' metanetx name charge: or another specified columns from table chem_prop\n"
          "\n- abb=flu info: prints all information from table pollutants\n"
          "- abb=flu metanetx\n"
          "- abb=flu metanetx name charge\n"
          "\n- name=Fluorene info\n"
          "- name=Fluorene metanetx\n"
          "- name=Fluorene metanetx name charge\n"
          "\n- eawag=c0388 info\n"
          "- eawag=c0388 metanetx\n"
          "- eawag=c0388 metanetx name charge\n")
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


def filling_reac_prop(conn):
    curs = conn.cursor()
    tsv_file = open("reac_prop.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    for line in read_tsv:
        equation = resolve_equation(line[1])
        if "B" in line[4]:
            bal = 1
        else:
            bal = 0
        if "T" in line[5]:
            trans = 1
        else:
            trans = 0
        curs.execute("insert into reac_prop (MNXR, MNXM_input, MNXD_input, MNXM_output, "
                     "MNXD_output, reference, classif, is_balanced, is_transport)"
                     " values (:MNXR, :MNXM_input, :MNXD_input, :MNXM_output, "
                     ":MNXD_output, :reference, :classif, :is_balanced, :is_transport)",
                     {'MNXR': line[0], 'MNXM_input': equation[0], 'MNXD_input': equation[1],
                      'MNXM_output': equation[2], 'MNXD_output': equation[3], 'reference': line[2],
                      'classif': line[3], 'is_balanced': bal, 'is_transport': trans})
        conn.commit()
    tsv_file.close()


def resolve_equation(equation):
    inputs = equation.split("=")[0][2:]
    outputs = equation.split("=")[1][3:]
    input_mnxm = inputs[inputs.find("MNXM"):inputs.find("@")]
    input_mnxd = inputs[inputs.find("@")+1:inputs.find(" ")]
    output_mnxm = outputs[outputs.find("MNXM"):outputs.find("@")]
    n = outputs[outputs.find("@"):].find(" ")
    if n == -1:
        output_mnxd = outputs[outputs.find("@")+1:]
    else:
        output_mnxd = outputs[outputs.find("@")+1:outputs.find(" ")]
    return input_mnxm,input_mnxd,output_mnxm,output_mnxd


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
        curs.execute('select id from eawag_reactions where eawag_reac_id=? and input_id=? and output_id=?',
                     (reactID, input, output))
        control = curs.fetchall()
        if len(control) == 0:
            curs.execute(
                'insert into eawag_reactions (eawag_reac_id, eawag_enz_id, expasyEC, input_id, output_id) '
                'values (:eawag_reac_id, :eawag_enz_id, :expasyEC, :input_id, :output_id)',
                {'eawag_reac_id': reactID, 'eawag_enz_id': enzymeID, 'expasyEC': expazyEC, 'input_id': input,
                 'output_id': output})
            conn.commit()
    csvfile.close()


def filling_chemprop(conn):
    curs = conn.cursor()
    tsv_file = open("chem_prop.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    try:
        for line in read_tsv:
            curs.execute("select eawag_id from eawag_compounds where smiles=?", (line[8],))
            res = curs.fetchall()
            if len(res) > 0:
                curs.execute("insert into chem_prop (MNXM, name, reference, formula, charge, mass, InChI,"
                             " InChIKey, smiles, eawag_id) values (:MNXM, :name, :reference, :formula, :charge, :mass,"
                             " :InChI, :InChIKey, :smiles, :eawag_id)",
                             {'MNXM': line[0], 'name': line[1], 'reference': line[2], 'formula': line[3],
                              'charge': line[4], 'mass': line[5], 'InChI': line[6],
                              'InChIKey': line[7], 'smiles': line[8], 'eawag_id': res[0][0]})
            else:
                curs.execute("insert into chem_prop (MNXM, name, reference, formula, charge, mass, InChI,"
                     " InChIKey, smiles) values (:MNXM, :name, :reference, :formula, :charge, :mass,"
                     " :InChI, :InChIKey, :smiles)",
                     {'MNXM': line[0], 'name': line[1], 'reference': line[2], 'formula': line[3],
                      'charge': line[4], 'mass': line[5], 'InChI': line[6],
                      'InChIKey': line[7], 'smiles': line[8]})
            conn.commit()
    except:
        print(line[0])
        raise RuntimeError
    tsv_file.close()


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
                curs.execute(insert_query, {'eawag_id': eawag_id, 'smiles': smiles, 'name': name, 'is_in_reaction': 1,
                                            'bestHitKeggID': bestHitKeggID, 'cutoff': cutoff,
                                            'alternativeKeggID': alternativeKeggID})
                conn.commit()
    f.close()


def fillDatabase(conn, path):
    pathfile = path + "c1"
    try:
        filling_cmp(conn, path, pathfile)
    except:
        print(path)
        raise RuntimeError
    pathfile = path + "c2"
    try:
        filling_cmp(conn, path, pathfile)
    except:
        print(path)
        raise RuntimeError
    try:
        filling_pollutants(conn,path)
    except:
        print(path)
        raise RuntimeError
    # try:
    #     filling_react(conn, path)
    # except:
    #     print(path)
    #     raise RuntimeError


def filling_pollutants(conn,path):
    curs = conn.cursor()
    arr = path.split("/")
    abb = arr[len(arr)-2]
    f = open(path + "longname.txt", "r")
    name = f.readline().split("\n")[0]
    f.close()
    if "(fungal)" in name:
        name = name[:-9]
    if "(anaerobic)" in name:
        name = name[:-12]
    if "Family" in name:
        name = name[:-7]
    if "Immobilization" in name:
        name = name[:-15]
    if "Synthesis" in name:
        name = name[:-10]
    curs.execute("select eawag_id from eawag_compounds where name=?", (name,))
    res = curs.fetchall()
    if len(res) > 0:
        eawag_id = res[0][0]
        curs.execute("select * from pollutants where eawag_id=?", (eawag_id,))
        control = curs.fetchall()
        if len(control) == 0:
            curs.execute("insert into pollutants (name, abbreviation, eawag_id) values (:name,:abb,:eawag_id)",
                     {'name': name, 'abb': abb, 'eawag_id': eawag_id})
            conn.commit()
    else:
        raise RuntimeError("Not found eawag for pollutant name: " + name)


def findBySmiles(res):
    conn = openDb()
    curs = conn.cursor()
    smiles = res[0].split("smiles=")[1]
    if len(res) == 1:
        find_query = "select * from eawag_compounds where smiles=?"
    elif len(res) > 1:
        find_query = "select " + res[1]
        for i in range(2, len(res)):
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
    conn = sqlite3.connect("xref_database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def controlIfExists(conn):
    curs = conn.cursor()
    curs.execute("PRAGMA table_info(eawag_compounds)")
    res1 = curs.fetchall()
 #   curs.execute("PRAGMA table_info(eawag_reactions)")
 #   res2 = curs.fetchall()

    if ((len(res1) == 0)):
        return False
    else:
        return True


def main():
    conn = openDb()
    if not controlIfExists(conn):
        initdb(conn)

    res = recognizeArgs(sys.argv)
    if res is not None:
        if ((len(res)) == 1 and ("smiles" in res[0])):
            findBySmiles(res)
        if len(res) > 1:
            if "info" == res[1]:
                findInfo(res[0])
            elif "metanetx" == res[1]:
                findMetanetx(res)
            elif "smiles" in res[0]:
                findBySmiles(res)


def findInfo(input):
    conn = openDb()
    curs = conn.cursor()
    query = "select * from pollutants where "
    if "name" in input:
        query = query + "name=?"
    elif "abb" in input:
        query = query + "abbreviation=?"
    elif "eawag" in input:
        query = query + "eawag_id=?"
    else:
        raise RuntimeError("To get info about pollutant you must write name= or abb= or eawag= ")
    curs.execute(query, (input.split("=")[1],))
    re = curs.fetchall()
    if len(re) > 0:
        for item in re:
            print(*item)
    else:
        print("No pollutant found")


def findMetanetx(res):
    conn = openDb()
    curs = conn.cursor()
    if "smiles" not in res[0]:
        eawag_id = None
        if "eawag" in res[0]:
            eawag_id = res[0].split("=")[1]
        elif "name" in res[0]:
            curs.execute("select eawag_id from pollutants where name=?", (res[0].split("=")[1],))
            re = curs.fetchall()
            if len(re) > 0:
                eawag_id = re[0][0]
        elif "abb" in res[0]:
            curs.execute("select eawag_id from pollutants where abbreviation=?", (res[0].split("=")[1],))
            re = curs.fetchall()
            if len(re) > 0:
                eawag_id = re[0][0]
        if eawag_id is not None:
            if len(res) == 2:
                find_query = "select * from chem_prop where eawag_id=?"
            elif len(res) > 2:
                find_query = "select " + res[2]
                for i in range(3, len(res)):
                    find_query = find_query + ", " + res[i]
                find_query = find_query + " from chem_prop where eawag_id=?"
            curs.execute(find_query, (eawag_id,))
            result = curs.fetchall()
            if len(result) > 0:
                for item in result:
                    print(*item)
            else:
                 print("No pollutant found")
        else:
            print("No pollutant found")
    else:
        if len(res) == 2:
            find_query = "select * from chem_prop where smiles=?"
        elif len(res) > 2:
            find_query = "select " + res[2]
            for i in range(3, len(res)):
                find_query = find_query + ", " + res[i]
            find_query = find_query + " from chem_prop where smiles=?"
        curs.execute(find_query, (res[0].split("=")[1],))
        result = curs.fetchall()
        if len(result) > 0:
            for item in result:
                print(*item)
        else:
            print("No pollutant found")


def initdb(conn):
    curs = conn.cursor()
    create_cmp_query = "create table if not exists eawag_compounds (id integer not null primary key, " \
                       "eawag_id text unique, smiles text, name text collate nocase, is_in_reaction bit, " \
                       "bestHitKeggID text, cutoff float, alternativeKeggID text)"
    curs.execute(create_cmp_query)
    # create_rxn_query = "create table if not exists eawag_reactions (id integer not null primary key, " \
    #                    "eawag_reac_id text not null, eawag_enz_id text, expasyEC text, " \
    #                    "input_id integer references eawag_compounds (id), " \
    #                    "output_id integer references eawag_compounds (id))"
    # curs.execute(create_rxn_query)
    # create_kegg_rxn_query = "create table if not exists kegg_reactions (id integer not null primary key,
    # eawag_id integer references eawag_reactions (id), eawag_reac_id text, kegg_input_id text, kegg_output_id
    # text, kegg_reac_id text, id_mvc integer references reactions (id))"
    # curs.execute(create_kegg_rxn_query)
    create_rxn2_query = "create table if not exists chem_prop (id integer not null primary key, " \
                            "MNXM text unique, name text collate nocase, reference text, " \
                            "formula text, charge integer, mass float, inChI text, inChIKey text," \
                        " smiles text, eawag_id text references eawag_compounds (eawag_id))"
    curs.execute(create_rxn2_query)
    # create_cmp2_query = "create table if not exists reac_prop (id integer not null primary key, " \
    #                         "MNXR text, MNXM_input text references chem_prop (MNXM), MNXD_input text, " \
    #                     "MNXM_output text references chem_prop (MNXM), MNXD_output text, reference text, " \
    #                         "classif text, is_balanced bit, is_transport bit)"
    # curs.execute(create_cmp2_query)
    create_pollutants = "create table if not exists pollutants (id integer not null primary key, " \
                        "name text collate nocase, abbreviation text not null, eawag_id text " \
                        "references eawag_compounds (eawag_id))"
    curs.execute(create_pollutants)
    conn.commit()

    rootdir = os.getcwd()
    for root, dirs, files in os.walk(rootdir):
        for dir in dirs:
            if dir != ".idea" and dir != "venv":
                path = str(os.path.join(dir)) + "/"
                fillDatabase(conn, path)
    try:
        filling_chemprop(conn)
       # filling_reac_prop(conn)
    except:
        raise RuntimeError("problem in filling chem_prop/reac_prop")


if __name__ == '__main__':
    main()