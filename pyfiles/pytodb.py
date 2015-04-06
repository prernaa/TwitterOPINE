import MySQLdb
import datetime

def checkNull(variable):
    if variable.strip()=="" or variable[:6]=="_NONE_":
        return None
    else:
        return variable

def getRecordTupleWithoutSenti(tc, tname, rawlst, normlst, poslst, neglst):
    twitter_id = int(rawlst[0])
##    print "ID = ",twitter_id
    created_at = datetime.datetime.strptime(rawlst[1], '%Y-%m-%d %H:%M:%S')
    tweet_raw = rawlst[2]
    tweet_norm = normlst[2]
    tweet_neg = neglst[2]
    tweet_pos = poslst[2]
    source = checkNull(rawlst[3])
    user_id = int(rawlst[4])
    user_name = checkNull(rawlst[5])
    user_screen_name = checkNull(rawlst[6])
    user_location = checkNull(rawlst[7])
    user_time_zone = checkNull(rawlst[8])
    user_statuses_count = int(rawlst[9])
    user_friends_count = int(rawlst[10])
    user_followers_count = int(rawlst[11])
    user_desc_raw = checkNull(rawlst[12])
    user_desc_norm = checkNull(normlst[12])
    user_desc_pos = checkNull(poslst[12])
    autopolarity_lbl = "UNKNOWN"
    autopolarity_score = 0.0
    autopolarity_offline = -1
    manualpolarity_poscount = 0
    manualpolarity_negcount = 0
    manualpolarity_neucount = 0
    manualpolarity_othercount = 0
    indexed = 0
    pre_crawled = 0
    pre_crawled_file_line = None
    api_query = tname
    date_crawled = datetime.datetime.now()
    columns = "(twitter_id, created_at, tweet_raw, tweet_norm, tweet_neg, tweet_pos, source, user_id, user_name, user_screen_name, user_location, user_time_zone, user_statuses_count, user_friends_count, user_followers_count, user_desc_raw, user_desc_norm, user_desc_pos, autopolarity_lbl, autopolarity_score, autopolarity_offline, manualpolarity_poscount, manualpolarity_negcount, manualpolarity_neucount, manualpolarity_othercount, indexed, pre_crawled, pre_crawled_file_line, api_query, date_crawled)"
    #valuesStr = "(%d, '%s', %s, %s, %s, %s, %s, %d, %s, %s, %s, %s, %d, %d, %d, %s, %s, %s, %s, %f, %d, %d, %d, %d, %d, %d, %d, %s, '%s')"
    valuesStr = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = tuple([twitter_id, created_at.strftime('%Y-%m-%d %H:%M:%S'), tweet_raw, tweet_norm, tweet_neg, tweet_pos, source, user_id, user_name, user_screen_name, user_location, user_time_zone, user_statuses_count, user_friends_count, user_followers_count, user_desc_raw, user_desc_norm, user_desc_pos, autopolarity_lbl, autopolarity_score, autopolarity_offline, manualpolarity_poscount, manualpolarity_negcount, manualpolarity_neucount, manualpolarity_othercount, indexed, pre_crawled, pre_crawled_file_line, api_query, date_crawled.strftime('%Y-%m-%d %H:%M:%S')])
    return (columns, valuesStr, values)

global db
db = MySQLdb.connect(host="localhost", user="root", passwd="sentiment", db="TwitterSearch")
global cur
cur = db.cursor()
db.autocommit(True)

def dbInputWithoutSenti(tLst, fraw, fnorm, fpos, fneg, allowDBinput=True):
    if not allowDBinput:
        cur.close()
        db.close()
        return None
    
    tname = ",".join(tLst)
    
    fInRaw = open(fraw, "r")
    fInNorm = open(fnorm, "r")
    fInPos = open(fpos, "r")
    fInNeg = open(fneg, "r")
    tc = 0
    for line in fInRaw:
        #print "Inserting Line ",tc," of ",tname
        tc = tc + 1
        rawlst = line.split("\t")
        normlst = next(fInNorm).split("\t")
        poslst = next(fInPos).split("\t")
        neglst = next(fInNeg).split("\t")
        
        columns, valuesStr, values = getRecordTupleWithoutSenti(tc, tname, rawlst, normlst, poslst, neglst)

        twtid = values[0]
        #qterm = tname.replace(","," ")
        qterms = set(tLst)

        twtnorm = values[3].strip()
        sql = "SELECT COUNT(*) FROM tweetTable2 WHERE tweet_norm=%s"
        cur.execute(sql,[twtnorm])
        res = cur.fetchone()
        normcount = res[0]

        sql = "SELECT COUNT(*) FROM tweetTable2 WHERE twitter_id="+str(twtid)
        cur.execute(sql)
        res = cur.fetchone()
        idcount = res[0]
        if idcount!=0: # twt id is duplicate => 
            sql = "SELECT api_query, pre_crawled_file_line FROM tweetTable2 WHERE twitter_id="+str(twtid)
            cur.execute(sql)
            res = cur.fetchone()
            qts = res[0]
            filepos = res[1]
            qtslst = set(qts.split(","))
            if qterms != qtslst: # same twt but diff query term
                qtslstfinal = list((qterms | qtslst))
                qts = ",".join(qtslstfinal)
                filepos = None
                sql = "UPDATE tweetTable2 SET api_query=%s WHERE twitter_id="+str(twtid)
                cur.execute(sql, tuple([qts, filepos]))
            else:
                "record already exists"
        elif normcount!=0: # tweet text is duplicate
            sql = "SELECT api_query, pre_crawled_file_line FROM tweetTable2 WHERE tweet_norm=%s"
            cur.execute(sql,[twtnorm])
            res = cur.fetchone()
            qts = res[0]
            filepos = res[1]
            qtslst = set(qts.split(","))
            if qterms != qtslst: # same twt but diff query term
                qtslstfinal = list((qterms | qtslst))
                qts = ",".join(qtslstfinal)
                filepos = None
                sql = "UPDATE tweetTable2 SET api_query=%s WHERE twitter_id="+str(twtid)
                cur.execute(sql, tuple([qts, filepos]))
            else:
                "record already exists"
        else:
            sql = "INSERT INTO tweetTable2 "+columns+" VALUES "+valuesStr
            sqlvals = values
            success = cur.execute(sql, sqlvals)
            if success==0:
                print "Line ",tc," of ",tname," unsuccessful!"


    fInRaw.close()
    fInNorm.close()
    fInPos.close()
    fInNeg.close()
    cur.close()
    db.close()
