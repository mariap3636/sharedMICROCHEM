import os.path
import urllib.request

testcompounds = {'2,4-d': '2,4-Dichlorophenoxyacetic Acid',
                'dds': "Dodecyl Sulfate", 'mtb': "Methyl tert-butyl ether"}


ref_string = "http://eawag-bbd.ethz.ch/servlets/pageservlet?ptype=p&pathway_abbr="
for key in testcompounds:
    page2 = urllib.request.urlopen(ref_string + key).read()
    finstr2 = str(page2).split("\\n")
    listOfReactions = []
    for k in range(0, len(finstr2)):
        if "reacID=" in finstr2[k]:
            n = finstr2[k].find("reacID=") + 7
            lastId = finstr2[k][n:n + 5]
            if lastId not in listOfReactions:
                listOfReactions.append(lastId)
    path3 = os.getcwd()
    path = path3 + "//" + key
    try:
        os.makedirs(path)
    except:
        pass
    path2 = path + "//" + "EAWAGrxns.txt"
    path3 = path + "//" + "longname.txt"
    f = open(path2, "w")
    for item in listOfReactions:
        f.write(item + "\n")
    f.close()
    f2 = open(path3, "w")
    f2.write(testcompounds[key])
    f2.close()

print("succesfully done")