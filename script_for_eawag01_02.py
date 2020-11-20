import os.path
import urllib.request

webstr = "http://eawag-bbd.ethz.ch/search/bbdlinks.html"

try:
    page = urllib.request.urlopen(webstr).read()
    finstr = str(page).split("\\n")
    for i in range(0, len(finstr)):
        if "Link to external website" in finstr[i]:
            j = i
            break

    ref_string = "http://eawag-bbd.ethz.ch/servlets/pageservlet?ptype=p&pathway_abbr="
    while "</table>" not in finstr[j]:
        while 'a href="..' not in finstr[j]:
            if "</table>" in finstr[j]:
                break
            j += 1
        if '</table>' in finstr[j]:
            break

        if "target=" in finstr[j]:
            nameOfPol = finstr[j][finstr[j].find("target=") + 14:finstr[j].find("</a>")]
        else:
            nameOfPol = finstr[j][finstr[j].find('.html">') + 7:finstr[j].find("</a>")]

        if 'fungal' in nameOfPol:
            nameOfPol = nameOfPol[:-8]
        elif 'anaerobic' in nameOfPol:
            nameOfPol = nameOfPol[:-12]

        finstr3 = finstr[j][finstr[j].find('href=') + 9:finstr[j].find(".html") + 5]
        abb = finstr3[:finstr3.find('/')]

        page2 = urllib.request.urlopen(ref_string + abb).read()
        finstr2 = str(page2).split("\\n")
        listOfReactions = []
        for k in range(0, len(finstr2)):
            if "reacID=" in finstr2[k]:
                n = finstr2[k].find("reacID=") + 7
                lastId = finstr2[k][n:n + 5]
                if lastId not in listOfReactions:
                    listOfReactions.append(lastId)
        path3 = os.getcwd()
        path = path3 + "//" + abb + "_" + nameOfPol
        try:
            os.makedirs(path)
        except:
            pass
        path2 = path + "//" + "EAWAGrxns.txt"
        f = open(path2, "w")
        for item in listOfReactions:
            f.write(item + "\n")
        while "</tr>" not in finstr[j]:
            j += 1
    f.close()
except IOError:
    pass      # to do - problem in last iteration/not important for script's proper work

print("succesfully done")