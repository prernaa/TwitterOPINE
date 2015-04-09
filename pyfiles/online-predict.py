clfPath = "/Users/Prerna/Desktop/Prerna/NTU/Courses-Year4-Sem2/CZ4034-InfoRet/code_app/TwitterOPINE/pyfiles/training_2015-02-26_14-43-43__100K"

import hickledir.hickle as hkl
import twokenize as tw
import processEmo as emh
import stFeatureHandler as fh
import rulesSVM as rsvm
import rulesPredict as rp
import mysql.connector

def openFile(savepath, filename):
    #return joblib.load("./"+savepath+"/"+filename+".joblib.pkl");
    return hkl.load(savepath+"/"+filename+".hkl", safe=False);

def updateTagTokenMismatch(uneq, lc, nonegtokens, postaglst):
    if len(nonegtokens)!=len(postaglst):
        uneq.append([lc,len(nonegtokens),len(postaglst)])

def getEmoRulesLbl(nonegtokens, postaglst, emoLabels):
    cemodict = emh.getEmoFeatures(nonegtokens, postaglst)
    epos = cemodict["cpos"]
    eneg = cemodict["cneg"]
    if epos>0 and eneg==0:
        emoLabels.append("positive")
        print "Rule = positive ",epos," ",eneg
    elif eneg>0 and epos==0:
        emoLabels.append("negative")
        print "Rule = negative ",epos," ",eneg
    else:
        emoLabels.append("unknown")

def predictLowScoreNew(corpusLst, poscorpus, resultDecision, thres, isStrict):
    lowScoreLabels = []
    for li in range(0, len(corpusLst)):
        negtwt = corpusLst[li]
        pos = poscorpus[li]
        d = resultDecision[li]
        if abs(d)<thres:
            lowScoreLabels.append(rp.applyCommonRuleNew(negtwt, pos, isStrict))
        else:
            lowScoreLabels.append("notcomputed")
    return lowScoreLabels


def getVectors():
    print "getting vectors"
    db = mysql.connector.connect(host="localhost", user="root", password="sentiment", database="TwitterSearch")
    cur = db.cursor()
    db.autocommit = True
    # fetch all tweets with unknown polarity
    sql = "SELECT * FROM tweetTable2 WHERE autopolarity_lbl=%s"
    cur.execute(sql,["UNKNOWN"])
    res = cur.fetchall()
    ids = []
    corpus = []
    poscorpus = []
    emoRulesLabels = []
    uneq = []
    lc = 0
    for r in res:
        lc = lc+1
        #print "predicting for line ",lc
        twt_norm = r[3]
        twt_neg = r[4]
        twt_pos = r[5]
        nonegtokens = tw.tokenizeRawTweetText(twt_norm)
        negtokens = tw.tokenizeRawTweetText(twt_neg)
        postaglst = twt_pos.split()
        updateTagTokenMismatch(uneq, lc, nonegtokens, postaglst)

        # modifying n-grams for "but"
        twt_new_neg, newpos = rsvm.removeButAnterior(twt_neg, postaglst)
        # modifying n-grams for conditionals
        if len(twt_new_neg)==len(twt_neg):
            twt_new_neg, newpos = rsvm.removeCondPosterior(twt_neg, postaglst)
        corpus.append(twt_new_neg)
        poscorpus.append(newpos)

        # applying emoticon rules
        getEmoRulesLbl(nonegtokens, postaglst, emoRulesLabels)

        ids.append(r[0])

    print "fetching n-grams from corpus"
    ngramvect = openFile(clfPath, "ngramvect")
    ngramFeatures = ngramvect.transform(corpus)
    allFeatures = ngramFeatures

    cur.close()
    db.close()

    return (ids, allFeatures, corpus, poscorpus, emoRulesLabels)


def MultiRulesResults(ids, resultLabels, resultDecision, RulesLabelsList, RulesFlagsList):
    db = mysql.connector.connect(host="localhost", user="root", password="sentiment", database="TwitterSearch")
    cur = db.cursor()
    db.autocommit = True

    crulesLst = [0]*len(RulesLabelsList)

    if not(False in RulesFlagsList):
        for ti in range(0, len(resultLabels)):
            twtid = ids[ti]
            svmlbl = resultLabels[ti]
            applied = False
            finallbl = "UNKNOWN";
            finalscore = 0.0
            for ri in range(0, len(RulesLabelsList)):
                rule = RulesLabelsList[ri]
                rulelbl = rule[ti]
                if not applied and rulelbl == "positive":
                    crulesLst[ri]=crulesLst[ri]+1
                    finallbl = rulelbl
                    finalscore = 4.00
                    #fw.write(rulelbl)
                    #fw.write("\t")
                    #fw.write(str(4.00))
                    #fw.write('\n')
                    applied=True
                elif not applied and rulelbl == "negative":
                    crulesLst[ri]=crulesLst[ri]+1
                    finallbl = rulelbl
                    finalscore = -4.00
                    #fw.write(rulelbl)
                    #fw.write("\t")
                    #fw.write(str(-4.00))
                    #fw.write('\n')
                    applied=True
            if not applied:
                finallbl = svmlbl
                finalscore = resultDecision[ti]
                #fw.write(svmlbl)
                #fw.write("\t")
                #fw.write(str(resultDecision[ti]))
                #fw.write('\n')
            sql = "UPDATE tweetTable2 SET autopolarity_lbl='"+finallbl+"', autopolarity_score="+str(finalscore)+", autopolarity_offline=0 WHERE twitter_id="+str(twtid)
            #cur.execute(sql, tuple([finallbl, finalscore, 0]))
            cur.execute(sql)

    cur.close()
    db.close()    

def predict():
    print "running predict code"
    ids, XVec, corpus, poscorpus, emoRulesLabels = getVectors()

    print "opening clf file"
    clf = openFile(clfPath, "clf")
    print "predicting labels"
    resultLabels = clf.predict(XVec)
    resultDecision = clf.decision_function(XVec)

    lowscorethresh = 0.5
    lowScoreLbls = predictLowScoreNew(corpus, poscorpus, resultDecision, lowscorethresh, isStrict=False)

    MultiRulesResults(ids, resultLabels, resultDecision, [emoRulesLabels, lowScoreLbls], [True, True])

if __name__ == "__main__":
    predict()
