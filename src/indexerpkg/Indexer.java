package indexerpkg;


import java.io.IOException;
import java.net.MalformedURLException;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;

import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrServer;
import org.apache.solr.common.SolrInputDocument;


public class Indexer
{
	private static String url = "http://localhost:8983/solr/collection1/";
	private static HttpSolrServer solrCore;
	public Indexer()throws MalformedURLException
	{
		solrCore = new HttpSolrServer(url);
	}
	public void addResultSet(ResultSet rs) throws SQLException,
    SolrServerException, IOException
    {
		if(rs.first())
		{
			int innerCount = 0;
	        Collection<SolrInputDocument> docList = new ArrayList<SolrInputDocument>();
	        ResultSetMetaData rsm = rs.getMetaData();
	        int numColumns = rsm.getColumnCount();
	        String[] colNames = new String[numColumns + 1];
	
	        /**
	         * JDBC numbers the columns starting at 1, so the normal java convention
	         * of starting at zero won't work.
	         */
	        
	        for (int i = 1; i < (numColumns + 1); i++)
	        {
	            colNames[i] = rsm.getColumnName(i);           
	        }
	        SolrInputDocument doc=new SolrInputDocument();
	        System.out.println("new document first");
            //doc = new SolrInputDocument();
            System.out.println("starting add first");
            doc.addField("id", rs.getString(colNames[1]));
            
            for(int k=2; k<numColumns+1; k++)
            {
            	doc.addField(colNames[k],rs.getString(colNames[k]));
            }
            docList.add(doc);
            
	        ArrayList<String> indexed_data = new ArrayList<String>();
	        
	        System.out.println("indexing");
	        System.out.println("calling result set");
	       
	        while (rs.next())
	        {
	            //count++;
	        	System.out.println("new document");
	            doc = new SolrInputDocument();
	            System.out.println("starting add");
	            doc.addField("id", rs.getString(colNames[1]));
	            for(int k=2; k<numColumns+1; k++)
	            {
	            	doc.addField(colNames[k],rs.getString(colNames[k]));
	            }
	            docList.add(doc); 	
	        }
	        
	        solrCore.add(docList); //Commit changes to solr 
	        solrCore.commit();
	        System.out.println("indexing done");
	    }
		 System.out.println("out of indexer");
    }
	/*public static void main(String[] args) {
	  	  try {  		  
	  		MySQLAccess s= new MySQLAccess();
	  	  	Indexer indexSqlRecords=new Indexer();
	  	  	ResultSet rs;
	  		rs=s.readDataBase();
	  		indexSqlRecords.addResultSet(rs); 
	  		s.markIndexed(rs);
	  		
	  		s.close();
	  	  } catch (Exception e) {
	  		 e.getMessage();
	  		 e.printStackTrace();
	  	}  
	  }*/
	}
/*http://localhost:8983/solr/collection1/update?stream.body=<delete><query>*:*</query></delete>
http://localhost:8983/solr/collection1/update?stream.body=<commit/>*/

