import os.path
import sys
import urllib.request


#recursive looking for all reacts in one line
def findReact(line, listOfReactions):
    if "reacID=" in line:
        n = line.find("reacID=") + 7
        if n == -1:
            return listOfReactions
        lastId = line[n:n + 5]
        if lastId not in listOfReactions:
            listOfReactions.append(lastId)
        if n < len(line):
            findReact(line[n:],listOfReactions)


webstr = "http://eawag-bbd.ethz.ch/search/bbdlinks.html"

try:
    page = urllib.request.urlopen(webstr).read()
    finstr = str(page).split("\\n")
    for i in range(0, len(finstr)):
        if "Link to external website" in finstr[i]:
            j = i
            break

    ref_string = "http://eawag-bbd.ethz.ch"
    while "</table>" not in finstr[j]:      # end of webpage
        while 'a href="..' not in finstr[j]:
            if "</table>" in finstr[j]:
                break
            j += 1
        ref_string2 = finstr[j][finstr[j].find("a href=") + 11:finstr[j].find(".html")] + ".html"
        if "target=" in finstr[j]:
            nameOfPol = finstr[j][finstr[j].find("target=") + 14:finstr[j].find("</a>")]
        else:
            nameOfPol = finstr[j][finstr[j].find('.html">') + 7:finstr[j].find("</a>")]

        if 'fungal' in nameOfPol:
            nameOfPol = nameOfPol[:-8]
        elif 'anaerobic' in nameOfPol:
            nameOfPol = nameOfPol[:-12]

        abb = ref_string2[:ref_string2.find('/')]
        page2 = urllib.request.urlopen(ref_string + '/' + ref_string2).read()
        finstr2 = str(page2).split("\\n")
        listOfReactions = []
        for k in range(0, len(finstr2)):
            if "reacID=" in finstr2[k]:
                findReact(finstr2[k],listOfReactions)
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
        j += 1
    f.close()
except IOError:
    pass      # problem in last iteration/not important for script's proper work

print("succesfully done")