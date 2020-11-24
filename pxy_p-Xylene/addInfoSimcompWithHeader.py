import csv
import os

csvfile = open('myEdgeList.csv')
f = csv.reader(csvfile)

list_of_newcolumns = {}

for line in f:
    if line == "":
        break
    arr = line[0].split()
    cmp1 = arr[0]
    cmp2 = arr[1]
    list = []
    simcomp_out1 = open(cmp1 + "_simcompOut.txt")
    simcomp_out2 = open(cmp2 + "_simcompOut.txt")

    list.append(simcomp_out1.readline().split()[0])
    string1 = ""
    for line2 in simcomp_out1:
        string1 = string1 + (line2.split()[0]) + ";"
    string1 = string1[:-1]
    list.append(string1)

    itemhere = simcomp_out2.readline()
    list.append(itemhere.split()[0])
    string2 = ""
    for line2 in simcomp_out2:
        string2 = string2 + (line2.split()[0]) + ";"
    string2 = string2[:-1]
    list.append(string2)
    list_of_newcolumns[cmp1+cmp2] = list
csvfile.close()

name = str(os.getcwd()).split('/')[-1].split('_')[0]

fnew = open('newoutput', 'w')
fold = open(name, 'r')


fnew.write("")

list_newfile = []
list_header = ["rxn", "eawagCMPid1", "eawagCMPid2", "eawagENZid", "expasyECnum", "keggCMP1BestHit",
               "keggCMP1alternatives", "keggCMP2BestHit", "keggCMP2alternatives"]
list_newfile.append(list_header)

for line in fold:
    list_for_newfile = line.split()
    id = str(list_for_newfile[1] + list_for_newfile[2])
    for item in list_of_newcolumns[id]:
        list_for_newfile.append(item)
    list_newfile.append(list_for_newfile)

for row in list_newfile:
    fnew.write("{: <6} {: <12} {: <12} {: <11} {: <12} {: <16} {: <21} {: <16} {: <21}\n".format(*row))

fnew.close()
fold.close()
os.rename('newoutput', name+"_new")
print('successfuly added new kegg columns')

