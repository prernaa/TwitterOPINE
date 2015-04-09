##posEmoReg = ["(-:", "(:", "=)",":)", ":-)", "=`)", ":`)", ":`-)", "=-d","=d", ";d", ":d", ":-d", "x-d", "xd", "^-^", "^_^", ":]", "^_-", "^_*"]
##posEmoIrreg = ["^^"]
##negEmoReg = [")-:","):", "=(", "]:", ":[", ":(", ":-(", ">;(", ">:(", ":_(", "d'x", ":`(", ':"(', "='[", ":'(", ":'-(", "dx", "\:", ":/", "(~_~)", ">__>", "<('-')>", "</3", "}"]
##negEmoIrreg = ["sigh", "cry", "cries", "sad", "yawn"]
posEmoReg = ["(-:", "(:", "=)",":)", ":-)", "=`)", ":`)", ":`-)", "=-d","=d", ";d", ":d", ":-d", "^-^", "^_^", ":]", "^_-", "^_*"]
posEmoIrreg = ["^^"]
negEmoReg = [")-:","):", "=(", "]:", ":[", ":(", ":-(", ">;(", ">:(", ":_(", "d'x", ":`(", ':"(', "='[", ":'(", ":'-(", "\:", ":/", "(~_~)", ">__>", "<('-')>", "</3", "}"]
negEmoIrreg = ["sigh", "cry", "cries", "sad", "yawn"]


def removeRepeats(emoraw):
    emoLcase = emoraw.lower()
    emonew = emoLcase[0]
    numrepeat = 0
    for ei in range(0, len(emoLcase)-1):
        prev = emoLcase[ei]
        curr = emoLcase[ei+1]
        if prev!=curr:
            emonew=emonew+curr
        else:
            numrepeat=numrepeat+1
    return (emoLcase, emonew, numrepeat)


def isPosIrrEmo(emoraw, emonorep):
    pos = False
    if "^^" in emoraw:
        pos =  True
    return pos

def isNegIrrEmo(emoraw, emonorep):
    neg = False
    for i in negEmoIrreg:
        if i in emonorep:
            neg = True
    return neg

def isPosOrNegRegEmo(emoraw, emonorep):
    pos = False
    for i in posEmoReg:
        if i in emonorep:
            pos = True
    neg = False
    for i in negEmoReg:
        if i in emonorep:
            neg = True
    return (pos, neg)

def getEmoFeatures(nonegtokens, tags):
    cposemo = 0
    cnegemo = 0
    cemo = 0
    emodict = {}
    for ti in range(0, min(len(nonegtokens), len(tags))):
        if tags[ti]=="E":
            cemo = cemo+1
            emoraw = nonegtokens[ti]
            emolcase, emonorep, numrep = removeRepeats(emoraw)
            if isPosIrrEmo(emoraw, emonorep) or isPosOrNegRegEmo(emoraw, emonorep)[0]:
                cposemo=cposemo+1
            if isNegIrrEmo(emoraw, emonorep) or isPosOrNegRegEmo(emoraw, emonorep)[1]:
                cnegemo=cnegemo+1
            if cposemo>0 or cnegemo>0:
                emkey = "EMO_"+emonorep
                if emkey in emodict:
                    emodict[emkey]=emodict[emkey]+1
                else:
                    emodict[emkey]=1
    # features
    # <cposemo, cnegemo>
    # <cposemo, cnegemo, cemo>
    # ratios
    # number of repeats
    return {"cpos":cposemo, "cneg":cnegemo}
    #return emodict
    

#if __name__ == "__main__":
    #print getEmoFeatures([":))))"], ["E"])
    # check emo in Irreg List (exact match)
    # check xoxo thingy
    # check emo in Reg list 

        
    
