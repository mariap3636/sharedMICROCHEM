import codecs
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

    try:
        simcomp_out1 = open(cmp1 + "_simcompOut.txt", "r")
    except:
        print("ERROR: the compound: " + cmp1 + " doesn't have a simcompOut.txt file")
        simcomp_out1 = None
    try:
        simcomp_out2 = open(cmp2 + "_simcompOut.txt", "r")
    except:
        print("ERROR: the compound: " + cmp2 + " doesn't have a simcompOut.txt file")
        simcomp_out2 = None

    # first cmp
    if simcomp_out1 is not None:
        try:
            smilepe = simcomp_out1.readline().split()
            if "1.0" not in smilepe[1]:
                if float(smilepe[1]) >= 0.9:
                    list.append(smilepe[0])
                else:
                    list.append("")
                print("Compound: " + cmp1 + " has kegg ID only with cutoff=" + smilepe[1])
            else:
                list.append(smilepe[0])
            string1 = ""
            for line2 in simcomp_out1:
                string1 = string1 + (line2.split()[0]) + ";"
            string1 = string1[:-1]
            list.append(string1)
        except:
            cutcom = "curl -F smiles='"
            htmlfile = codecs.open(cmp1 + '.html', "r", "utf-8")
            for line2 in htmlfile:
                if "SMILES" in line2:
                    smiles = line2[line2.find("SMILES String:") + 15:line2.find("<p>")]
                    break
            cutcom = cutcom + smiles
            cutcom = cutcom + "' -F cutoff=0.60 -F limit=10 http://rest.genome.jp/simcomp/"

 #           listcum.append(cutcom)

#            result = subprocess.run(listcum, stdout=subprocess.PIPE)
#            output = result.stdout.decode('utf-8')
            output = os.popen(cutcom).read()

            if output:
                list.append("")
                list.append("")
                print("Compound: " + cmp1 + " has kegg ID only with cutoff=" + output.split()[1])
                simcomp_out1.close()
                simcomp_out1 = open(cmp1 + "_simcompOut.txt", "w")
                simcomp_out1.write(output.split()[0] + "\t" + output.split()[1])
                simcomp_out1.close()
            else:
                list.append("")
                list.append("")
    else:
        print("Some serious error: for compound: " + cmp1 + " missing the _simcompOut.txt file!")
        list.append("")
        list.append("")

    # second cmp
    if simcomp_out2 is not None:
        try:
            smilepe = simcomp_out2.readline().split()
            if "1.0" not in smilepe[1]:
                if float(smilepe[1]) >= 0.9:
                    list.append(smilepe[0])
                else:
                    list.append("")
                print("Compound: " + cmp2 + " has kegg ID only with cutoff=" + smilepe[1])
            else:
                list.append(smilepe[0])
            string2 = ""
            for line2 in simcomp_out2:
                string2 = string2 + (line2.split()[0]) + ";"
            string2 = string2[:-1]
            list.append(string2)
        except:
            cutcom1 = "curl -F smiles='"
            cutcom2 = "' -F cutoff=0.60 -F limit=10 http://rest.genome.jp/simcomp/"

            htmlfile = codecs.open(cmp2 + '.html', "r", "utf-8")
            for line2 in htmlfile:
                if "SMILES" in line2:
                    smiles = line2[line2.find("SMILES String:") + 15:line2.find("<p>")]
                    break

            command = cutcom1 + smiles + cutcom2
            output = os.popen(command).read()

            if output:
                list.append("")
                list.append("")
                print("Compound: " + cmp2 + " has kegg ID only with cutoff=" + output.split()[1])
                simcomp_out2.close()
                simcomp_out2 = open(cmp2 + "_simcompOut.txt", "w")
                simcomp_out2.write(output.split()[0] + "\t" + output.split()[1])
                simcomp_out2.close()
            else:
                list.append("NA_eawagCMPid")
                list.append("")
    else:
        print("Some serious error: for compound: " + cmp2 + " missing the _simcompOut.txt file!")
        list.append("")
        list.append("")

    list_of_newcolumns[cmp1+cmp2] = list
    simcomp_out1.close()
    simcomp_out2.close()
csvfile.close()

name = str(os.getcwd()).split('/')[-1].split('_')[0]

def testPropertyOfLine(list):
    assert len(list) >= 3
    assert "r" in list[0]
    assert "c" in list[1]
    assert "c" in list[2]

    if len(list) == 5:
        return list

    if len(list) == 4:
        if list[4][0] == "e":
            list.append("")
            return list
        if type(list[4][0]) == int:
            print("Reaction: " + list[0] + " missing enzyme ID in: " + name + " file")
            ec = list.pop()
            list.append("")
            list.append(ec)
            return list
    if len(list) == 3:
        print("Reaction: " + list[0] + " missing enzyme ID in: " + name + " file")
        list.append("")
        list.append("")
        return list


fold = open(name, 'r')

list_newfile = []
list_header = ["rxn", "eawagCMPid1", "eawagCMPid2", "eawagENZid", "expasyECnum", "keggCMP1BestHit",
               "keggCMP1alternatives", "keggCMP2BestHit", "keggCMP2alternatives"]
list_newfile.append(list_header)

# every line in abb file
for line in fold:
    list_for_newfile = line.split()
    try:
        list_for_newfile = testPropertyOfLine(list_for_newfile)
        id = str(list_for_newfile[1] + list_for_newfile[2])
    except:
        print("Some serious error in file: " + name + " missing compounds/reaction ID")
        n = len(list_for_newfile)
        for i in range(5-n,5):
            list_for_newfile.append("")


    for item in list_of_newcolumns[id]:
        list_for_newfile.append(item)
    list_newfile.append(list_for_newfile)

if os.path.exists(name + "_new.csv"):
    os.remove(name + "_new.csv")

with open(name + '_new.csv', 'w') as f:
    wr = csv.writer(f,delimiter='\t')
    wr.writerows(list_newfile)

f.close()
fold.close()
print('Successfuly added new kegg columns')

