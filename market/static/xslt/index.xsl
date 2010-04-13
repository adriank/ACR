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
			<link href="http://e.fstatic.eu/css/style2.css" rel="stylesheet" type="text/css"/>
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
				<x:call-template name="layout">
					
				</x:call-template>
			</div>
			<div class="container w974 footer">
				<div class="widget template" id="copyright">Adrian Kalbarczyk all rigths reserved</div>
			</div>
		</body>
		</html>
	</x:template>
	
	<x:template name="layout">
		<!--<x:for-each select="/list/object">-->
		<!--	<x:if test="@name='product' ">	-->
		<!--		<p><x:value-of select="id"/></p>-->
		<!--		<p><x:value-of select="name"/></p>-->
		<!--		<p><x:value-of select="demo"/></p>-->
		<!--		<p><x:value-of select="buydownload"/></p>-->
		<!--		<p><x:value-of select="downloadstats"/></p>-->
		<!--		<p><x:value-of select="clickstats"/></p>-->
		<!--		<p><x:value-of select="note"/></p>-->
		<!--		<p><x:value-of select="docstag"/></p>-->
		<!--		<p><x:value-of select="lecence"/></p>-->
		<!--		<p><x:value-of select="screenshot"/></p>-->
		<!--		<p><x:value-of select="producent"/></p>-->
		<!--	</x:if>-->
		<!--	<x:if test="@name='changelog' ">-->
		<!--		<p><x:value-of select="id"/></p>-->
		<!--		<p><x:value-of select="content"/></p>-->
		<!--	</x:if>	-->
		<!--</x:for-each>-->
		<p><b>Information:</b></p>
		<x:for-each select="//*[@name='information']">
		<p><x:value-of select="id"/></p>
		<p><x:value-of select="lang"/></p>
		<p><x:value-of select="info"/></p>
		</x:for-each>
		
		<p><b>Changelog:</b></p>
		<x:for-each select="//*[@name='changelog']">
			<p><x:value-of select="id"/></p>
			<p><x:value-of select="content"/></p>
		</x:for-each>
		
		<p><b>Product:</b></p>
		<x:for-each select="//*[@name='product']">
			<p><x:value-of select="id"/></p>
			<p><x:value-of select="name"/></p>
			<p><x:value-of select="demo"/></p>
			<p><x:value-of select="buydownload"/></p>
			<p><x:value-of select="downloadstats"/></p>
			<p><x:value-of select="clickstats"/></p>
			<p><x:value-of select="note"/></p>
			<p><x:value-of select="docstag"/></p>
			<p><x:value-of select="lecence"/></p>
			<p><x:value-of select="screenshot"/></p>
			<p><x:value-of select="producent"/></p>
		</x:for-each>
		
		<p><b>QA:</b></p>
		<x:for-each select="//*[@name='qa']/object">
			<p><x:value-of select="id"/></p>
			<p><x:value-of select="question"/></p>
			<p><x:value-of select="answer"/></p>
			<p><x:value-of select="user"/></p>
			<p><x:value-of select="author"/></p>
		</x:for-each>
		
		<p><b>Producent:</b></p>
		<x:for-each select="//*[@name='producent']">
			<p><x:value-of select="id"/></p>
			<p><x:value-of select="name"/></p>
			<p><x:value-of select="card"/></p>
			<p><x:value-of select="link"/></p>
			<p><x:value-of select="info"/></p>
		</x:for-each>
		
		<p><b>Comments:</b></p>
		<x:for-each select="//*[@name='comments']">
			<p><x:value-of select="id"/></p>
			<p><x:value-of select="content"/></p>
		</x:for-each>
		
		<p><b>TODO:</b></p>
		<x:for-each select="//*[@name='todo']/object">
			<p><x:value-of select="id"/></p>
			<p><x:value-of select="content"/></p>
		</x:for-each>		
	</x:template>
</x:stylesheet>
