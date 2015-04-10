<%@ page language="java" contentType="text/html; charset=US-ASCII"
    pageEncoding="US-ASCII" import="java.util.*"%>
<%
	/*boolean showResults = false;
	ArrayList<HashMap<String, String>> returneddocs = (ArrayList<HashMap<String, String>>) request.getAttribute("results");
	if (returneddocs == null || returneddocs.size()<=0){
		System.out.println("no results");
		showResults = false;
	}
	else{
		System.out.println("Results are back!");
		System.out.println(returneddocs.size());
		showResults = true;
		//session.setAttribute("resultsdisp",1); 
		//session.setAttribute("results",returneddocs); 
		//session.removeAttribute("resultsdisp"); 
		//session.removeAttribute("results"); 
		//response.sendRedirect("http://myexpressions.in/");
		//System.out.println("Did it redirect?");
		return;
	}*/
	%>
<!DOCTYPE html>
<html>
<head>
<!-- Bootstrap -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="bootstrap/css/bootstrap-spacelab.css" rel="stylesheet" media="screen">
    <link href="bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="css/select-css.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <link href='http://fonts.googleapis.com/css?family=Josefin+Sans' rel='stylesheet' type='text/css'>
	<!--[if IE 7]>
	  <link rel="stylesheet" href="path/to/font-awesome/css/font-awesome-ie7.min.css">
	<![endif]-->
	<style type ="text/css">
	body {padding-bottom:70px;background-color: #c0deed;}
	.stdp{ font-size: 15px;}
	.centertxt{text-align:center;}
	.righttxt{text-align: right;}
	.btxt{font-weight: bold;}
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
	.divpos{
		border-right: 20px solid #009933;
	}
	.divneg{
		border-right: 20px solid #e50000;
	}
	.divneu{
		border-right: 20px solid #1dcaff;
	}
	.divunk{
		border-right: 0px solid #ffffff;
	}
	#piekey{
		text-align: center;
	}

	.senti-legend {
    	/*background:#ffffff;*/
    	font-size: 15px;
    	text-align: center;
    	line-height: 30px;
    	margin:0 auto;
    	text-align:left;
    	width:100%;
    	margin-top: 40px;
	}
	.senti-legend ul {
		margin: 0;
    	vertical-align: middle;
    	/*line-height: 30px;*/
    }
	.senti-legend ul li {
  		list-style: none;
 		/*margin-bottom:10px;*/
	}
	.senti-legend ul.legend-labels li span {
  		display: inline-block;
  		height: 10px;
  		width: 40px;
  		border: 1px solid #999;
	}
	#pgmenudiv{
		margin:0 auto;
		text-align: left;
		margin-top:30px;
	}
	.pgselect{
		border: 1px solid #433e90;
    	border-radius: 5px;
		color: #433e90;
	}
	.pgopt {
	}
	#searchlbl{
		font-size:40px;
		font-weight: bold;
		font-family: 'Josefin Sans', sans-serif;
	}
	#tweetsearch {
		border: 0px none;
	}
	#btnSearch {
		margin-top:8px;
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
      <label for="Tweet"><span id = "searchlbl">Search Tweets<!--  strong style="color:#e50000;">*</strong-->:</span></label>
      <input type="text" placeholder="Enter Query (Required)" class="form-control" id="tweetsearch">
      <button id="btnSearch" type="button" class="btn btn-primary btn-lg">Go!</button>
    </div>
    <div class="form-group">
      <!--  label for="user"><strong style="font-size:16px;">Filter by user description:</strong></label-->
      <input type="hidden" placeholder="Optional Filter for User Description" class="form-control" id="usersearch">
    </div>
    <!--  strong style="font-size:14px; color:#e50000;">*required field</strong-->
    <!--  br/><br/><button id="btnSearch" type="button" class="btn btn-primary btn-lg">Go!</button> -->
    <div id = "waitsign"><i class='fa fa-spinner fa-pulse fa-2x'></i> Please wait...</div>
	</form>
	<div style="font-size:10px; color:#e50000;" id = "formError"><span>&nbsp;</span></div>
	</div>
	</div>
	<div class = "row-fluid">
	<div style = "margin-top:1px; padding:10px;" class = "span10 offset1 centertxt darktxt">
	</div>
	</div>
	
	<div class = "row-fluid">
	<div id = "numresultsdisp" class = "centertxt span9 offset1 btxt">
	</div>
	<div class = "centertxt span1 btxt">
	</div>
	</div>
	
	<div class = "row-fluid">
	<div id = "piediv1" class = "span2 offset1 centertxt">
	</div>
	<div id = "piediv2" class = "span2 centertxt">
	</div>
	<div id = "piekey" class = "span2">
	<div id = "pgmenudiv">
	</div>
	<div id = "piekeyin">
	</div>
	</div>
	<div id = "wordclouddiv" class = "span4 centertxt">
	</div>
	</div>
	
	
	
	<!-- Result Rows Start Here -->
	<div id = "resultsdiv">
	
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
<script src="chartsjs/ChartNew.js"></script>
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

function setDisplaySizes(){
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
}
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

function dispPieChart(canvasid, numpos, numneg, numneu){
	var ctx = document.getElementById(canvasid).getContext("2d");
	var newopts = {
			animation : true,
		    inGraphDataShow: true,
		    inGraphDataAnglePosition : 2,
		    inGraphDataRadiusPosition: 2,
		    inGraphDataRotate : "inRadiusAxisRotateLabels",
		    inGraphDataAlign : "center",
		    inGraphDataVAlign : "middle",
		    inGraphDataFontColor: 'black'
		    /*legend:true*/
		}
	var data = [
	            {
	                value: numpos,
	                color:"#009933"
	                //highlight: "#00CC33"
	                //title: "Positive"
	            },
	            {
	                value: numneg,
	                color: "#e50000"
	                //highlight: "#FF3300"
	                //title: "Negative"
	            },
	            {
	                value: numneu,
	                color: "#1dcaff"
	                //highlight: "#33FFFF"
	                //title: "Neutral/Mixed
	            }
	        ];
	var sentiPie = new Chart(ctx).Pie(data, newopts);
}

function displayResultsInDivs(resultjson, numresults, pg, top10counts){
	
	var countpos = 0;
	var countneg = 0;
	var countneu = 0;
	var countunk = 0;
	
	var b4_tweet_raw_pos = "<div class = \"row-fluid\"><div style = \"margin-top:10px; padding:10px;\" class = \"divpos eqspan span10 offset1 centertxt whitebg darktxt\"><div class = \"twttxt\"><i class=\"qicon fa fa-quote-left fa-lg\"></i>";
	var b4_tweet_raw_neg = "<div class = \"row-fluid\"><div style = \"margin-top:10px; padding:10px;\" class = \"divneg eqspan span10 offset1 centertxt whitebg darktxt\"><div class = \"twttxt\"><i class=\"qicon fa fa-quote-left fa-lg\"></i>";
	var b4_tweet_raw_neu = "<div class = \"row-fluid\"><div style = \"margin-top:10px; padding:10px;\" class = \"divneu eqspan span10 offset1 centertxt whitebg darktxt\"><div class = \"twttxt\"><i class=\"qicon fa fa-quote-left fa-lg\"></i>";
	var b4_tweet_raw_unk = "<div class = \"row-fluid\"><div style = \"margin-top:10px; padding:10px;\" class = \"divunk eqspan span10 offset1 centertxt whitebg darktxt\"><div class = \"twttxt\"><i class=\"qicon fa fa-quote-left fa-lg\"></i>";

	var b4_src_time = "<i class=\"qicon fa fa-quote-right fa-lg\"></i><br/>";
	var end_tweet_raw = "</div></div>";
	var b4_pol_disp = "<div style = \"width: 8.55\%; margin-left:0px; margin-top:10px; padding:10px;\" class = \"eqspan span1 centertxt whitebg darktxt\"><div class = \"classdisp\">";
	var class_pos = "<i class=\"classpos fa fa-smile-o fa-4x\"></i>";
	var class_neg = "<i class=\"classneg fa fa-frown-o fa-4x\"></i>";
	var class_neu = "<i class=\"classneu fa fa-meh-o fa-4x\"></i>";
	var class_unk = "<i class=\"classunk fa fa-question-circle fa-4x\"></i>";
	var after_pol_disp = "</div></div></div>";
	var b4_usr_info = "<div class = \"row-fluid\"><div style = \"margin-top:0px; padding:10px;\" class = \"span10 offset1 centertxt whitebg darktxt\"><div class = \"usrtxt\"><hr style=\"margin-top:5.0px; margin-bottom:5.0px;\"/>";
	var after_usr_info = "</div></div></div>";
	var getnumresults = numresults;
	var maxnumresults = 50;
	if (numresults>maxnumresults){
		getnumresults = maxnumresults;
	}
	// page number calculation
	var pgoffset = pg-1;
	var pgstart = pgoffset*50+1;
	var pgend = pgstart+49;
	if (pgend>numresults){
		pgend = numresults;
	}
	var divnumdisp = document.getElementById('numresultsdisp');
	divnumdisp.innerHTML = "Showing results "+pgstart+" to "+pgend+" of "+numresults;
	var div = document.getElementById('resultsdiv');
	div.innerHTML = "";
	for (i = pgstart; i < pgend; i++) { 	
		var extrastuff = "";
		var pollbl = resultjson[i].autopolarity_lbl;
		var polscore = resultjson[i].autopolarity_score;
		if (polscore>-0.5 && polscore<0.5){
			pollbl="neutral";
		}
		if (pollbl=="positive"){
			b4_tweet_raw = b4_tweet_raw_pos;
			countpos = countpos+1;
		}
		else if(pollbl=="negative"){
			b4_tweet_raw = b4_tweet_raw_neg;
			countneg = countneg+1;
		}
		else if(pollbl=="neutral"){
			b4_tweet_raw = b4_tweet_raw_neu;
			countneu = countneu+1;
		}
		else{
			b4_tweet_raw = b4_tweet_raw_unk;
			countunk = countunk+1;
		}
		extrastuff = extrastuff+b4_tweet_raw;
		extrastuff = extrastuff+resultjson[i].tweet_raw;
		extrastuff = extrastuff+b4_src_time;
		
		extrastuff = extrastuff+"Posted using <em>"+resultjson[i].source+"</em> at <em>"+resultjson[i].created_at+"</em>";
		extrastuff = extrastuff+end_tweet_raw;
		extrastuff = extrastuff+b4_usr_info;
		extrastuff = extrastuff+"<strong>By</strong> "+resultjson[i].user_screen_name+", <strong>Name:</strong> "+resultjson[i].user_name+", <strong>From:</strong> "+resultjson[i].user_location+", <strong>Time Zone:</strong> "+resultjson[i].user_time_zone+"<strong>.</strong><br/>";
		extrastuff = extrastuff+resultjson[i].user_desc_raw;
		extrastuff = extrastuff+after_usr_info;
		div.innerHTML = div.innerHTML+extrastuff;
	}
	setDisplaySizes();
	var lbl1 = "For Top 10 Results:<br/>";
	var lbl2 = "For Current Page Results:<br/>";
	document.getElementById('piediv1').innerHTML = lbl1 + "<canvas id=\"senticharttop10\" width=\"200\" height=\"200\"></canvas>";
	document.getElementById('piediv2').innerHTML = lbl2 + "<canvas id=\"sentichart\" width=\"200\" height=\"200\"></canvas>";
	dispPieChart("sentichart", countpos, countneg, countneu);
	dispPieChart("senticharttop10", top10counts[0], top10counts[1], top10counts[2]);
	
	var keyhtml = "<div class='senti-legend'><ul class='legend-labels'><li style = \"color:#666666;\"><span style='background:#009933;'></span> Positive</li><li style = \"color:#666666;\"><span style='background:#e50000;'></span> Negative</li><li style = \"color:#666666;\"><span style='background:#1dcaff;'></span> Neutral/Mixed</li></ul></div>";
	document.getElementById('piekeyin').innerHTML = keyhtml;
	
	$("#pgselectid").val(pg.toString());
	//var element = document.getElementById('pgselectid');
	//alert(element.value);
    //element.value = pg.toString();
}

function countTop10(resultjson, strlen){
	var end = 10;
	if (strlen<end){
		end = strlen;
	}
	var countpos=0;
	var countneg=0;
	var countneu=0;
	var countunk=0;
	for (i = 0; i < end; i++) {
		var pollbl = resultjson[i].autopolarity_lbl;
		var polscore = resultjson[i].autopolarity_score;
		if (polscore>-0.5 && polscore<0.5){
			pollbl="neutral";
		}
		if (pollbl=="positive"){
			countpos = countpos+1;
		}
		else if(pollbl=="negative"){
			countneg = countneg+1;
		}
		else if(pollbl=="neutral"){
			countneu = countneu+1;
		}
		else{
			countunk = countunk+1;
		}
		
	}
	return [countpos, countneg, countneu, countunk];
}
$(document.body).on('change','#pgselectid',function(){
	//alert("changed");
    var newval = parseInt($(this).val());
    var results = window.myResults;
    var resultslen = window.myResultsLen;
    var top10counts = window.top10counts;
    displayResultsInDivs(results, resultslen, newval, top10counts);
});

function dispPageNums(resultslen){
	var numpgs = Math.ceil(resultslen/50);
	var div = document.getElementById('pgmenudiv');
	var disptxtstart = "View: <select id = \"pgselectid\" class = \"pgselect\">";
	var disptxtend = "</select>";
	var dispopt = ""
	
	for (i=0; i<numpgs; i++){
		dispopt=dispopt+"<option class=\"pgopt\" value = \""+(i+1)+"\">Page "+(i+1)+"</option>";
	}
	div.innerHTML = disptxtstart+dispopt+disptxtend;
}

function crawlerRun(twtq, usrq){
	/*$.post('crawlhandler.jsp', {tweetsearch: twtq, usersearch: usrq}, function(data, textStatus) {
		//data contains the JSON object
		//textStatus contains the status: success, error, etc
		alert("got resp!")
		//alert(data[0].tweet_raw);
	}, "json");*/
	var datatosend = {tweetsearch: twtq, usersearch: usrq}
	$.ajax({
	    datatype : "json",
	    method: "post",
	    url: "crawlhandler.jsp",
	    data : datatosend,
	    success : function(result) {
	        //alert("result called!"); // result is an object which is created from the returned JSON
	    	var strlen = result.length;
	    	//alert(strlen);
	    	var top10counts = countTop10(result, strlen);
	    	displayResultsInDivs(result, strlen, 1, top10counts);
	    	window.myResults = result;
	    	window.myResultsLen = strlen;
	    	window.top10counts = top10counts
	    	dispPageNums(strlen);
	    	stopWaitSign();
	    },
	});
}

$(document).ready(function() {
	$("#waitsign").hide();
	//Chart.defaults.global.responsive = true;
	//Chart.defaults.global.maintainAspectRatio = true;
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
        	//stopWaitSign();
        	//Post request object with form
        }
    }); 
});
</script>
</body>
</html>