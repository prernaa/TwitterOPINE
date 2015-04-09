<%@ page language="java" contentType="application/json; charset=UTF-8"
    import="java.util.*,java.io.*,mainpkg.RunEngine" %>
<%
response.setContentType("application/json");
System.out.println("Hello I am crawlhandler.jsp");
String twtq = request.getParameter("tweetsearch");
String usrq = request.getParameter("usersearch");
System.out.println(twtq);
System.out.println(usrq);
String jsondocs = RunEngine.processRawQuery(twtq);
//System.out.println(jsondocs);
out.print(jsondocs);

%>