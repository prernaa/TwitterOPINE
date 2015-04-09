from nltk.tokenize import sent_tokenize
import twokenize as tw

def removeRepeats(raw):
    Lcase = raw.lower()
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

def findButs(tokens):
    butlocs= []
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        normt = removeRepeats(t)
        if normt=="but" or normt=="but_neg":
            butlocs.append(ti)
    return butlocs


def removeButAnterior(twt, tags):
    sent_tokenize_list = sent_tokenize(twt)
    finaltwt = ""
    finaltags = []
    st= 0
    for s in sent_tokenize_list:
        tokens = tw.tokenizeRawTweetText(s)
        stags = tags[st:st+len(tokens)]
        st = len(tokens)
        butlocs = findButs(tokens)
        # take last last "but" location
        if len(butlocs)>0:
            loc = butlocs[-1]
            finaltokens = tokens[loc+1:]
            stags = stags[loc+1:]
            newsent = " ".join(finaltokens)
            finaltwt = finaltwt + newsent
            finaltags=finaltags+stags
        else:
            finaltwt = finaltwt+s
            finaltags=finaltags+stags
            
    return (finaltwt, finaltags)

def findIfs(tokens):
    iflocs= []
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        normt = removeRepeats(t)
        if normt=="if" or normt=="if_neg":
            iflocs.append(ti)
    return iflocs

def findThens(tokens):
    thenlocs= []
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        normt = removeRepeats(t)
        if normt=="then" or normt=="then_neg":
            thenlocs.append(ti)
    return thenlocs

def findCommas(tokens):
    commalocs= []
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        normt = removeRepeats(t)
        if normt=="," or normt==",_neg":
            commalocs.append(ti)
    return commalocs

def findUntilUnless(tokens):
    unlocs= []
    for ti in range(0, len(tokens)):
        t = tokens[ti]
        normt = removeRepeats(t)
        if normt=="until" or normt=="until_neg" or normt=="unless" or normt=="unless_neg":
            unlocs.append(ti)
    return unlocs

def findIncase(tokens):
    incaselocs= []
    for ti2 in range(1, len(tokens)):
        ti1 = ti2-1
        t1 = tokens[ti1]
        t2 = tokens[ti2]
        normt1 = removeRepeats(t1)
        normt2 = removeRepeats(t2)
        if (normt1=="in" and normt2=="case") or (normt1=="in_neg" and normt2=="case_neg"):
            incaselocs.append(ti1)
    return incaselocs

def removeIncasePosterior(twt, tags):
    # in case ____, _____
    # in case ____ <pos_tag hint> ____
    sent_tokenize_list = sent_tokenize(twt)
    finaltwt = ""
    finaltags = []
    st = 0
    for s in sent_tokenize_list:
        tokens = tw.tokenizeRawTweetText(s)
        stags = tags[st:st+len(tokens)]
        st = len(tokens)
        iclocs = findIncase(tokens)
        commalocs2 = []
        if len(iclocs)>0:
            loc = iclocs[-1]
            commalocs = findCommas(tokens)
            for cl in commalocs:
                if cl > loc:
                    commalocs2.append(cl)
        if len(commalocs2)>0:
            endlocs = commalocs2
            endloc = min(endlocs)
            beforeloctokens = tokens[:loc]
            beforelocstags = stags[:loc]
            afterendloctokens = tokens[endloc+1:]
            afterendlocstags = stags[endloc+1:]
            finaltokens = beforeloctokens + afterendloctokens
            finaltags = beforelocstags+afterendlocstags
            newsent = " ".join(finaltokens)
            finaltwt = finaltwt + newsent
        else:
            finaltwt = finaltwt+s
            finaltags=finaltags+stags
            
    return (finaltwt, finaltags)

def removeUnlessUntilPosterior(twt, tags):
    # unless_____, ______
    # until _____, ______
    # @TODO: unless_____ <pos_tag hint> ______
    # @TODO: until _____<postag hint> ______
    sent_tokenize_list = sent_tokenize(twt)
    finaltwt = ""
    finaltags = []
    st = 0
    for s in sent_tokenize_list:
        tokens = tw.tokenizeRawTweetText(s)
        stags = tags[st:st+len(tokens)]
        st = len(tokens)
        unlocs = findUntilUnless(tokens)
        commalocs2=[]
        if len(unlocs)>0:
            loc = unlocs[-1]
            commalocs = findCommas(tokens)
            for cl in commalocs:
                if cl > loc:
                    commalocs2.append(cl)
        if len(commalocs2)>0:
            endlocs = commalocs2
            endloc = min(endlocs)
            beforeloctokens = tokens[:loc]
            beforelocstags = stags[:loc]
            afterendloctokens = tokens[endloc+1:]
            afterendlocstags = stags[endloc+1:]
            finaltokens = beforeloctokens + afterendloctokens
            finaltags = beforelocstags+afterendlocstags
            newsent = " ".join(finaltokens)
            finaltwt = finaltwt + newsent
        else:
            finaltwt = finaltwt+s
            finaltags=finaltags+stags
            
    return (finaltwt, finaltags)

def removeIfPosterior(twt, tags):
    # if____ then____
    # if____, ____
    # even if _____ then ____
    # even if _____, _____
    # @TODO: _____ if ____
    # @TODO: if____ <pos_tag hint> ____
    # @TODO: _____ even if _____
    # @TODO: even if____ <pos_tag hint> ____
    sent_tokenize_list = sent_tokenize(twt)
    finaltwt = ""
    finaltags = []
    st = 0
    for s in sent_tokenize_list:
        tokens = tw.tokenizeRawTweetText(s)
        stags = tags[st:st+len(tokens)]
        st = len(tokens)
        iflocs = findIfs(tokens)
        thenlocs2=[]
        commalocs2=[]
        if len(iflocs)>0:
            loc = iflocs[-1]
            if loc>0 and (removeRepeats(tokens[loc-1])=="even" or removeRepeats(tokens[loc-1])=="even_neg"):
                loc = loc-1 # handling "even if"
            thenlocs = findThens(tokens)
            commalocs = findCommas(tokens)
            for tl in thenlocs:
                if tl > loc:
                    thenlocs2.append(tl)
            for cl in commalocs:
                if cl > loc:
                    commalocs2.append(cl)
        if len(thenlocs2)>0 or len(commalocs2)>0:
            endlocs = thenlocs2 + commalocs2
            endloc = min(endlocs)
            # handle "then" after comma
            for tl in thenlocs2:
                if tl==endloc+1:
                    endloc=tl
            beforeloctokens = tokens[:loc]
            beforelocstags = stags[:loc]
            afterendloctokens = tokens[endloc+1:]
            afterendlocstags = stags[endloc+1:]
            finaltokens = beforeloctokens + afterendloctokens
            finaltags = beforelocstags+afterendlocstags
            newsent = " ".join(finaltokens)
            finaltwt = finaltwt + newsent
        else:
            finaltwt = finaltwt+s
            finaltags=finaltags+stags
            
    return (finaltwt, finaltags)

def removeCondPosterior(twt, tags):
    iftwt, iftags = removeIfPosterior(twt, tags)
    untwt, untags = removeUnlessUntilPosterior(twt, tags)
    ictwt, ictags = removeIncasePosterior(twt, tags)
    twtlen = len(twt)
    iflen = len(iftwt)
    unlen = len(untwt)
    iclen = len(ictwt)
    if iflen<twtlen:
        return (iftwt, iftags)
    elif iclen<twtlen:
        return (ictwt, ictags)
    elif unlen<twtlen:
        return (untwt, untags)
    else:
        return (twt, tags)
            
            
##if __name__ == "__main__":
##    #twt = "if you work hard, then you will succeed."
##    #twt = "even if things don't go as planned, you must keep fighting."
##    #tags = "a b c d , e f g h ,"
##    #tags = "a b c d e f g , h i j k ,"
##    #twt = "Try to be a good person even if others are not nice." # not done yet
##    #tags = "a b c d e f g h i j k l ,"
##    twt = "In case things don't work out, try again! Don't worry so much."
##    tags = "a b c d e f , g h , i j k l , "
##    tags = tags.split()
##    print twt
##    print tags
##    print removeIncasePosterior(twt, tags)
