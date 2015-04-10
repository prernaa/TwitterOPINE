package mainpkg;
import indexerpkg.Indexer;
import indexerpkg.MySQLAccess;
import predictpkg.Classifier;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.common.SolrDocumentList;

import querypkg.Querying;
import cmu.arktweetnlp.*;
import cmu.arktweetnlp.Tagger.TaggedToken;
import crawlerpkg.*;

public class RunEngine {
	
	//String[] tags2use = {"N","^","S", "Z", "V", "A", "R", "!", "#", "E", "G", "M"};
	public static String[] tags2use = {"N","^","S", "Z", "V", "A", "#", "M"};
	public static String[] concepts2use = {"N N", "N V", "V N", "A N", "R N", "P N", "P V", "R A", "^ ^", "N ^", "^ N", "^ V", "V ^", "A ^", "R ^", "P ^", "Z V", "V Z", "A Z", "R Z", "P Z", "S V", "V S", "A S", "R S", "P S", "V T", "! !", "! V", "V !", "N !", "! N"};
	public static String[] withtags2use = {"#", "E", "G"};
	public static String[] stopwords = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"};
	public static List<TaggedToken> tagQuery(String twtq) {
		String modelfilename ="/cmu/arktweetnlp/model.20120919";
		/*File f = new File(modelfilename);
		if(f.exists() && !f.isDirectory()){
			System.out.printf("File exists");
		}*/
		Tagger tagger = new Tagger();
		try {
			tagger.loadModel(modelfilename);
			List<TaggedToken> taggedTokens = tagger.tokenizeAndTag(twtq);
			System.out.printf("Printing tags");
			for (TaggedToken token : taggedTokens) {
				System.out.printf("%s\t%s\n", token.tag, token.token);
			}
			return taggedTokens;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
	
	//public static ArrayList<HashMap<String, String>> processRawQuery(String twtq) throws Exception {
	public static String processRawQuery(String twtq) throws Exception {
		// TODO Auto-generated method stub
		System.out.println("engine called");
		List<TaggedToken> taggedTokens = tagQuery(twtq);
		ArrayList<HashMap<String, String>> returneddocs = new ArrayList<HashMap<String, String>>();
		String jsondocs = "";
		if (taggedTokens != null){
			System.out.printf("Tagged");
			Crawler newcrawler = new Crawler();
			ArrayList <ArrayList <String>> unibigrams = newcrawler.generateQueryForSolr(taggedTokens, tags2use, concepts2use, withtags2use, stopwords);
			//check if already indexed by calling querying class 
			
	  		Querying check_query = new Querying();
	  		int docssize = check_query.queryb4Crawling(unibigrams);
	  		System.out.println("Docs size:"+docssize);
			
	  		if(docssize==0)
	    	{
	  			System.out.println("Length of stop1");
	  			System.out.println(stopwords.length);
	  			newcrawler.crawl(taggedTokens, tags2use, concepts2use, withtags2use, stopwords, 20);
	  			System.out.println("Predicting for new data");
	  			String pypath = newcrawler.getPythonPath();
	  			Classifier newclassifier = new Classifier();
	  			newclassifier.predict(pypath);
	    	}
	  		else{
	  			System.out.println("Already indexed. No crawling needed....");
	  		}
			
			//call indexer class from here
			MySQLAccess s= new MySQLAccess();
	  	  	Indexer indexSqlRecords=new Indexer();
	  	  	ResultSet rs, rs2;
	  		rs=s.readDataBase();
	  		rs2=rs;
	  		indexSqlRecords.addResultSet(rs); 	  		
	  		s.markIndexed(rs2);
	  		s.close();
	  		
	  		//Call Querying class 
	  		Querying obj = new Querying();
	  		//returneddocs = obj.query(twtq, "");
	    	//System.out.println("Run Engine 1st result:"+returneddocs.get(0));
	  		ArrayList <String> retQuery = obj.queryAfterIndexing(unibigrams);
	  		jsondocs = retQuery.get(0);
	  		/*String toRun = retQuery.get(1);
	  		System.out.println(toRun);
	  		if (toRun=="Run"){
	  			System.out.println("Running Predict");
	  			String pypath = newcrawler.getPythonPath();
	  			Classifier newclassifier = new Classifier();
	  			newclassifier.predict(pypath);
	  		}*/
		}
		else{
			//return via post that query cannot be processed
	        
		}
		//System.out.println(jsondocs);
		return jsondocs;
	}

}
