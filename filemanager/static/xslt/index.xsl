<?xml version="1.0" encoding="UTF-8"?>
<x:stylesheet xmlns:x="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<x:output method="html" version="4.01" encoding="UTF-8"
		doctype-public="-//W3C//DTD HTML 4.01//EN"
		doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>
 
	<x:template match="/">
		<html>
		<head>
			<title>AsynCode Blog</title>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
			<!-- export css and js to config.xml -->
			<link rel="stylesheet" type="text/css" href="http://e.fstatic.eu/css/yui-rf.css"/>
			<link href="http://e.fstatic.eu/css/grids.css" rel="stylesheet" type="text/css"/>
			<link href="http://e.fstatic.eu/css/style.css" rel="stylesheet" type="text/css"/>
			<link href="http://oyc.fstatic.eu/css/style2.css" rel="stylesheet" type="text/css"/>
			<link href="http://e.fstatic.eu/css/article.css" rel="stylesheet" type="text/css"/>
			<!--<link href="http://localhost:9999/css/style.css" rel="stylesheet" type="text/css"/>-->
			<script src="http://yui.yahooapis.com/3.1.1/build/yui/yui-min.js" charset="utf-8" type="text/javascript"/>
			<style>
				html{background:#00598a;}
				<!--body{background: -moz-linear-gradient(top, #e1e8f6, #00598a);filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#e1e8f6', endColorstr='#00598a');}-->
				body{background: #00598a;}
				body{margin-top:0}
				.options{float:right;display:none;}
				.header{background:#0e1e3b; width:100%; height:56px;}
				.hd{width:974px; margin:0 auto;}
				.hd ul{margin:0;}
				#logo img{
					margin-top:24px;
				}
				.serviceName{
					width:974px;
					margin:auto;
					color:#4089be;
					font-size:40px;
					font-weight:bold;
					margin-top:16px;
					margin-bottom:8px;
				}
				#menu li.item a, #menu li.currentItem span {
					color:#003399;
					display:block;
					font-size:16px;
					font-weight:bold;
					line-height:32px;
					padding:0 16px;
				}
				#menu li:hover, #menu li:hover a, #menu
				li.currentItem, #menu li.currentItem span{
					background-color:#AACCFF;
					color:#333333;
					cursor: pointer;
					text-align:center;
					text-decoration:none;
				}
				.footer{
					font-family:Arial;
					-webkit-border-radius:3px;
					-moz-border-radius:3px;
					background:#000033;
					border-top: 1px solid #656565;
					padding:8px 0;
					text-align: center;
					color:#ddd;
				}
				.footer{text-align:left; padding: 0;background:#00003;font-size:10px;}
				.footer p{margin-left:120px; margin-right:10px;}
				.footer img{
					<!--width: 220px;-->
					float: left;
					<!--margin: 10px;-->
					<!--background: #CBF622 url(images/bg_bottom.gif) center bottom no-repeat;-->
					<!--padding-bottom: 75px;-->
					margin-left:14px;margin-top:8px;
				}
				.sidebar {
					width: 60px;
					float: left;
					margin: 10px;
					background: #CBF622 url(images/bg_bottom.gif) center bottom no-repeat;
					padding-bottom: 5px;
				}
				.post .abstract{margin-left:16px;margin-right:96px;text-align:justify;}
				.post:hover{ color:#00598a;background:#e6e6e6;-webkit-border-radius:5px;-moz-border-radius:5px;}
				.post:hover .options{display:block; margin-top:-50px;margin-right:7px;}
				textarea{height:150px;}
				.commentauthor{font-weight:bold;color:green;float:left;}
				.comenttitle{font-weight:bold;color:blue;float:left;}
				.date{float:right;}
				#postOverlay {left:0px;top:0;}
				#postOverlay {display:none;position: fixed;width: 100%;height: 100%;background-color: #000;opacity: 0.5;filter: alpha(opacity=50);z-index: 104;}
				#fbOverlay { display: none;z-index:204 }
				.yui-widget #fbOverlay {display: block;  background: rgba(0, 0, 0, 0.5);border-radius: 6px;-moz-border-radius: 6px;-webkit-border-radius: 6px;padding: 10px;}
				#fbOverlay .yui-widget-hd {border: #3B5998 1px solid;background: #6D84B4;color: #fff;padding: 0 10px;cursor: move;}
				#fbOverlay .yui-widget-hd {border: #3B5998 1px solid;background: #6D84B4;color: #fff;padding: 0 10px;cursor: move;}
				#fbOverlay .yui-widget-bd {background: #fff;border: #555 1px solid;border-top: none;border-bottom : none;padding: 0 10px;}
				#fbOverlay .yui-widget-ft {border: #555 1px solid;border-top: none;background: #f2f2f2;}
				#fbOverlay .yui-widget-ft > div {border-top: #ccc 1px solid;padding: 5px 10px;text-align: right;}
				#fbOverlay textarea{width:300px;height:50px;}
				#fbOverlay .widget{margin-bottom:0;}
				
				<!--.magazineView h1, .magazineView h2, .magazineView h3,.magazineView h4-->
				#articles h1{
					margin-top:0;
				}
				#articles h3{
				border-bottom:6px solid #cccccc;
				color:#333333;
				font-weight:bold;
				line-height:16px;
				margin-bottom:20px;
				margin-top:16px;
				padding-bottom:6px;
				text-align:left;
				text-transform:uppercase;
				width:50%;
				}
				#articles .post:hover h3{
					border-bottom:6px solid #e6e6e6;
					color:#00598a;
				}
				.readMore{
				margin-left:782px;
				color:#b7415a;
				}
				.edit{
					background:url('http://localhost:9999/img/edit1.png');
					width:25px;
					height:25px;float:right;
					margin-right:5px;
				}
				.edit:hover{
					background:url('http://localhost:9999/img/edit2.png');
					width:25px;
					height:25px;
				}
				.delete{
					background:url('http://localhost:9999/img/delete1.png');
					width:25px;
					height:25px;float:right;
				}
				.delete:hover{
					background:url('http://localhost:9999/img/delete2.png');
					width:25px;
					height:25px;
				}
				
				p.intro  {
				color:#006699;
				font-size:15px;
				font-weight:bold;
				line-height:18px;
				margin-bottom:16px;
				text-align:justify;
				}
				#rightMenu{
					float:right;margin-right:0px;margin-top:-56px;
				}
				#rightMenu .login{
					background:url('http://localhost:9999/img/login2.png');
					width:41px;
					height:41px;
					float:left;
				}
				#rightMenu .login:hover{
					background:url('http://localhost:9999/img/login1.png');
				}
				#rightMenu .register{
					background:url('http://localhost:9999/img/custombig2.png');
					width:41px;
					height:41px;
					float:left;
					margin-left:6px;
				}
				#rightMenu .register:hover{
					background:url('http://localhost:9999/img/custombig1.png');
					
				}
				#rightMenu .add{
					background:url('http://localhost:9999/img/addbig2.png');
					width:41px;
					height:41px;
					float:left;
					margin-left:6px;
				}
				#rightMenu .add:hover{
					background:url('http://localhost:9999/img/addbig1.png');
				}
				form label {
					width:128px;
				}
			</style>
		</head>
		<body>
			<div class="container w974 header">
				<div class="hd">
				<div class="widget template" id="logo">
					<!--<h1>AsynCode Blog</h1>-->
					<a href="http://localhost:9999/"><img src="http://localhost:9999/img/logo_wyciagniete.png"/></a>
				</div>
				<!--<div id="menu">-->
					<!--<ul>-->
						<!--<li class="item"><a href="http://localhost:9999/admin-panel_add_post">Add post</a></li>-->
						<!--<li class="item"><a href="http://localhost:9999/">Blog</a></li>-->
					<!--</ul>-->
				<!--</div>-->
				</div>	
			</div>
			<div class="serviceName">FILES</div>
			<div class="w974 body">
					
				<x:if test="//*[@view='default']">
					<x:call-template name="defaultlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='list']">
					<x:call-template name="listlayout">
						
					</x:call-template>
				</x:if>
				<x:if test="//*[@view='delete']">
					<x:call-template name="deletelayout">
						
					</x:call-template>
				</x:if>
				
			</div>
			<div class="container w974 footer">
				<!--<div class="widget template" id="copyright">Adrian Kalbarczyk all rigths reserved</div>-->
				<img src="http://localhost:9999/img/blog-logosmall.png"/>
				<p>
					nec nisi diam, ornare et tincidunt ac, rutrum id lacus. Nullam cursus risus at
					turpis rhoncus bibendum. Nulla adipiscing velit sit amet purus vulputate ut
					suscipit magna reet. Nulla facilisi pretium ac justo, nec nisi diam, ornare et tincidunt ac, returum id lacus.
					Nullam cursus risus at turpis rhoncus bibendum. Nulla adipiscing velit sit amet purus vulputate ut suscipit magna
				</p>
			</div>
		</body>
		</html>
	</x:template>
	<x:template name="defaultlayout">
		
		<div class="widget list" id="articles">
			<h1>Zarządzanie plikami</h1>
			<form action="http://localhost:9999/list" method="post" enctype="multipart/form-data">
				<label>Lista plików</label>
				<input type="submit" name="list" value="List" accesskey="l"></input><br/><br/>
			</form>
			<form action="http://localhost:9999/delete" method="post" enctype="multipart/form-data">
				<label>Usuń plik</label>
				<input type="submit" name="delete" value="Delete" accesskey="r"></input><br/><br/>
			</form>
			<form action="http://localhost:9999/upload" method="post" enctype="multipart/form-data">
				<label>Wrzuć plik</label>
				<input type="file" name="upload" value="Upload" accesskey="u"></input><br/><br/>
			</form>
		</div>
	</x:template>
	<x:template name="listlayout">
		Lista
		<x:for-each select="//*[@name='list']|//*[@name='list']/object">
			<div class="post">
				<div><x:value-of select="@name"/></div>
			</div>
		</x:for-each>
	</x:template>
	<x:template name="deletelayout">
		Delete
	</x:template>
</x:stylesheet>
