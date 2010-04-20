<?xml version="1.0" encoding="UTF-8"?>
<x:stylesheet xmlns:x="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<x:output method="html" version="4.01" encoding="UTF-8"
		doctype-public="-//W3C//DTD HTML 4.01//EN"
		doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>
 
	<x:template match="/">
		<html>
		<head>
			<title>New template</title>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
			<!-- export css and js to config.xml -->
			<link rel="stylesheet" type="text/css" href="http://e.fstatic.eu/css/yui-rf.css"/>
			<link href="http://e.fstatic.eu/css/grids.css" rel="stylesheet" type="text/css"/>
			<link href="http://e.fstatic.eu/css/style.css" rel="stylesheet" type="text/css"/>
			<link href="http://oyc.fstatic.eu/css/style2.css" rel="stylesheet" type="text/css"/>
			<link href="http://e.fstatic.eu/css/article.css" rel="stylesheet" type="text/css"/>
			<script src="http://yui.yahooapis.com/3.0.0/build/yui/yui-min.js" type="text/javascript"/>
			<style>html,body{background:#464646;}</style>
		</head>
		<body>
			<div class="container w974 header">
				<div class="widget template" id="logo">
					<h1>AsynCode Market</h1>
				</div>
			</div>
			<div class="w974 body">
				<x:if test="//*[@view='default']">
					<x:call-template name="defaultlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='product']">
					<x:call-template name="productlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='producent']">
					<x:call-template name="producentlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='userquestion']">
					<x:call-template name="userquestionlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='add_usercomment']">
					<x:call-template name="usercommentlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='usernote']">
					<x:call-template name="usernotelayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='productstatus']">
					<x:call-template name="setproductstatuslayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='developeranswer']">
					<x:call-template name="developeranswerlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='developerchangelog']">
					<x:call-template name="developerchangeloglayout">
						
					</x:call-template>
				</x:if>
			</div>
			<div class="container w974 footer">
				<div class="widget template" id="copyright">Adrian Kalbarczyk all rigths reserved</div>
			</div>
		</body>
		</html>
	</x:template>
	
	<x:template name="defaultlayout">
		<p><b>Product list:</b></p>
		<x:for-each select="//*[@name='productlist']/object">
			<p><a href="http://localhost:9999/producent/{producentid}"><x:value-of select="producentname"/></a>:&#160;<a href="http://localhost:9999/product/{productid}"><x:value-of select="name"/></a></p>
		</x:for-each>	
		<p><b>Developers info:</b></p>
		<x:for-each select="//*[@name='developers_info']/object">
			<!--<p><x:value-of select="id"/></p>-->
			<p><x:value-of select="content"/></p>
		</x:for-each>	
		
	</x:template>
	<x:template name="productlayout">
		<x:for-each select="//*[@name='product']">
			<p><b>Product name:&#160;</b><x:value-of select="name"/></p>
		</x:for-each>	
			
		<x:for-each select="//*[@name='product_producent']">
			<p><b>Producent: &#160;</b><x:value-of select="producentname"/></p>
			<p><b>Producent card: &#160;</b><a href="http://{card}"><x:value-of select="card"/></a></p>
			<p><b>Producent page: &#160;</b><a href="http://{link}"><x:value-of select="link"/></a></p>
		</x:for-each>
		
		<x:for-each select="//*[@name='product']">
			<p><b>Application demo: &#160;</b><a href="#"><x:value-of select="demo"/></a></p>
			<p><b>Buy or Download: &#160;</b><a href="#"><x:value-of select="buydownload"/></a></p>
			<p><b>Downloads: &#160;</b><x:value-of select="downloadstats"/></p>
			<p><b>Clicks: &#160;</b><x:value-of select="clickstats"/></p>
			<p><b>Note: &#160;</b><x:value-of select="note"/></p>
			<p><b>Docs tag:&#160;</b><x:value-of select="docstag"/></p>
			<p><b>Licence: &#160;</b><x:value-of select="licence"/></p>
			<p><b>Screenshots: &#160;</b><x:value-of select="screenshot"/></p>
			<!--<p><x:value-of select="producent"/></p>-->
		</x:for-each>
		
		<p><b>Information:</b></p>
		<x:for-each select="//*[@name='information']">
			<!--<p><x:value-of select="id"/></p>-->
			<p><x:value-of select="lang"/></p>
			<p><x:value-of select="info"/></p>
		</x:for-each>
		
		<p><b>Changelog:</b></p>
		<x:for-each select="//*[@name='changelog']">
			<!--<p><x:value-of select="id"/></p>-->
			<p><x:value-of select="content"/></p>
		</x:for-each>
		
		<!--<p><b>Tagi: &#160;</b>games, blood</p>-->
		
		<p><b>TODO:</b></p>
		<x:for-each select="//*[@name='todo']/object">
			<!--<p><x:value-of select="id"/></p>-->
			<p><x:value-of select="content"/></p>
		</x:for-each>
		
		<p><b>QUESTIONS AND ANSWERS:</b></p>
		<x:for-each select="//*[@name='qa']/object">
			<!--<p><x:value-of select="id"/></p>-->
			<p><b>Q: &#160;</b><x:value-of select="question"/></p>
			<p><b>A: &#160;</b><x:value-of select="answer"/></p>
		</x:for-each>
		
		<!--<p><b>Comments:</b></p>-->
		<!--<x:for-each select="//*[@name='comments']">-->
		<!--	<p><x:value-of select="id"/></p>-->
		<!--	<p><x:value-of select="content"/></p>-->
		<!--</x:for-each>-->
		
		<b>USER</b>
		<x:for-each select="//*[@name='product']">
		<p><a href="http://localhost:9999/userquestion/{id}">Make a question</a></p>
		<form action="http://localhost:9999/add_userquestion" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="question" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>	
		<p><a href="http://localhost:9999/usercomment">Add comment</a></p>
		<form action="" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="comment" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
		<p><a href="http://localhost:9999/usernote">Add note</a></p>
		<form action="add_usernote" method="post" enctype="multipart/form-data">
			<input type="text" id="abstract" name="note" accesskey="x"></input>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
		</x:for-each>
		
		<b>DEVELOPER</b>
		<p><a href="http://localhost:9999/productstatus">Set product status</a></p>
		<form action="set_productstatus" method="post" enctype="multipart/form-data">
			<input type="radio" name="status" value="hidden" checked="checked"/> hidden<br />
			<input type="radio" name="status" value="test" /> test<br />
			<input type="radio" name="status" value="beta" /> beta<br />
			<input type="radio" name="status" value="avaible" /> avaible<br />
			<input value="Send" type="submit" accesskey="s"/>
		</form>
		<p><a href="http://localhost:9999/developeranswer">Add developer answer</a></p>
		<form action="add_developeranswer" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="answer" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
		<p><a href="http://localhost:9999/developerchangelog">Add changes changelog</a></p>
		<form action="add_developerchangelog" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="changelog" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
	</x:template>
	
	<x:template name="producentlayout">
		<!--<x:for-each select="//*[@name='product']">-->
		<!--	<p><x:value-of select="id"/></p>-->
		<!--	<p><x:value-of select="name"/></p>-->
		<!--	<p><x:value-of select="demo"/></p>-->
		<!--	<p><x:value-of select="buydownload"/></p>-->
		<!--	<p><x:value-of select="downloadstats"/></p>-->
		<!--	<p><x:value-of select="clickstats"/></p>-->
		<!--	<p><x:value-of select="note"/></p>-->
		<!--	<p><x:value-of select="docstag"/></p>-->
		<!--	<p><x:value-of select="licence"/></p>-->
		<!--	<p><x:value-of select="screenshot"/></p>-->
		<!--	<p><x:value-of select="producent"/></p>-->
		<!--	<p><x:value-of select="licence"/></p>-->
		<!--</x:for-each>-->
		
		<x:for-each select="//*[@name='producent']">
			<p><b>Producent name: &#160;</b><x:value-of select="name"/></p>
			<p><b>Producent homepage: &#160;</b><x:value-of select="link"/></p>
			<!--<p><x:value-of select="card"/></p>-->
			<!--<p><x:value-of select="info"/></p>-->
		</x:for-each>
		
		<!--<x:for-each select="//*[@name='comments']">-->
		<!--	<p><x:value-of select="id"/></p>-->
		<!--	<p><x:value-of select="content"/></p>-->
		<!--</x:for-each>-->
		<p><b>Products:</b></p>
		<x:for-each select="//*[@name='producent_product']|//*[@name='producent_product']/object">
			<p><x:value-of select="name"/></p>
			<!--<p><x:value-of select="producentname"/></p>-->
		</x:for-each>
		<p><b>Info:</b></p>
		<x:for-each select="//*[@name='producent_info']">
			<!--<p><x:value-of select="id"/></p>-->
			<!--<p><x:value-of select="name"/></p>-->
			<!--<p><x:value-of select="card"/></p>-->
			<!--<p><x:value-of select="link"/></p>-->
			<p><x:value-of select="info"/></p>
		</x:for-each>	
	</x:template>
	<x:template name="userquestionlayout">
		<b>User question</b>
		<form action="http://localhost:9999/add_userquestion" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="question" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>	
	</x:template>
	<x:template name="usercommentlayout">
		<b>User comment</b>
		<form action="" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="comment" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
	</x:template>   
	<x:template name="usernotelayout">
		<b>User note</b>
		<form action="add_usernote" method="post" enctype="multipart/form-data">
			<input type="text" id="abstract" name="note" accesskey="x"></input>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
	</x:template>
	<x:template name="setproductstatuslayout">
		<b>Set productstatus</b>
		<form action="set_productstatus" method="post" enctype="multipart/form-data">
			<input type="radio" name="status" value="hidden" checked="checked"/> hidden<br />
			<input type="radio" name="status" value="test" /> test<br />
			<input type="radio" name="status" value="beta" /> beta<br />
			<input type="radio" name="status" value="avaible" /> avaible<br />
			<input value="Send" type="submit" accesskey="s"/>
		</form>
	</x:template>
	<x:template name="developeranswerlayout">
		<b>Developer answer</b>
		<form action="add_developeranswer" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="answer" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
	</x:template>
	<x:template name="developerchangeloglayout">
		<b>Developer changelog</b>
		<form action="add_developerchangelog" method="post" enctype="multipart/form-data">
			<textarea id="abstract" name="changelog" accesskey="x"></textarea><br/>
			<input value="Send" type="submit" accesskey="s"/>
		</form>
	</x:template>
</x:stylesheet>
