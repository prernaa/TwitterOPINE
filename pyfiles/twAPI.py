import tweepy



def getTwAPI():
    # Consumer keys and access tokens, used for OAuth
    consumer_key = 'O5FP9bDaInYDSz1vAxO6X9XAj'
    consumer_secret = 'Nq0rYe9qIV9BQJ30XjhENs321MahnfGSmoaFtBUP9rzA6DsgaI'
    access_token = '370543757-7feaqkZjZKUxRNJHkrUWpDFP9TYih5dBTroV9mKF'
    access_token_secret = '7unJq3FIz2sOE27LBBAGyN3yBZzpb8xqkcZpmDIryHndR'    
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    return api

def searchTw(api, terms, maxnum):
    twts = []
    results = tweepy.Cursor(api.search, count=maxnum, q=terms, lang='en').items(maxnum)
    #print "results obtained"
    tc = 0
    for tweet in results:
        tc=tc+1
        #print tc
        if tc>maxnum:
            break
        try:
            #twtdict = {"text" : tweet.text.encode('utf-8')}
            if tweet.retweeted is True:
                print "found retweet"
                continue
            twtdict = {}
            twtdict["id"] = str(tweet.id_str)
            twtdict["created"] = str(tweet.created_at)
            twtdict["text"] = unicode(tweet.text).encode('utf-8', 'ignore').encode('string_escape')
            twtdict["source"] = unicode(tweet.source).encode('utf-8', 'ignore')
            twtdict["user_id"] = tweet.author.id_str
            twtdict["user_name"] = unicode(tweet.author.name).encode('utf-8', 'ignore')
            twtdict["user_screen_name"] = unicode(tweet.author.screen_name).encode('utf-8', 'ignore')
            twtdict["user_location"] = unicode(tweet.author.location).encode('utf-8', 'ignore')
            twtdict["user_time_zone"] = unicode(tweet.author.time_zone).encode('utf-8', 'ignore')
            twtdict["user_statuses_count"] = unicode(tweet.author.statuses_count).encode('utf-8', 'ignore')
            twtdict["user_friends_count"] = unicode(tweet.author.friends_count).encode('utf-8', 'ignore')
            twtdict["user_followers_count"] = unicode(tweet.author.followers_count).encode('utf-8', 'ignore')
            twtdict["user_description"] = unicode(tweet.author.description).encode('utf-8', 'ignore').encode('string_escape')
            twts.append(twtdict)
            
        except UnicodeEncodeError, e:
            print "unicode encode error ",str(e)
            pass
        except UnicodeDecodeError, e:
            print "unicode decode error ",str(e)
            pass
        
    return twts
        
