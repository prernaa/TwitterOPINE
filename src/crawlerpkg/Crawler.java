package crawlerpkg;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.ProcessBuilder.Redirect;
import java.util.*;

import cmu.arktweetnlp.Tagger.TaggedToken;

public class Crawler {
	
	public static String pathPyFiles = "/Users/Prerna/Desktop/Prerna/NTU/Courses-Year4-Sem2/CZ4034-InfoRet/code_app/TwitterOPINE/pyfiles/";
	
	public String generateQuery(List<TaggedToken> twtqtokens, String[] tags2use, String[] concepts2use, String[] withtags2use, String[] stopwords) {
		System.out.println("Generating Query");
		List<String> querylist=new ArrayList<String>();
		List<String> splittedlist=new ArrayList<String>();
		List<String> splittedlisttags=new ArrayList<String>();
		System.out.println("Length of stop");
		System.out.println(stopwords.length);
		
		// add unigrams (includes hashtags)
		for (TaggedToken token : twtqtokens) {
			if (!Arrays.asList(stopwords).contains(token.token)){
				System.out.println(token.token);
				System.out.println("Not in stop");
				if( Arrays.asList(tags2use).contains(token.tag) ){
					querylist.add(token.token);
					System.out.println(token.token);
					System.out.println("ADDED");
				}
				splittedlist.add(token.token);
				splittedlisttags.add(token.tag);
			}
			else{
				System.out.println("Remove stop");
				System.out.println(token.token);
			}
		}
		System.out.println("Querylist size1:");
		System.out.println(querylist.size());
		// add bigrams
		for (int i = 1; i < splittedlist.size(); i++) {           
		    String prev = splittedlist.get(i-1);
		    String prevtag = splittedlisttags.get(i-1);
		    String curr = splittedlist.get(i);
		    String currtag = splittedlisttags.get(i);
		    String bi = "\""+prev+" "+curr+"\"";
		    String bitags = prevtag+" "+currtag;
		    Boolean isprevinuse = Arrays.asList(tags2use).contains(prevtag);
		    Boolean iscurrinuse = Arrays.asList(tags2use).contains(currtag);
		    Boolean isprevwithinuse = Arrays.asList(withtags2use).contains(prevtag);
		    Boolean iscurrwithinuse = Arrays.asList(withtags2use).contains(currtag);
		    System.out.println(bi);
			System.out.println(bitags);
		    if( Arrays.asList(concepts2use).contains(bitags) ){
				querylist.add(bi);
				System.out.println("Bi Added:");
			}
		    else if ((isprevinuse && iscurrwithinuse) || (iscurrinuse && isprevwithinuse)) {
		    	querylist.add(bi);
		    	System.out.println("Bi Added2:");
		    }
		}
		System.out.println("Querylist size:");
		System.out.println(querylist.size());
		String query = "";
		if (querylist.size()>0){
			String q1 = querylist.get(0);
			query = query+q1;
			for (int i = 1; i < querylist.size(); i++) { 
				query = query+" ";
				query = query+querylist.get(i);
			}
		}
		System.out.println("Query is as follows:");
		System.out.println(query); //printed to console for debugging
		return query;
	}

	public void crawl(List<TaggedToken> twtqtokens, String[] tags2use, String[] concepts2use, String[] withtags2use, String[] stopwords, int maxnum) {
		String querystr = generateQuery(twtqtokens, tags2use, concepts2use, withtags2use, stopwords);
		System.out.println("API call for query");
		querystr = querystr.replace("\"","\\\""); // escaping double quotes
		System.out.println("query string");
		System.out.println(querystr);
		String pythonScriptPath = pathPyFiles+"pycrawler.py";
		System.out.println("pythonScriptPath");
		System.out.println(pythonScriptPath);
		try {
			ProcessBuilder pb = new ProcessBuilder("/usr/bin/python",pythonScriptPath,querystr);
	        pb.redirectOutput(Redirect.INHERIT);
	        Process p = pb.start();
	        int success = p.waitFor();
	        System.out.println("waitFor");
			System.out.println(success);
		} catch (IOException | InterruptedException e) {
			// TODO Auto-generated catch block
			System.out.println("Crawling Failed!");
			e.printStackTrace();
		}
	}

}
