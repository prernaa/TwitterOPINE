<%@ page language="java" contentType="text/html; charset=US-ASCII"
    pageEncoding="US-ASCII" import="java.util.*,java.io.*,mainpkg.RunEngine" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=US-ASCII">
<title>Crawling Form Handler (NO UI)</title>
</head>
<body>
<%
String twtq = request.getParameter("tweetsearch");
String usrq = request.getParameter("usersearch");
System.out.println(twtq);
System.out.println(usrq);
RunEngine.processRawQuery(twtq);
%>

</body>
</html>