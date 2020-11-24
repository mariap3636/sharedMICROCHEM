import os

f = open('myEdgeList.csv', 'r')

list_of_newcolumns = {}

for line in f:
    arr = line.split()
    cmp1 = arr[0]
    cmp2 = arr[1]
    list = []
    simcomp_out1 = open(cmp1 + "_simcompOut.txt")
    simcomp_out2 = open(cmp2 + "_simcompOut.txt")
    for line2 in simcomp_out1:
        list.append(line2.split()[0])
    for line2 in simcomp_out2:
        list.append(line2.split()[0])
    list_of_newcolumns[cmp1+cmp2] = list
f.close()

name = str(os.getcwd()).split('/')[-1].split('_')[0]

fnew = open('newoutput', 'w')
fold = open(name, 'r')

for line in fold:
    fnew.write(line.split('\n')[0])
    fnew.write(" ")
    id = str(line.split()[1] + line.split()[2])
    for item in range(0, len(list_of_newcolumns[id])):
        fnew.write(list_of_newcolumns[id][item])
        fnew.write(' ')
    fnew.write('\n')

fnew.close()
fold.close()
os.remove(name)
os.rename('newoutput', name)
print('successfuly added new kegg columns')

