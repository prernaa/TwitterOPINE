import twAPI as tw
import processTwt as pt
import pytodb as pdb
import time
import os
import os.path
import codecs
import shlex
import sys

thispath = os.path.dirname(os.path.realpath(__file__))


allowDBinput = True

def getNewFileName():
    global thispath
    ts = time.time()
    fc=0
    twtfile = thispath+"/tmp/twtTemp"+str(ts)+str(fc)+".txt"
    while (os.path.isfile(str(twtfile)) == True):
        twtfile = thispath+"/tmp/twtTemp"+str(ts)+str(fc)+".txt"
    return twtfile

def rmFile(filename):
    try:
        if (os.path.isfile(str(filename)) == True):
            os.remove(filename)
    except OSError as e: # name the Exception `e`
        print "Failed with:", e.strerror # look what it says
        print "Error code:", e.code 


def callSearch(query, fetchnum):
    tempfname = getNewFileName()
    ferrors = tempfname[:-4]+"_WithError.txt"
    fraw = tempfname
    fnorm = tempfname[:-4]+"_norm.txt"
    fpos = tempfname[:-4]+"_POS.txt"
    fneg = tempfname[:-4]+"_NEG.txt"
    qsplit = shlex.split(query)
    writeTwts = []
    hashTwts = {}
    countRepeats = 0
    api = tw.getTwAPI()
    twtLsts = tw.searchTw(api, qsplit, fetchnum)
    print "number of tweets = ", len(twtLsts)
    for twDict in twtLsts:
        pt.writeToFile(twDict, qsplit, ferrors)
    if len(twtLsts)>0:
        pt.deleteErrorsFromFile(ferrors, fraw)
        pt.generateNormFile(fraw, fnorm)
        pt.generateTaggedFile(fnorm, fpos, 2, 12)
        pt.generateNegFile(fnorm, fpos, fneg, 2, 2)
        # @TODO - call predict.py here itself
        pdb.dbInputWithoutSenti(qsplit, fraw, fnorm, fpos, fneg, allowDBinput)
    rmFile(ferrors)
    rmFile(fraw)
    rmFile(fnorm)
    rmFile(fpos)
    rmFile(fneg)
    
    

if __name__ == "__main__":
##    parser = argparse.ArgumentParser()
##    parser.add_argument("-s")
##    parser.add_argument("-n")
##    args = parser.parse_args()
    print "HELLO WORLD"
    fetchnum=20
    arglst = sys.argv

    if len(arglst)==3:
        fetchnum = int(arglst[2])
    if len(arglst)>=2:
        print "call search deactivated"
        callSearch(str(arglst[1]), fetchnum)
        

##    if args.s != '' and args.s is not None:
##        query = args.s
##        #print "query ",query
##        if args.n != '' and args.n is not None:
##            fetchnum=int(args.n)
        
        
