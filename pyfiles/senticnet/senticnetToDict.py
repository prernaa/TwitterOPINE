from sklearn.externals import joblib

snfile = "senticnet.txt"

f = open(snfile, 'r');

snDict = {}
lc=0
for line in f:
    lc=lc+1
    if(lc%100==0):
        print lc
    lst = line.split()
    phraselst = lst[:len(lst)-1]
    polarity = lst[len(lst)-1]
    print polarity
    polarity = float(polarity)
    print polarity
    phrase = " ".join(phraselst)
    if polarity<-0.5 or polarity>0.5:
        snDict[phrase] = polarity
f.close()

print len(snDict)
_ = joblib.dump(snDict, "senticnetDict_verypolar.joblib.pkl", compress=9);
