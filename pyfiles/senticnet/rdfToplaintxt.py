import xml.etree.ElementTree as ET
import re
import sys
sys.path.append("/Users/Prerna/Desktop/Prerna/NTU/FYP_Report_OnlineSys/OnlineSASystem/code/sentweet/hickledir")
import hickle as hkl
from nltk.corpus import stopwords
stop = stopwords.words('english')

def remStop(txt):
    lst = txt.split()
    lstnew = []
    for l in lst:
        if l not in stop:
            lstnew.append(l)
    newtxt = " ".join(lstnew)
    return newtxt

#version = "full"
version = "veryPolar"
thres = 0.6
#mode = "writeRaw"
mode = "writeNostopwords"

snfile = "senticnet3rdf.txt"
f = open(snfile, 'r');
sndict={}
rmlst = []
prevtxt = ""
prevkey = ""
for line in f:
    booltxt = "text xmlns" in line
    boolpol = "polarity xmlns" in line
    if len(line)==0 or (booltxt==False and boolpol==False):
        continue
    if booltxt:
        element = ET.XML(line)
        prevtxt = element.text
        if mode == "writeNostopwords":
            prevkey = remStop(prevtxt)
        else:
            prevkey = prevtxt
        #print prevkey
    if boolpol and prevkey=="":
        rmlst.append(prevtxt)
    if boolpol and prevkey!="":
        pol = float(re.sub('<[^>]*>', '', line))
        if version == "full":
            sndict[prevkey] = pol
        elif version == "veryPolar" and (pol>thres or pol<-1*thres):
            sndict[prevkey] = pol
    
f.close()

snofile = "senticnet3"
lendict = len(sndict)
if version == "veryPolar":
    hkl.dump(sndict, snofile+"_"+version+str(thres)+"_"+mode+"_"+str(lendict)+".hkl", "w")
else:
    hkl.dump(sndict, snofile+"_"+version+"_"+mode+"_"+str(lendict)+".hkl", "w")

print len(sndict)
print rmlst
