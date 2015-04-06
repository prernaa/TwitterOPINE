package mainpkg;
import java.io.File;
import java.io.IOException;
import java.util.*;

import cmu.arktweetnlp.*;
import cmu.arktweetnlp.Tagger.TaggedToken;
import crawlerpkg.*;

public class RunEngine {
	
	//String[] tags2use = {"N","^","S", "Z", "V", "A", "R", "!", "#", "E", "G", "M"};
	public static String[] tags2use = {"N","^","S", "Z", "V", "A", "#", "M"};
	public static String[] concepts2use = {"N N", "N V", "V N", "A N", "R N", "P N", "P V", "R A", "^ ^", "N ^", "^ N", "^ V", "V ^", "A ^", "R ^", "P ^", "Z V", "V Z", "A Z", "R Z", "P Z", "S V", "V S", "A S", "R S", "P S", "V T"};
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
	
	public static void processRawQuery(String twtq) {
		// TODO Auto-generated method stub
		System.out.println("engine called");
		List<TaggedToken> taggedTokens = tagQuery(twtq);
		
		if (taggedTokens != null){
			System.out.printf("Tagged");
			
			Crawler newcrawler = new Crawler();
			System.out.println("Length of stop1");
			System.out.println(stopwords.length);
			newcrawler.crawl(taggedTokens, tags2use, concepts2use, withtags2use, stopwords, 50);
			System.out.println("After Query generation");
		}
		else{
			//return via post that query cannot be processed
		}

	}

}
