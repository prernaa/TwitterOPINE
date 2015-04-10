package querypkg;

import indexerpkg.MySQLAccess;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.Charset;
import java.sql.ResultSet;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrServer;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrDocumentList;
import org.noggit.JSONUtil;

import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;

import java.util.regex.Pattern;
import java.util.regex.Matcher;
public class Querying {

	 
    private static String url = "http://localhost:8983/solr/collection1/";
    private static HttpSolrServer server;

    public Querying() throws MalformedURLException
    {
    	server = new HttpSolrServer(url);
    }
    
        
    public int queryb4Crawling(ArrayList<ArrayList<String>> user_query) throws Exception
    {
    	SolrQuery solr_query = new SolrQuery();
    	String queryStr="(";
    	ArrayList<String> unigrams=user_query.get(0);
    	
    	for(int i=0; i<unigrams.size();i++)
    	{
    		String word = unigrams.get(i).replace("#", "");
    		if(i!=unigrams.size()-1)
    			queryStr = queryStr + "tweet_norm:*"+word+"* OR ";
    		else
    			queryStr = queryStr + "tweet_norm:*"+word+"*)";
    	}
		//DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		//Date date = new Date();
		//System.out.println(dateFormat.format(date)); //2014/08/06 15:59:48
		//queryStr = queryStr + "date_crawled:*"+dateFormat.format(date).split(" ")[0]+"*";
    	System.out.println(queryStr);
    	solr_query.setQuery(queryStr);
    	
    	MySQLAccess obj = new MySQLAccess();
        int count = obj.getNumberofTweets();
    	solr_query.setRows(count);
        //query.addSortField( "user_followers_count", SolrQuery.ORDER.asc );
        QueryResponse rsp = server.query( solr_query );
        System.out.println("Querying");
        SolrDocumentList docs = rsp.getResults();
        return docs.size();

    }
    
    public ArrayList <String> queryAfterIndexing(ArrayList<ArrayList<String>> user_query) throws Exception
    {
    	ArrayList<String> unigrams = user_query.get(0);
    	ArrayList<String> bigrams = user_query.get(1);
    	HashMap<String, Integer> hm_uni = new HashMap<String, Integer>();
    	HashMap<String, Integer> hm_bi = new HashMap<String, Integer>();
    	
    	//unigrams permutation
    	for(int i=0; i<unigrams.size(); i++)
    	{
    		hm_uni.put(unigrams.get(i), 1);
    		if(unigrams.get(i).charAt(0)=='#')
    			hm_uni.put(unigrams.get(i).substring(1), 0);
    		else
    			hm_uni.put("#"+unigrams.get(i), 0);
    	}
    	//bigrams permutation
    	for(int i=0; i<bigrams.size(); i++)
    	{
    		String[] bigs = bigrams.get(i).split(" ");
    		hm_bi.put(bigrams.get(i), 1);
    		String stripped1=bigs[0];
    		String stripped2=bigs[1];
    		if(bigs[0].contains("#"))
    			stripped1=bigs[0].replace("#", "");
    		if(bigs[1].contains("#"))
    			stripped2=bigs[1].replace("#", "");
    		String permute1 = stripped1 + " " + stripped2;
    		String permute2 = "#"+stripped1+" "+stripped2;
    		String permute3 = stripped1+" #"+stripped2;
    		String permute4 = "#"+stripped1+" #"+stripped2;
    		if(!hm_bi.containsKey(permute1))
    			hm_bi.put(permute1, 0);
    		if(!hm_bi.containsKey(permute2))
    			hm_bi.put(permute2, 0);
    		if(!hm_bi.containsKey(permute3))
    			hm_bi.put(permute3, 0);
    		if(!hm_bi.containsKey(permute4))
    			hm_bi.put(permute4, 0);
    	}
    	
    	//query generation
    	SolrQuery solr_query = new SolrQuery();
    	String queryStr="";
    	
    	Iterator it = hm_uni.entrySet().iterator();
    	while(it.hasNext())
    	{
    		Map.Entry pair = (Map.Entry) it.next();
    		String unigram = (String) pair.getKey();
    		int value = (int) pair.getValue();
    		
    		if(value == 1)
    		{
    			queryStr = queryStr + "tweet_norm:*"+unigram+"*^10 OR ";
    		}
    		else
    		{
    			queryStr = queryStr + "tweet_norm:*"+unigram+"*^6 OR ";
    		}
    	}
    	Iterator it2 = hm_bi.entrySet().iterator();
    	while(it2.hasNext())
    	{
    		Map.Entry pair = (Map.Entry) it2.next();
    		String bigram = (String) pair.getKey();
    		int value = (int) pair.getValue();
    		String[] bigs = bigram.split(" ");
    		if(value==1)
    			queryStr= queryStr+ "(tweet_norm:*"+bigs[0]+"* AND tweet_norm:*"+bigs[1]+"*)^20 OR ";
    		else
    			queryStr= queryStr+ "(tweet_norm:*"+bigs[0]+"* AND tweet_norm:*"+bigs[1]+"*)^10 OR ";
    	}    	
    	
    	
    	System.out.println(queryStr.substring(0, queryStr.length()-4));
    	solr_query.setQuery(queryStr.substring(0, queryStr.length()-4));
    	
    	MySQLAccess obj = new MySQLAccess();
        int count = obj.getNumberofTweets();
    	solr_query.setRows(count);
    	solr_query.addSortField("score", SolrQuery.ORDER.desc);
        solr_query.addSortField( "user_followers_count", SolrQuery.ORDER.desc );
        System.out.println(solr_query);
        QueryResponse rsp = server.query( solr_query );
        System.out.println("Querying");
        SolrDocumentList docs = rsp.getResults();
        
        int countunk = 0;
        int counttotal = 0;
        for (SolrDocument doc : docs){
        	String lbl = (String) doc.getFieldValue("autopolarity_lbl");
        	counttotal = counttotal+1;
        	if (lbl=="UNKNOWN"){
        		countunk = countunk + 1;
        	}
        	if (counttotal==10){
        		break;
        	}
        }
        String toRunPredict;
        if (countunk!=0){
        	toRunPredict = "Run"; 
        }
        else{
        	toRunPredict = "DontRun"; 
        }
        
        String returnValue = JSONUtil.toJSON(docs); 
        ArrayList <String> retArr = new ArrayList <String>();
        retArr.add(returnValue);
        retArr.add(toRunPredict);
        return retArr;
    }
 
}
