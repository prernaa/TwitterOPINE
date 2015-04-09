from scipy.sparse import coo_matrix, hstack
import twokenize as tw
from nltk.corpus import stopwords
stop = stopwords.words('english')
import hickledir.hickle as hkl

sndictpath = "/Users/Prerna/Desktop/Prerna/NTU/Courses-Year4-Sem2/CZ4034-InfoRet/code_app/TwitterOPINE/pyfiles/senticnet/senticnet3_full_writeNostopwords_14659.hkl"
sndict = hkl.load(sndictpath, safe=False);

def combineFeatures(flist):
    f_coo_matrix_lst = []
    for f in flist:
        f_coo_matrix_lst.append(coo_matrix(f))
    return hstack(f_coo_matrix_lst)

def rem_Quote(negtwt, tags):
    tokens = tw.tokenizeRawTweetText(negtwt)
    countQ = 0
    rem=0
    newtokens = []
    newpos = []
    notincld = []
    quotpos = []
    for ti in range(0, min(len(tokens), len(tags))):
        t = tokens[ti]
        p = tags[ti]
        prevrem=rem
        if p=="," and t=='"' and rem==0:
            rem = 1
            quotpos.append(ti)
        elif p=="," and t=='"' and rem==1:
            rem = 0
            quotpos.append(ti)
    if len(quotpos) % 2 != 0:
        quotpos=quotpos[0:len(quotpos)-1]
    st = -1
    for i in range(0, len(quotpos), 2):
        en = quotpos[i]
        newtokens.extend(tokens[st+1:en])
        newpos.extend(tags[st+1:en])
        newtokens.append("_QUOTE_")
        newpos.append("Q")
        st = quotpos[i+1]
    newtokens.extend(tokens[st+1:])
    newpos.extend(tags[st+1:])
    
    if len(quotpos)>=2:
        newnegtwt = " ".join(newtokens)
        return (newnegtwt, newpos)
    else:
        return (negtwt, tags)
    
def getNegOnline(twt, postags):
    negWords = ["never","no","nothing","nowhere","noone","none","not","havent","haven't","hasnt","hasn't","hadnt","hadn't","cant","can't","couldnt","couldn't","shouldnt","shouldn't","wont","won't","wouldnt","wouldn't","dont","don't","doesnt","doesn't","didnt","didn't","isnt","isn't","arent","aren't","aint","ain't"]
    nounTags = ["N", "^", "Z"] # noun, proper noun, proper noun + possessive
    adjTags = ["A"] # Adjective
    adverbTags = ["R"] # Adverb
    verbTags = ["V", "T"] # verb, verb particle
    negatedWords = []
    tokens = tw.tokenizeRawTweetText(twt)
    negFlag=0
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        if(len(postags)<(ti+1)):
            p='NP'
        else:
            p = postags[ti]
        if t in negWords:
            negFlag=1
        elif negFlag==1 and p==",":
            negFlag=0
        elif negFlag==1 and (p in nounTags or p in adjTags or p in adverbTags or p in verbTags):
            negatedWords.append(tokens[ti])
            tokens[ti] = tokens[ti]+"_NEG"
    negtwt = " ".join(tokens)
    return (negtwt, negatedWords)


def getPuncFeatures(tokens, tags):
    isQ = 0.0
    isE = 0.0
    for ti in range(0, min(len(tokens), len(tags))):
        isQinT=0.0
        isEinT = 0.0
        t = tokens[ti]
        p = tags[ti]
        if p == ",":
            cQ = t.count("?")
            cE = t.count("!")
            if cQ>0 and cE==0:
                isQinT = 0.5
                if cQ>=2:
                    isQinT = 1.0
            if cE>0:
                isEinT = 0.5
                if cE>=2:
                    isEinT = 1.0
        if isEinT>isE:
            isE=isEinT
        if isQinT>isQ:
            isQ=isQinT
    return {"Punc_?":isQ, "Punc_!":isE}

def getNegWordsFrmNegtwt(negtwt):
    negatedWords = []
    tokens = tw.tokenizeRawTweetText(negtwt)
    for t in tokens:
        if t[-4:]=="_NEG" or t[-4:]=="_neg":
            negatedWords.append(t[:-4])
    return negatedWords

def getNegWordsAndNoNegTokens(negtwt):
    negatedWords = []
    tokens = tw.tokenizeRawTweetText(negtwt)
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        if t[-4:]=="_NEG" or t[-4:]=="_neg":
            tokens[ti]=t[:-4]
            negatedWords.append(t[:-4])
    return (tokens, negatedWords)

def getSNVal(term, isNeg):
    if term not in sndict:
        return None
    else:
        if isNeg:
            #print term, " ", -1*sndict[term]
            return -1*sndict[term]
        else:
            #print term, " ", sndict[term]
            return sndict[term]

def countPosAndNeg(qTerms, isNegs):
    cpos = 0
    cneg = 0
    maxpos = 0.0
    maxneg = 0.0
    avgpol = 0.0
    for qi in range(0, len(qTerms)):
        isneg = isNegs[qi]
        term = qTerms[qi]
        val = getSNVal(term, isneg)
        if val is None:
            continue
        avgpol = avgpol+val
        if val>0:
            if val>maxpos:
                maxpos=val
            cpos=cpos+1
        else:
            if val<maxneg:
                maxneg=val
            cneg=cneg+1
    return (cpos,cneg, maxpos, maxneg, avgpol)

def remStopTokPos(nonegtokens, postags):
    newt=[]
    newp=[]
    for ti in range(0, min(len(nonegtokens), len(postags))):
        t = nonegtokens[ti].lower()
        p = postags[ti].lower()
        if t not in stop:
            #print t
            newt.append(t)
            newp.append(p)
    return (newt, newp)

def getSNQueryTerms(nonegtokens, postags, negatedWords):
    Ntags = ["n", "^", "z"]
    Vtags = ["v"]
    Atags = ["a"]
    Rtags = ["r"]
    Ptags = ["p"]
    qTerms = []
    isNegs = []
    newt, newp = remStopTokPos(nonegtokens, postags)
    
    if len(newt)==0:
        return (qTerms, isNegs)
    
    # First Term
    t = newt[0]
    qTerms.append(t)
    if t in negatedWords:
        isNegs.append(1)
    else:
        isNegs.append(0)

    for ti in range(1, min(len(newt), len(newp))):
        pret = newt[ti-1]
        prep = newp[ti-1]
        t = newt[ti]
        p = newp[ti]

        # Single-terms
        qTerms.append(t)
        if t in negatedWords:
            isNegs.append(1)
        else:
            isNegs.append(0)

        # Double-terms
        if (t in negatedWords)!=(pret in negatedWords): # must be in same neg scope
            continue

        if prep in Ntags and p in Ntags: # N + N
            qTerms.append(pret+" "+t)
            if t in negatedWords:
                isNegs.append(1)
            else:
                isNegs.append(0)
        if prep in Ntags and p in Vtags: # N + V
            qTerms.append(pret+" "+t)
            if t in negatedWords:
                isNegs.append(1)
            else:
                isNegs.append(0)
        if prep in Vtags and p in Ntags: # V + N
            qTerms.append(pret+" "+t)
            if t in negatedWords:
                isNegs.append(1)
            else:
                isNegs.append(0)
        if prep in Atags and p in Ntags: # A + N
            qTerms.append(pret+" "+t)
            if t in negatedWords:
                isNegs.append(1)
            else:
                isNegs.append(0)
        if prep in Rtags and p in Ntags: # R + N
            qTerms.append(pret+" "+t)
            if t in negatedWords:
                isNegs.append(1)
            else:
                isNegs.append(0)
        if prep in Ptags and p in Ntags: # P + N
            qTerms.append(pret+" "+t)
            if t in negatedWords:
                isNegs.append(1)
            else:
                isNegs.append(0)
        if prep in Ptags and p in Vtags: # P + V
            qTerms.append(pret+" "+t)
            if t in negatedWords:
                isNegs.append(1)
            else:
                isNegs.append(0)


            
    return (qTerms, isNegs)

def calcPolMeasure(cpos, cneg):
    if cpos>cneg:
        if cneg!=0:
            return float(cpos)/cneg
        else:
            return cpos
    elif cneg>cpos:
        if cpos!=0:
            return float(cneg)/cpos
        else:
            return cneg
    else:
        return 0.0

def getSNFeatures(negtwt, postags):
    nonegtokens, negatedWords = getNegWordsAndNoNegTokens(negtwt)
    qTerms, isNegs = getSNQueryTerms(nonegtokens, postags, negatedWords)
    #print qTerms
    #print isNegs
    cpos, cneg, maxpos, maxneg, avgpol = countPosAndNeg(qTerms, isNegs)
    #print cpos, " ", cneg," ", maxpos," ",maxneg
    
    if abs(maxpos)>abs(maxneg):
        maxtotal = maxpos
    elif abs(maxneg)>abs(maxpos):
        maxtotal = maxneg
    else:
        maxtotal = 0.0
    polmeasure = calcPolMeasure(cpos, cneg)
    
    if cpos>cneg and maxpos>=0.6:
        poldir = 1
    elif cneg>cpos and maxneg<=-0.6:
        poldir = -1
    else:
        poldir = 0
    #return {"sn_poldir":poldir}
    #return {"sn_avgpol":avgpol}
    #return {"sn_cpos":cpos, "sn_cneg":cneg, "sn_maxpos":maxpos, "sn_maxneg":maxneg, "sn_polmeasure":polmeasure, "sn_avgpol":avgpol, "sn_poldir":poldir}
        
    return {"sn_cpos":cpos, "sn_cneg":cneg, "sn_maxpos":maxpos, "sn_maxneg":maxneg}
    #return {"sn_maxtotal":maxtotal}
    #return {"sn_polmeasure":polmeasure, "sn_maxtotal":maxtotal}

##if __name__ == "__main__":
##    atwt = ["I", "am", "not", "a", "good", "person"]
##    pos = "^ v x d a n"
##    pos = pos.split()
##    print "testing"
##    #getSNFeatures(atwt, pos, ["a", "good", "person"])
##    negtwt = "I am not a_neg good_neg person_neg"
##    print getNegWordsAndNoNegTokens(negtwt)
