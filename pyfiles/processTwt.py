from subprocess import Popen, PIPE, STDOUT
import codecs
import re
import twokenize as tw

negWords = ["never","no","nothing","nowhere","noone","none","not","havent","haven't","hasnt","hasn't","hadnt","hadn't","cant","can't","couldnt","couldn't","shouldnt","shouldn't","wont","won't","wouldnt","wouldn't","dont","don't","doesnt","doesn't","didnt","didn't","isnt","isn't","arent","aren't","aint","ain't"]
nounTags = ["N", "^", "Z"] # noun, proper noun, proper noun + possessive
adjTags = ["A"] # Adjective
adverbTags = ["R"] # Adverb
verbTags = ["V", "T"] # verb, verb particle
writeTwtCount = 0

def rmAtURL(twt):
    twttokens = twt.split()
    for ti in range(0, len(twttokens)):
        t = twttokens[ti]
        twttokens[ti] = re.sub(r"(?:https?\://)\S+", "http://URL.com", twttokens[ti])
        twttokens[ti] = re.sub(r"(?:\@)\S+", "@USER", twttokens[ti])
        if twttokens[ti][:4]=="www."or twttokens[ti][:5]=="(www.":
            twttokens[ti]="http://URL.com"
        if twttokens[ti][1:]=="http://URL.com":
            twttokens[ti]="http://URL.com"
        if twttokens[ti][1:]=="@USER":
            twttokens[ti]="@USER"
    twt = " ".join(twttokens)
    return twt  

def checkNull(variable):
    if variable.strip()=="" or variable=="_NONE_" or variable is None:
        return None
    else:
        return variable
    
def writeToFile(twDict, searchTerm, tempfname):
    global writeTwtCount
    outF = codecs.open(tempfname, "a", "utf-8")
    try:
        outF.write(twDict["id"]) #1
        outF.write("\t")
        outF.write(twDict["created"]) #2
        outF.write("\t")
        outF.write(twDict["text"]) #3
        outF.write("\t")
        source = twDict["source"].strip()
        if source.lower() == "none" or len(source)==0:
            source = "_NONE_"
        outF.write(source) #4
        outF.write("\t")
        usrid = twDict["user_id"].strip()
        if usrid.lower() == "none" or len(usrid)==0:
            usrid = "_NONE_"
        outF.write(usrid) #5
        outF.write("\t")
        usrname = twDict["user_name"].strip()
        if usrname.lower() == "none" or len(usrname)==0:
            usrname = "_NONE_"
        outF.write(usrname) #6
        outF.write("\t")
        usrscrname = twDict["user_screen_name"].strip()
        if usrscrname.lower() == "none" or len(usrscrname)==0:
            usrscrname = "_NONE_"
        outF.write(usrscrname) #7
        outF.write("\t")
        usrloc = twDict["user_location"].strip()
        if usrloc.lower() == "none" or len(usrloc)==0:
            usrloc = "_NONE_"
        outF.write(usrloc) #8
        outF.write("\t")
        usrtimezone = twDict["user_time_zone"].strip()
        if usrtimezone.lower() == "none" or len(usrtimezone)==0:
            usrtimezone = "_NONE_"
        outF.write(usrtimezone) #9
        outF.write("\t")
        usrstcount = twDict["user_statuses_count"].strip()
        if usrstcount.lower() == "none" or len(usrstcount)==0:
            usrstcount = "_NONE_"
        outF.write(usrstcount) #10
        outF.write("\t")
        usrfrcount = twDict["user_friends_count"].strip()
        if usrfrcount.lower() == "none" or len(usrfrcount)==0:
            usrfrcount = "_NONE_"
        outF.write(usrfrcount) #11
        outF.write("\t")
        usrfollcount = twDict["user_followers_count"].strip()
        if usrfollcount.lower() == "none" or len(usrfollcount)==0:
            usrfollcount = "_NONE_"
        outF.write(usrfollcount) #12
        outF.write("\t")
        usrdesccount = twDict["user_description"].strip()
        if usrdesccount.lower() == "none" or len(usrdesccount)==0:
            usrdesccount = "_NONE_"
        outF.write(usrdesccount) #13
        writeTwtCount=writeTwtCount+1
        #print "Written ",writeTwtCount
    except Exception as e:
        #print "failed to write ",str(e)
        outF.write("_ERROR_EXCEPTION_")
        pass
    outF.write("\n")
    outF.close()

def generateNegFile(normtempfile, taggedtempfile, negtempfile, twtIdx, posIdx):
    fIn = codecs.open(normtempfile, "r")
    fPos = codecs.open(taggedtempfile, "r")
    fOut = codecs.open(negtempfile, 'w', encoding='utf-8')

    lc = 0
    for line in fIn:
        posline = next(fPos)
        lc=lc+1
        #print "line ",lc
        lst = line.split("\t")
        poslst = posline.split("\t")
        twt = lst[twtIdx]
        pos = poslst[posIdx]
        twt = " ".join(twt.split())
        pos = " ".join(pos.split())
        try:
            twt = twt.decode('utf-8')
        except UnicodeDecodeError:
            continue
        tokens = tw.tokenizeRawTweetText(twt)
        postags = pos.split()
        #assert (len(postags) == len(tokens)), 'LINE:",lc,"==> Length Mismatch Between #Tokens(",len(tokens),") and #POS (",len(postags),") tags!'
        #if (len(postags) != len(tokens)):
            #print postags
            #print
            #print tokens
            #print "LINE:",lc," ==> Length Mismatch Between #Tokens(",len(tokens),") and #POS (",len(postags),") tags!"
        negFlag=0
        for ti in range(0, len(tokens)):
            t = tokens[ti]
            p = postags[ti]
            if t in negWords:
                negFlag=1
            elif negFlag==1 and p==",":
                negFlag=0
            elif negFlag==1 and (p in nounTags or p in adjTags or p in adverbTags or p in verbTags):
                tokens[ti] = tokens[ti]+"_NEG"
        #print twt
        #print " ".join(tokens)
        #print pos
        negtwt = " ".join(tokens)
        for l in lst[:twtIdx]:
            #print l
            fOut.write(l)
            fOut.write("\t")
        fOut.write(negtwt)
        for l in lst[twtIdx+1:]:
            #print l
            fOut.write("\t")
            fOut.write(l)
        #fOut.write("\n")

    fIn.close()
    fPos.close()
    fOut.close()

def generateTaggedFile(normtempfile, taggedtempfile, twtIdx, usrdescIdx):
    taggerOut = Popen(["/Users/Prerna/Desktop/Prerna/NTU/Courses-Year4-Sem2/CZ4034-InfoRet/code/ark-tweet-nlp-0.3.2/runTagger.sh", "--input-field",str(twtIdx+1), "--no-confidence", normtempfile], stdout=PIPE, stderr=STDOUT)
    taggerOutU = Popen(["/Users/Prerna/Desktop/Prerna/NTU/Courses-Year4-Sem2/CZ4034-InfoRet/code/ark-tweet-nlp-0.3.2/runTagger.sh", "--input-field",str(usrdescIdx+1), "--no-confidence", normtempfile], stdout=PIPE, stderr=STDOUT)
    fIn = open(normtempfile, "r")
    fT = open(taggedtempfile, "w")

    lc = 0
    for il in fIn:
        lc=lc+1
        #print "tagging line ",lc
        inlst = il.split("\t")
        tl = taggerOut.stdout.readline()
        intl = tl.split("\t")
        #print intl
        while True:
            if tl!="" and len(intl)>2:
                break
            else:
                tl = taggerOut.stdout.readline()
                intl = tl.split("\t")
        
        for i in range(0,twtIdx):
            fT.write(inlst[i])
            fT.write("\t")
        #print intl[1]
        brtags = intl[1].split(" ")
        for t in brtags:
            fT.write(t)
            fT.write(" ")

        for i in range(twtIdx+1,usrdescIdx):
            fT.write("\t")
            fT.write(inlst[i])
        fT.write("\t")

        tU = taggerOutU.stdout.readline()
        intU = tU.split("\t")
        while True:
            if tU!="" and len(intU)>2:
                break
            else:
                tU = taggerOutU.stdout.readline()
                intU = tU.split("\t")
        brtagsU = intU[1].split(" ")
        for t in brtagsU:
            fT.write(t)
            fT.write(" ")
            
        fT.write("\n")
    fIn.close()
    fT.close()

def generateNormFile(tempfile, normtempfile):
    inF = codecs.open(tempfile, "r", "utf-8")
    outF = codecs.open(normtempfile, "w", "utf-8")

    twtIdx = 2
    userdescIdx = 12
    tc = 0
    for line in inF:
        tc=tc+1
        lst = line.split("\t")
        if len(lst)!=13:
            print "LINE ",tc," => length = ",len(lst)," instead of 13"
        for i in range(0,twtIdx):
            outF.write(lst[i])
            outF.write("\t")
        norm = rmAtURL(lst[twtIdx])
        outF.write(norm)
        outF.write("\t")
        for i in range(twtIdx+1,userdescIdx):
            outF.write(lst[i])
            outF.write("\t")
        normU = rmAtURL(lst[userdescIdx])
        outF.write(normU)
    ##    outF.write("\t")
    ##    for i in range(userdescIdx+1,len(lst)):
    ##        outF.write(lst[i])
    ##        outF.write("\t")
        outF.write("\n")
    inF.close()
    outF.close()
    
def deleteErrorsFromFile(tempfile, noerrortempfile):
    inF = codecs.open(tempfile, "r", "utf-8")
    outF = codecs.open(noerrortempfile, "w", "utf-8")
    for line in inF:
        lst = line.split()
        if lst[-1] != "_ERROR_EXCEPTION_":
            outF.write(line)
    inF.close()
    outF.close()
