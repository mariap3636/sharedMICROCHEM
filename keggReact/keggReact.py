import csv
import os
import urllib.request

urlkegg = 'https://www.kegg.jp/entry/'

def findR(path):
    reac_list = []
    f = open(path + path[:-1] + "_new.csv", "r")
    f.readline()
    for line in f:
        arr = line.split("\t")
        keggc1 = []
        keggc2 = []
        if ((arr[5] != "") and (arr[5] != "NA_eawagCMPid")):
            keggc1.append(arr[5])
        if arr[6] != "":
            ar = arr[6].split(";")
            for item in ar:
                keggc1.append(item)
        if ((arr[7] != "") and (arr[7] != "NA_eawagCMPid")):
            keggc2.append(arr[7])
        if ((arr[8] != "") and arr[8] != "\n"):
            ar2 = arr[8].split(";")
            for item in ar2:
                if "\n" in item:
                    keggc2.append(item.split("\n")[0])
                else:
                    keggc2.append(item)
        ec = arr[4]

        if (keggc1 == []):
            print("Some serious problem: this eawag id cmp doesn't have kegg id: " + arr[1])
        if (keggc2 == []):
            print("Some serious problem: this eawag id cmp doesn't have kegg id: " + arr[2])

        for cm1 in keggc1:
            for cm2 in keggc2:
                try:
                    keggc = measure(cm1, cm2)
                except:
                    print(path)
                    print(cm1)
                    print(cm2)
                    raise RuntimeError
                reac = []

                reac_final = []
                reac_final.append(arr[0])
                reac_final.append(ec)
                reac_final.append(cm1)
                reac_final.append(cm2)

                findKegg = open("kegg.txt", "r")
                for line2 in findKegg:
                    if line2.split()[0][4:] == keggc[0]:
                        reac.append(line2.split()[1])
                    elif line2.split()[0][4:] == keggc[1]:
                        reac2 = line2.split()[1]
                        for r in reac:
                            if reac2 == r:
                                page = urllib.request.urlopen(urlkegg+r[3:]).read().decode('utf-8')
                                if ec != "":
                                    if findOrder(page, ec):
                                        reac_final.append(reac2[3:])
                                        print(r[3:])
                                else:
                                    reac_final.append(reac2[3:])
                                    print(r[3:])
                                break
                                
                findKegg.close()
                reac_list.append(reac_final)
    if os.path.exists(path + 'keggRxn.csv'):
        os.remove(path + 'keggRxn.csv')

    with open(path + 'keggRxn.csv', 'w') as f_final:
        wr = csv.writer(f_final, delimiter='\t')
        wr.writerows(reac_list)
    f_final.close()
    f.close()

#
# def findOrder(page, kegg1,kegg2):
#     help = False
#     arr = page.split('\n')
#     for line in arr:
#         if help is True:
#             m = int(line.find(";=&"))
#             if ((int(line.find(kegg1)) < m) and (m < int(line.find(kegg2)))):
#                 return True
#             else:
#                 return False
#         if "Equation" in line:
#             help = True
#

def findOrder(page, ec):
    help = False
    arr = page.split('\n')
    for line in arr:
        if help is True:
            if ec in line:
                return True
            else:
                return False
        if "Enzyme" in line:
            help = True


def measure(keggc1, keggc2):
    c1 = int(keggc1[1:])
    c2 = int(keggc2[1:])
    if c1 > c2:
        return keggc2,keggc1
    else:
        return keggc1,keggc2

def main():
    rootdir = os.getcwd()
    for root, dirs, files in os.walk(rootdir):
        for dir in dirs:
            if dir != ".idea" and dir !="venv":
                path = str(os.path.join(dir)) + "/"
                findR(path)


if __name__ == '__main__':
    main()

