from nltk.tokenize import sent_tokenize
from nltk.corpus import sentiwordnet as swn
import twokenize as tw
from sklearn.externals import joblib
import math
senticnetpath = "/Users/Prerna/Desktop/Prerna/NTU/Courses-Year4-Sem2/CZ4034-InfoRet/code_app/TwitterOPINE/pyfiles/sentimentLexicons/senticnetDict_verypolar.joblib.pkl"
senticnetDict = joblib.load(senticnetpath)
BLdictpath = "/Users/Prerna/Desktop/Prerna/NTU/Courses-Year4-Sem2/CZ4034-InfoRet/code_app/TwitterOPINE/pyfiles/sentimentLexicons/bingliu.joblib.pkl"
BLdict = joblib.load(BLdictpath)
#from gensim.models import word2vec
#modelPath = "./../sentiment140word2vec/models/w2vModel_trainingFULL"
#model = word2vec.Word2Vec.load(modelPath)
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from nltk.corpus import stopwords
stop = stopwords.words('english')


def rem_NEG(token):
    if token[-4:] == "_NEG":
        return (token[:-4],1)
    else:
        return (token,0)
def getSentiWNVals(word, pos, neg):
    wordswn=[]
    if pos=="n" or pos=="a" or pos=="r" or pos=="v":
        wordswn = swn.senti_synsets(word, pos)
    if len(wordswn)==0:
        wordswn = swn.senti_synsets(word)
    if len(wordswn)>0:
        wordswn1 = wordswn[0]
        if neg==0:
            return {"pos":wordswn1.pos_score(), "neg":wordswn1.neg_score(), "obj":wordswn1.obj_score()}
        else:
            return {"pos":wordswn1.neg_score(), "neg":wordswn1.pos_score(), "obj":wordswn1.obj_score()}
    else:
        return {"pos":-1.0, "neg":-1.0, "obj":-1.0}

def getDictVals(lexdict, word, neg):
    if word in lexdict:
        pol = lexdict[word]
        if (pol>0 and neg==0) or (pol<0 and neg==1):
            return {"pos":abs(pol), "neg":0.0, "obj":0.0}
        elif (pol>0 and neg==1) or (pol<0 and neg==0):
            return {"pos":0.0, "neg":abs(pol), "obj":0.0}
        else:
            return {"pos":-1.0, "neg":-1.0, "obj":-1.0}
    else:
        return {"pos":-1.0, "neg":-1.0, "obj":-1.0}

def getPolarityMeasure(numpos, numneg):
    if numpos>numneg:
        if numneg>0:
            return (float(numpos)/numneg, 1)
        else:
            return (float(numpos), 1)
    elif numneg>numpos:
        if numpos>0:
            return (float(numneg)/numpos, -1)
        else:
            return (numpos, -1)
    else:#neg score and pos score are equal!
        return (0.0, 0)

def incPosNegCount(polScores, cpos, cneg, isStricter, polthresh):
    foundPol = False
    maxPolScore = 0.0
    poldir = "unk"
    if not isStricter:
        if polScores["pos"]>polScores["neg"] and polScores["pos"]>polScores["obj"]:
            cpos=cpos+1
            foundPol = True
            maxPolScore=polScores["pos"]
            poldir = "pos"
        elif polScores["neg"]>polScores["pos"] and polScores["neg"]>polScores["obj"]:
            cneg=cneg+1
            foundPol = True
            maxPolScore=polScores["neg"]
            poldir = "neg"
    else:
        if polScores["pos"]> polthresh and polScores["pos"]>polScores["neg"] and polScores["pos"]>polScores["obj"]:
            cpos=cpos+1
            foundPol=True
            maxPolScore=polScores["pos"]
            poldir = "pos"
        elif polScores["neg"] >polthresh and polScores["neg"]>polScores["pos"] and polScores["neg"]>polScores["obj"]:
            cneg=cneg+1
            foundPol=True
            maxPolScore=polScores["neg"]
            poldir = "neg"
    return (cpos, cneg, foundPol, maxPolScore, poldir)
    

def getPolCountOfTwt(persenttokens, persenttags, isStricter, polthresh):
    cpos = 0
    cneg = 0
    maxofmax=0.0
    countP = 0
    sumP = 0.0
    avgP = 0.0
    countN = 0
    sumN = 0.0
    avgN = 0.0
    for si in range(0, min(len(persenttokens), len(persenttags))):
        tokens = persenttokens[si]
        postags = persenttags[si]
        for ti in range(0, min(len(tokens), len(postags))):
            t = tokens[ti]
            p = postags[ti]
            t,n = rem_NEG(t)
            polScores = getSentiWNVals(t, p, n)
            #print "t -> sentiwn -> ",polScores
            cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
            if not foundPol:
                polScores = getDictVals(senticnetDict, t, n)
                #print "t -> senticnet -> ",polScores
                cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
            if not foundPol and not isStricter: # do not use BL for Hard Rules as it contains only +1 and -1 polarity values
                polScores = getDictVals(BLdict, t, n)
                #print "t -> bing liu -> ",polScores
                cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
            if maxPolScore>maxofmax:
                maxofmax = maxPolScore
            if poldir=="pos":
                sumP=sumP+maxPolScore
                countP=countP+1
            elif poldir=="neg":
                sumN=sumN+maxPolScore
                countN=countN+1
    if countN>0:
        avgN = sumN/countN
    if countP>0:
        avgP = sumP/countP
    return (cpos,cneg, maxofmax, avgP, avgN)

def rmStopWords(tokens, tags):
    newtokens = []
    newtags = []
    for ti in range(0, min(len(tokens), len(tags))):
        t = tokens[ti]
        p = tags[ti]
        if t not in stop:
            newtokens.append(t)
            newtags.append(p)
    return (newtokens, newtags)

def getPolCountOfTwtNew(persenttokens, persenttags, isStricter, polthresh):
    cpos = 0
    cneg = 0
    maxofmax=0.0
    countP = 0
    sumP = 0.0
    avgP = 0.0
    countN = 0
    sumN = 0.0
    avgN = 0.0
    for si in range(0, min(len(persenttokens), len(persenttags))):
        tokens, postags = rmStopWords(persenttokens[si], persenttags[si])
        stemmed = []
        concepts = []
        concepttags = []
        conceptnegs = []
        conceptmulti = []
        if len(tokens)==0:
            break
        t = tokens[0]
        p = postags[0]
        t,n = rem_NEG(t)
        stemt = stemmer.stem(t)
        stemmed.append(stemt)
        concepts.append(t)
        concepttags.append(p)
        conceptnegs.append(n)
        conceptmulti.append(0)
        if t!=stemt:
            concepts.append(stemt)
            concepttags.append(p)
            conceptnegs.append(n)
            conceptmulti.append(0)

        patterns = [("N", "N"), ("N", "V"), ("V", "N"), ("A", "N"), ("R", "N"), ("P", "N"), ("P", "V")]
        for ti in range(1, min(len(tokens), len(postags))):
            t = tokens[ti]
            p = postags[ti]
            t,n = rem_NEG(t)
            prevt = tokens[ti-1]
            prevp = postags[ti-1]
            prevt, prevn = rem_NEG(prevt)
            stemt = stemmer.stem(t)
            stemprevt = stemmed[-1]
            stemmed.append(stemt)
            # Add single word concepts
            concepts.append(t)
            concepttags.append(p)
            conceptnegs.append(n)
            conceptmulti.append(0)
            if t!=stemt:
                concepts.append(stemt)
                concepttags.append(p)
                conceptnegs.append(n)
                conceptmulti.append(0)
            searchpattern = tuple([prevp, p])
            concatlst = []
            if searchpattern in patterns:
                concept = prevt+" "+t
                if concept not in concepts and n==prevn:
                    concepts.append(concept)
                    concepttags.append("unk")
                    conceptnegs.append(n)
                    conceptmulti.append(1)
                concept = stemprevt+" "+t
                if concept not in concepts and n==prevn:
                    concepts.append(concept)
                    concepttags.append("unk")
                    conceptnegs.append(n)
                    conceptmulti.append(1)
                concept = prevt+" "+stemt
                if concept not in concepts and n==prevn:
                    concepts.append(concept)
                    concepttags.append("unk")
                    conceptnegs.append(n)
                    conceptmulti.append(1)
                concept = stemprevt+" "+stemt
                if concept not in concepts and n==prevn:
                    concepts.append(concept)
                    concepttags.append("unk")
                    conceptnegs.append(n)
                    conceptmulti.append(1)
            
        for ci in range(0, len(concepts)):
            concept = t = concepts[ci]
            p = concepttags[ci]
            n =  conceptnegs[ci]
            multi = conceptmulti[ci]
            polScores = getDictVals(senticnetDict, concept, n)
            #print "t -> sentiwn -> ",polScores
            cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
            if not foundPol and multi!=1:
                polScores = getSentiWNVals(t, p, n)
                #print "t -> senticnet -> ",polScores
                cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
            if not foundPol and multi!=1 and not isStricter: # do not use BL for Hard Rules as it contains only +1 and -1 polarity values
                polScores = getDictVals(BLdict, t, n)
                #print "t -> bing liu -> ",polScores
                cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
            if maxPolScore>maxofmax:
                maxofmax = maxPolScore
            if poldir=="pos":
                sumP=sumP+maxPolScore
                countP=countP+1
            elif poldir=="neg":
                sumN=sumN+maxPolScore
                countN=countN+1
    if countN>0:
        avgN = sumN/countN
    if countP>0:
        avgP = sumP/countP
    return (cpos,cneg, maxofmax, avgP, avgN)

def removeRepeats(raw):
    Lcase = raw.lower()
    if len(Lcase)==0:
        return raw
    new = Lcase[0]
    numrepeat = 0
    for ei in range(0, len(Lcase)-1):
        prev = Lcase[ei]
        curr = Lcase[ei+1]
        if prev!=curr:
            new=new+curr
        else:
            numrepeat=numrepeat+1
    return new

def findButsFrmTokens(tokens):
    butlocs= []
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        normt = removeRepeats(t)
        if normt=="but" or normt=="but_neg":
            butlocs.append(ti)
    return butlocs

def findButsFrmTwt(twt):
    tokens = tw.tokenizeRawTweetText(twt)
    butlocs= []
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        normt = removeRepeats(t)
        if normt=="but" or normt=="but_neg":
            butlocs.append(ti)
    return butlocs

def applyButRule(negtwt):
    if len(findButsFrmTwt(negtwt))==0:
        return "unknown"
    # Remove everything before the last "but" in every sentence
    sent_tokenize_list = sent_tokenize(negtwt)
    finalsenttokens = []
    for s in sent_tokenize_list:
        tokens = tw.tokenizeRawTweetText(s)
        butlocs = findButsFrmTokens(tokens)
        if len(butlocs)>0:
            loc = butlocs[-1]
            finaltokens = tokens[loc+1:]
            finalsenttokens.append(finaltokens)
        else:
            finalsenttokens.append(tokens)
    cpos, cneg = getPolCountOfTwt(finalsenttokens)
    if cpos>cneg:
        return "positive"
    elif cneg>cpos:
        return "negative"
    else:
        return "unknown"


def getWord2VecSimilar(word):
    w2vexp = []
    if word in model:
        sim = model.most_similar(word)
        for s in sim:
            if s[1]>0.5:
                w2vexp.append(s[0])
    return w2vexp

def expandTokens(tokens):
    tokensExp = []
    negs = []
    for t in tokens:
        t,n = rem_NEG(t)
        tExp = [t]
        stemt = stemmer.stem(t)
        if stemt!=t:
            tExp = tExp + [stemt]
        tnorep = removeRepeats(t)
        if tnorep!=t:
            tExp = tExp + [tnorep]
        #tExp = tExp + getWord2VecSimilar(t)
        tokensExp.append(tExp)
        negs.append(n)
    return (tokensExp, negs)

def getPolCountOfExptwt(persenttokens, isStricter, polthresh):
    cpos = 0
    cneg = 0
    maxofmax=0.0
    countP = 0
    sumP = 0.0
    avgP = 0.0
    countN = 0
    sumN = 0.0
    avgN = 0.0
    for si in range(0, len(persenttokens)):
        tokens = persenttokens[si]
        tokensExp, negs = expandTokens(tokens)
        for ti in range(0, len(tokens)):
            expOfToken = tokensExp[ti]
            n = negs[ti]
            for t in expOfToken:
                polScores = getSentiWNVals(t, "no_pos", n)
                #print "t -> sentiwn -> ",polScores
                cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
                if not foundPol:
                    polScores = getDictVals(senticnetDict, t, n)
                    #print "t -> senticnet -> ",polScores
                    cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
                if not foundPol and not isStricter: # do not use BL for Hard Rules as it contains only +1 and -1 polarity values
                    polScores = getDictVals(BLdict, t, n)
                    #print "t -> bing liu -> ",polScores
                    cpos,cneg, foundPol, maxPolScore, poldir = incPosNegCount(polScores, cpos, cneg, isStricter, polthresh)
                #print "counts"
                #print cpos
                #print cneg
                if maxPolScore>maxofmax:
                    maxofmax = maxPolScore
                if poldir=="pos":
                    sumP=sumP+maxPolScore
                    countP=countP+1
                elif poldir=="neg":
                    sumN=sumN+maxPolScore
                    countN=countN+1
                if foundPol:
                    break
    if countN>0:
        avgN = sumN/countN
    if countP>0:
        avgP = sumP/countP
    return (cpos,cneg, maxofmax, avgP, avgN)
    
def applyCommonRule(negtwt, pos, isStrict=False, isStricter=False, polthresh=0.0):
    sent_tokenize_list = sent_tokenize(negtwt)
    finalsenttokens = []
    finalpostokens = []
    st = 0
    for s in sent_tokenize_list:
        tokens = tw.tokenizeRawTweetText(s)
        stags = pos[st:st+len(tokens)]
        st = len(tokens)
        finalsenttokens.append(tokens)
        finalpostokens.append(stags)
    cpos, cneg, maxPol, avgP, avgN = getPolCountOfTwt(finalsenttokens, finalpostokens, isStricter, polthresh)
    #print cpos
    #print cneg
    if not isStrict and not isStricter:
        if cpos>cneg and maxPol>=0.6:
            return "positive"
        elif cneg>cpos and maxPol>=0.6:
            return "negative"
        else:
            cpos, cneg, maxPol, avgP, avgN = getPolCountOfExptwt(finalsenttokens, isStricter, polthresh)
            if cpos>cneg and maxPol>=0.6:
                return "positive"
            elif cneg>cpos and maxPol>=0.6:
                return "negative"
            else:
                return "unknown"
##        if cpos>0 and cneg == 0:
##            return "positive"
##        elif cneg>0 and cpos==0:
##            return "negative"
##        else:
##            cpos, cneg  = getPolCountOfExptwt(finalsenttokens, isStricter, polthresh)
##            if cpos>0 and cneg==0:
##                return "positive"
##            elif cneg>0 and cpos==0:
##                return "negative"
##            else:
##                return "unknown"

    else:
        if cpos>cneg:
            return "positive"
        elif cneg>cpos:
            return "negative"
        else:
            return "unknown"
##        if (cpos==1 or cpos==2) and cneg==0:
##            return "positive"
##        elif (cneg==1 or cneg==2) and cpos==0:
##            return "negative"
##        else:
##            return "unknown"
##        if cpos>0 and cneg==0:
##            return "positive"
##        elif cneg>0 and cpos==0:
##            return "negative"
##        else:
##            return "unknown"

def applyCommonRuleNew(negtwt, pos, isStrict=False, isStricter=False, polthresh=0.0):
    sent_tokenize_list = sent_tokenize(negtwt)
    finalsenttokens = []
    finalpostokens = []
    st = 0
    for s in sent_tokenize_list:
        tokens = tw.tokenizeRawTweetText(s)
        stags = pos[st:st+len(tokens)]
        st = len(tokens)
        finalsenttokens.append(tokens)
        finalpostokens.append(stags)
    cpos, cneg, maxPol, avgP, avgN = getPolCountOfTwtNew(finalsenttokens, finalpostokens, isStricter, polthresh)
    #print cpos
    #print cneg
    if not isStrict and not isStricter:
        if cpos>cneg and maxPol>=0.6:
            return "positive"
        elif cneg>cpos and maxPol>=0.6:
            return "negative"
        else:
            return "unknown"
##            cpos, cneg, maxPol, avgP, avgN = getPolCountOfExptwt(finalsenttokens, isStricter, polthresh)
##            if cpos>cneg and maxPol>=0.6:
##                return "positive"
##            elif cneg>cpos and maxPol>=0.6:
##                return "negative"
##            else:
##                return "unknown"
##        if cpos>0 and cneg == 0:
##            return "positive"
##        elif cneg>0 and cpos==0:
##            return "negative"
##        else:
##            cpos, cneg  = getPolCountOfExptwt(finalsenttokens, isStricter, polthresh)
##            if cpos>0 and cneg==0:
##                return "positive"
##            elif cneg>0 and cpos==0:
##                return "negative"
##            else:
##                return "unknown"

    else:
        if cpos>cneg:
            return "positive"
        elif cneg>cpos:
            return "negative"
        else:
            return "unknown"
##        if (cpos==1 or cpos==2) and cneg==0:
##            return "positive"
##        elif (cneg==1 or cneg==2) and cpos==0:
##            return "negative"
##        else:
##            return "unknown"
##        if cpos>0 and cneg==0:
##            return "positive"
##        elif cneg>0 and cpos==0:
##            return "negative"
##        else:
##            return "unknown"
    
##if __name__ == "__main__":
##    #atwt = "I am a good student, but I hate exams."
##    #atwt = "This phone is amazing #Hurry"
##    #pos = "d n d a #"
##    atwt = "I hate you"
##    pos = "^ v ^"
##    pos = pos.split()
##    print "call but rule"
##    print applyCommonRule(atwt, pos)

##if __name__ == "__main__":
##    atwt = "I loove"
##    pos = "d v"
##    pos = pos.split()
##    print applyCommonRule(atwt, pos, False)
