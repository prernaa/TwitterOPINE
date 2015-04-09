package indexerpkg;

import java.io.Closeable;
import java.net.MalformedURLException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;

import org.apache.solr.client.solrj.response.QueryResponse;
/**
* The MySQLAccess program connects to our localhost database phpmyadmin and gets all the 
* records stored in the table. 
* For connection to database , username is root and password is wampmysql.
* @author  Information Retrieval Group 18
* @version 1.0
* @since   2014-04-14 
*/
public class MySQLAccess {
	
  private Connection connect = null;
  private Statement statement = null;
  private ResultSet resultSet = null;
  private int count;
  /**
   * Reads all records from the database 
   * 
   * @throws MalformedURLException
   */
  public ResultSet readDataBase() throws Exception {
    try {
    	
      //load the MySQL driver
      Class.forName("com.mysql.jdbc.Driver");
      
      //setup the connection with the the database
      connect = DriverManager
          .getConnection("jdbc:mysql://localhost:3306","root","sentiment");

      //statements allow to issue SQL queries to the database
      statement = connect.createStatement();
      
      //resultSet gets the result of the SQL query
      resultSet = statement.executeQuery("select * from TwitterSearch.tweetTable2 where indexed=0");
      
      //return the resultSet obtained
      return resultSet;
      
    } catch (Exception e) {
      throw e;
    }

  }
  public void markIndexed(ResultSet rs) throws SQLException, Exception
  {
	  System.out.println("updating");
	  System.out.println(rs.getRow());
	  
	  //while(rs.next())
	  //{
		  System.out.println("in while");
		  //load the MySQL driver
	      Class.forName("com.mysql.jdbc.Driver");
	      System.out.println("driver loaded");
	      //setup the connection with the the database
	      connect = DriverManager
	          .getConnection("jdbc:mysql://localhost:3306","root","sentiment");
	      System.out.println("connection successful");
	      //statements allow to issue SQL queries to the database
	      statement = connect.createStatement();
	      //System.out.println("updating");
	      //System.out.println(rs.getBigDecimal(0));
	      String query = "Update TwitterSearch.tweetTable2 SET indexed=1 where indexed=0";
		  statement.executeUpdate(query);
	  //}
	  
  }
  public int getNumberofTweets() throws Exception
  {
	  try {
	    	
	      //load the MySQL driver
	      Class.forName("com.mysql.jdbc.Driver");
	      
	      //setup the connection with the the database
	      connect = DriverManager
	          .getConnection("jdbc:mysql://localhost:3306","root","sentiment");

	      //statements allow to issue SQL queries to the database
	      statement = connect.createStatement();
	      
	      //resultSet gets the result of the SQL query
	      
	      ResultSet resultCount = statement.executeQuery("select COUNT(*) from TwitterSearch.tweetTable2");
	      resultCount.next();
	      System.out.println(resultCount.getFetchSize()+" ,"+"count: "+resultCount.getInt(1));
	      //return the resultSet obtained
	      return resultCount.getInt(1);
	      
	    } catch (Exception e) {
	      throw e;
	    }

  }

  /**
   * Closes all connections
   */
  public void close() {
   try {
	resultSet.close();
	statement.close();
	connect.close() ;
	} catch (SQLException e) {		
		e.printStackTrace();
	};   
  }

  
  } 