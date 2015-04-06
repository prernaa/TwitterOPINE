<%@ page language="java" contentType="text/html; charset=US-ASCII"
    pageEncoding="US-ASCII"%>
<!DOCTYPE html>
<html>
<head>
<!-- Bootstrap -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="bootstrap/css/bootstrap-spacelab.css" rel="stylesheet" media="screen">
    <link href="bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
	<!--[if IE 7]>
	  <link rel="stylesheet" href="path/to/font-awesome/css/font-awesome-ie7.min.css">
	<![endif]-->
	<style type ="text/css">
	body {padding-bottom:70px;background-color: #c0deed;}
	.stdp{ font-size: 15px;}
	.centertxt{text-align:center;}
	.whitebg{background-color: #ffffff;}
	.darkbg{background-color: #0084b4;}
	.darktxt{color: #433e90;}
	.twttxt{
		text-align: left;
		float: left;
		margin-right: 5px;
	}
	.classdisp{
		text-align: center;
		float: right;
	}
	.classpos{
		color: #009933;
	}
	.classneg{
		color: #e50000;
	}
	.classneu{
		color: #1dcaff;
	}
	.classunk{
		color: #000000;
	}
	.usrtxt{
		text-align: right;
	}
	.qicon{
		margin:5px;
	}
	</style>
<title>Twitter OPINE: Twitter OPINion mining Engine</title>
</head>
<body>
<div class = "container-fluid" style = "margin-top:25px; margin-bottom:25px;">
	<div class = "row-fluid vout">
	<div class = "span5 offset1 centertxt darktxt">
	<img src = "img/logo_2.png"/>
	<h2 class="darktxt" style="margin-bottom:-3px;">Twitter OPINE</h2>
	<em style="font-size:14px;">An <strong>OPIN</strong>ion mining search <strong>E</strong>ngine for Twitter</em>
	</div>
	<!-- FORM INPUT -->
	<div class = "vin span5 centertxt darktxt">
	<form id = "searchform" role="form">
    <div class="form-group">
      <label for="Tweet"><strong style="font-size:16px;">Search tweets<strong style="color:#e50000;">*</strong>:</strong></label>
      <input type="text" placeholder="Enter Query (Required)" class="form-control" id="tweetsearch">
    </div>
    <div class="form-group">
      <label for="user"><strong style="font-size:16px;">Filter by user description:</strong></label>
      <input type="text" placeholder="Optional Filter for User Description" class="form-control" id="usersearch">
    </div>
    <strong style="font-size:14px; color:#e50000;">*required field</strong>
    <br/><br/><button id="btnSearch" type="button" class="btn btn-primary btn-lg">Go!</button>
    <div id = "waitsign"><i class='fa fa-spinner fa-pulse fa-2x'></i> Please wait...</div>
	</form>
	<div style="font-size:10px; color:#e50000;" id = "formError"><span>&nbsp;</span></div>
	</div>
	</div>
	<div class = "row-fluid">
	<div style = "margin-top:1px; padding:10px;" class = "span10 offset1 centertxt darktxt">
	</div>
	</div>
	
	<!-- Result Rows Start Here -->
	<div class = "row-fluid">
	<div style = "margin-top:10px; padding:10px;" class = "eqspan span9 offset1 centertxt whitebg darktxt">
	<div class = "twttxt">
	<i class="qicon fa fa-quote-left fa-lg"></i>
	Dummy_Tweet_Text
	<i class="qicon fa fa-quote-right fa-lg"></i>
	<br/>
	Posted using <em>Source</em> at <em>Time</em>.
	</div>
	</div>
	<div style = "width: 8.55%; margin-left:0px; margin-top:10px; padding:10px;" class = "eqspan span1 centertxt whitebg darktxt">
	<div class = "classdisp">
	<i class="classpos fa fa-smile-o fa-4x"></i>
	</div>
	</div>
	</div>
	<div class = "row-fluid">
	<div style = "margin-top:0px; padding:10px;" class = "span10 offset1 centertxt whitebg darktxt">
	<div class = "usrtxt">
	<hr style="margin-top:5.0px; margin-bottom:5.0px;"/>
	<strong>By</strong> user_screen_name, <strong>Name:</strong> User_name, <strong>From:</strong> Location, <strong>Time Zone:</strong> Time_Zone<strong>.</strong><br/>
	User_Desc
	</div>
	</div>
	</div>
	
	<div class = "row-fluid">
	<div style = "margin-top:10px; padding:10px;" class = "eqspan span9 offset1 centertxt whitebg darktxt">
	<div class = "twttxt">
	<i class="qicon fa fa-quote-left fa-lg"></i>
	Dummy_Tweet_Text
	<i class="qicon fa fa-quote-right fa-lg"></i>
	<br/>
	Posted using <em>Source</em> at <em>Time</em>.
	</div>
	</div>
	<div style = "width: 8.55%; margin-left:0px; margin-top:10px; padding:10px;" class = "eqspan span1 centertxt whitebg darktxt">
	<div class = "classdisp">
	<i class="classneg fa fa-frown-o fa-4x"></i>
	</div>
	</div>
	</div>
	<div class = "row-fluid">
	<div style = "margin-top:0px; padding:10px;" class = "span10 offset1 centertxt whitebg darktxt">
	<div class = "usrtxt">
	<hr style="margin-top:5.0px; margin-bottom:5.0px;"/>
	<strong>By</strong> user_screen_name, <strong>Name:</strong> User_name, <strong>From:</strong> Location, <strong>Time Zone:</strong> Time_Zone<strong>.</strong><br/>
	User_Desc
	</div>
	</div>
	</div>
	
	<div class = "row-fluid">
	<div style = "margin-top:10px; padding:10px;" class = "eqspan span9 offset1 centertxt whitebg darktxt">
	<div class = "twttxt">
	<i class="qicon fa fa-quote-left fa-lg"></i>
	Dummy_Tweet_Text
	<i class="qicon fa fa-quote-right fa-lg"></i>
	<br/>
	Posted using <em>Source</em> at <em>Time</em>.
	</div>
	</div>
	<div style = "width: 8.55%; margin-left:0px; margin-top:10px; padding:10px;" class = "eqspan span1 centertxt whitebg darktxt">
	<div class = "classdisp">
	<i class="classneu fa fa-meh-o fa-4x"></i>
	</div>
	</div>
	</div>
	<div class = "row-fluid">
	<div style = "margin-top:0px; padding:10px;" class = "span10 offset1 centertxt whitebg darktxt">
	<div class = "usrtxt">
	<hr style="margin-top:5.0px; margin-bottom:5.0px;"/>
	<strong>By</strong> user_screen_name, <strong>Name:</strong> User_name, <strong>From:</strong> Location, <strong>Time Zone:</strong> Time_Zone<strong>.</strong><br/>
	User_Desc
	</div>
	</div>
	</div>
	
	<div class = "row-fluid">
	<div style = "margin-top:10px; padding:10px;" class = "eqspan span9 offset1 centertxt whitebg darktxt">
	<div class = "twttxt">
	<i class="qicon fa fa-quote-left fa-lg"></i>
	Dummy_Tweet_Text
	<i class="qicon fa fa-quote-right fa-lg"></i>
	<br/>
	Posted using <em>Source</em> at <em>Time</em>.
	</div>
	</div>
	<div style = "width: 8.55%; margin-left:0px; margin-top:10px; padding:10px;" class = "eqspan span1 centertxt whitebg darktxt">
	<div class = "classdisp">
	<i class="classunk fa fa-question-circle fa-4x"></i>
	</div>
	</div>
	</div>
	<div class = "row-fluid">
	<div style = "margin-top:0px; padding:10px;" class = "span10 offset1 centertxt whitebg darktxt">
	<div class = "usrtxt">
	<hr style="margin-top:5.0px; margin-bottom:5.0px;"/>
	<strong>By</strong> user_screen_name, <strong>Name:</strong> User_name, <strong>From:</strong> Location, <strong>Time Zone:</strong> Time_Zone<strong>.</strong><br/>
	User_Desc
	</div>
	</div>
	</div>
	
	<!-- FOOTER -->
	<!--  div class = "row-fluid">
		<div class = "span12">
			<div class="navbar navbar-fixed-bottom">
				<p class="navbar-text pull-right">&copy; 2014, Prerna Chikersal</p>
			</div>
		</div>
	</div-->
</div>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<script src="bootstrap/js/bootstrap.min.js"></script>
<script src="bootstrap/js/bootswatch.js"></script>
<script>
$(function() {
	   var maxHeight=0;
	   $('.eqspan').each(function(){
	      if($(this).height()>maxHeight) {
	       maxHeight=$(this).height();
	      }
	   });

	    $('.eqspan').height(maxHeight);
	    
	    var parentHeight = $('.vout').height();
	    var childHeight = $('.vin').height();
	    $('.vin').css('margin-top', (parentHeight - childHeight) / 2);
	});
</script>
<script>
function stripHTML(dirtyString) {
    var container = document.createElement('div');
    container.innerHTML = dirtyString;
    return container.textContent || container.innerText;
}
function validateForm(twtq, usrq) {
	  lentwtq = twtq.length;
	  lenusrq = usrq.length;
	  if(lentwtq<=0) {
		return 0;
	  }
	  if(lentwtq>140){
		  return -1;
	  }
	  if(lenusrq>140){
		  return -2;
	  }
	  return 1;
}
function getError(errornum){
	if(errornum==0) {
		return '"Search tweets" field is required.';
	}
	else if(errornum==-1){
		return 'Text entered must not exceed 140 characters.';
	}
	else if(errornum==-2){
		return 'Text entered must not exceed 140 characters.';
	}
	else{
		return ' ';
	}
}
function showWaitSign(){
	$("#btnSearch").hide();
	$("#waitsign").show();
}
function stopWaitSign(){
	$("#waitsign").hide();
	$("#btnSearch").show();
}
function crawlerRun(twtq, usrq){
	$.post('crawlhandler.jsp', {tweetsearch: twtq, usersearch: usrq});
	alert("posted to crawler");
}
/*function indexerRun(){
	
}
function getResultsAsRequest(){
	//Run Query code and get ArrayList or some Java Object with results
	//set request object with the query results
	//return request object
}*/
$(document).ready(function() {
	$("#waitsign").hide();
    $("#btnSearch").click(function(){
        var twtq = stripHTML($('#tweetsearch').val().trim());
        var usrq = stripHTML($('#usersearch').val().trim());
        valsuccess = validateForm(twtq, usrq);
        errortext = getError(valsuccess);
        $('#formError span').text(errortext);
        if (valsuccess==1){
        	showWaitSign();
        	crawlerRun(twtq, usrq);
        	//indexerRun();
        	//requestobj = getResultsAsRequest();
        	stopWaitSign();
        	//Post request object with form
        }
    }); 
});
</script>
</body>
</html>