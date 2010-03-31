<?xml version="1.0" encoding="UTF-8"?>
<x:stylesheet xmlns:x="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<x:output method="html" version="4.01" encoding="UTF-8"
		doctype-public="-//W3C//DTD HTML 4.01//EN"
		doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>
<!-- TODO some of these variables should be merged with others -->
	<x:variable name="doc" select="/list"/>
	<x:variable name="lang" select="//object[@name='lang']/@current"/>
	<!--<x:variable name="lang">pl</x:variable>-->
<!-- TODO create generator which sets domain -->
<!-- IE don't understand relative paths so domain MUST be predefined -->
	<x:variable name="configdoc" select="document('http://asyncode.com:9999/xml/config.xml')/config"/>
	<x:variable name="domain" select="$configdoc/domain/node()"/>
	<x:variable name="langdoc" select="document(concat($domain,'xml/texts_',$lang,'.xml'))/t"/>
	<x:variable name="static" select="$configdoc/staticdomain/node()"/>
	<x:variable name="role" select="/document/user/@role"/>
	<!--<x:variable name="f"><x:value-of select="$domain"/>layouts/<x:value-of select="/document/view/@name"/>.xml</x:variable>-->
	<x:variable name="layoutdoc" select="//object[@name='layout']"/>
	<!--<x:variable name="layoutdoc" select="document($layoutfile)/layout"/>-->
	<x:include href="widgets.xsl"/>

	<x:template match="/">
		<html>
		<head>
			<!-- TODO make it template -->
			<x:variable name="title">
				<x:if test="$layoutdoc//pagetitle/@langelement">
					<x:value-of select="$langdoc//*[local-name()=$layoutdoc/pagetitle/@langelement]"/>
				</x:if>
				<x:if test="$layoutdoc//pagetitle/@datasource">
					<x:value-of select="(//@*|//*)[local-name()=$layoutdoc/pagetitle/@datasource]"/>
				</x:if>
				<x:value-of select="$layoutdoc/pagetitle/node()"/>
			</x:variable>
			<title><x:value-of select="$title"/> - <x:value-of select="$configdoc/name/node()"/></title>
			<meta name="description" content="{$configdoc/description/node()}"/>
			<meta name="keywords" content="{$configdoc/keywords/node()}"/>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
			<!-- export css and js to config.xml -->
			<link rel="stylesheet" type="text/css" href="http://e.fstatic.eu/css/yui-rf.css"/>
			<link href="http://e.fstatic.eu/css/grids.css" rel="stylesheet" type="text/css"/>
			<link href="http://e.fstatic.eu/css/style.css" rel="stylesheet" type="text/css"/>
			<link href="{$static}css/style2.css" rel="stylesheet" type="text/css"/>
			<link href="http://e.fstatic.eu/css/article.css" rel="stylesheet" type="text/css"/>
			<style>html,body{background:<x:value-of select="$configdoc/backgroundcolor"/>;}</style>
			<!--<x:if test="count(//document/text)">-->
			<!--	<x:if test="count(//document/text//@lang)">-->
			<!--		<link type="text/css" rel="stylesheet" href="http://e.fstatic.eu/sh2/sh_style.min.css"/>-->
			<!--		<script type="text/javascript" src="http://e.fstatic.eu/sh2/sh_main.min.js"></script>-->
			<!--		<x:for-each select="//source/@lang">-->
			<!--			<script type="text/javascript" src="http://e.fstatic.eu/sh2/sh_{.}.js"></script>-->
			<!--		</x:for-each>-->
			<!--	</x:if>-->
			<!--</x:if>-->
			<x:if test="$role='admin'">
				<link href="http://e.fstatic.eu/css/admin.css" rel="stylesheet" type="text/css"/>
			</x:if>
			<script src="http://yui.yahooapis.com/3.0.0/build/yui/yui-min.js" type="text/javascript"/>
			<!--<script type="text/javascript" src="{$static}js/init.js"/>-->
			<script type="text/javascript"><x:value-of select="$doc//*[@name='layout']/script"/></script>
		</head>
		<body>
			<x:call-template name="layout">
				<x:with-param name="layout" select="$configdoc/layout"/>
			</x:call-template>
			<x:if test="count(//error)">
				<x:copy-of select="//error"/>
			</x:if>
		</body>
		</html>
	</x:template>

	<x:template name="layout">
		<x:param name="layout"/>
		<x:for-each select="$layout/*">
			<x:if test="local-name()='block'">
				<x:variable name="width">
					<x:choose>
						<x:when test="count(@width)"><x:value-of select="@width"/></x:when>
						<x:otherwise><x:value-of select="$configdoc/defaultwidth/node()"/></x:otherwise>
					</x:choose>
				</x:variable>
				<div class="{@type} w{$width} {@name}">
					<x:call-template name="layout">
						<x:with-param name="layout" select="."/>
					</x:call-template>
				</div>
			</x:if>
			<x:if test="local-name()='widget'">
				<div class="widget {@type}" id="{@name}">
					<x:apply-templates mode="widget" select="."/>
				</div>
			</x:if>
			<x:if test="local-name()='body'">
				<x:call-template name="layout">
					<x:with-param name="layout" select="$layoutdoc"/>
				</x:call-template>
			</x:if>
		</x:for-each>
	</x:template>

<!-- TODO add required fields support -->
	<x:template match="widget[@type='form']" mode="widget">
		<x:variable name="values" select="$doc//*[local-name()=current()/@values]/object"/>
		<form action="{@action}" method="post" enctype="multipart/form-data">
			<x:for-each select="item">
				<x:variable name="value">
					<x:variable name="helper" select="($values/@*|$values/*)[name()=current()/@name]"/>
					<x:choose>
						<x:when test="count(@value)">
							<x:copy-of select="$doc//object[@name=current()/@value]/node()"/>
						</x:when>
						<x:when test="not($helper)">
							<x:value-of select="."/>
						</x:when>
						<x:otherwise>
							<x:value-of select="$helper"/>
						</x:otherwise>
					</x:choose>
				</x:variable>
				<x:choose>
					<x:when test="local-name()='item' and @type='hidden'">
						<input id="{@name}" type="{@type}" name="{@name}" value="{$value}"/>
					</x:when>
					<x:when test="local-name()='item' and @type!='hidden'">
						<div class="item">
							<label for="{@name}">
								<x:choose>
								<x:when test="count(@langElement)">
									<x:value-of select="$langdoc//*[local-name()=current()/@langElement]"/>
								</x:when>
								<x:otherwise>
									<x:value-of select="@name"/>
								</x:otherwise>
								</x:choose>
							</label>
							<x:choose>
								<x:when test="@type='text' or @type='file' or @type='hidden' or @type='password'">
									<input id="{@name}" type="{@type}" name="{@name}" value="{$value}" accesskey="{@accesskey}"/>
								</x:when>
								<x:when test="@type='textarea'">
									<textarea id="{@name}" name="{@name}" accesskey="{@accesskey}"><x:copy-of select="$value"/></textarea>
								</x:when>
								<x:when test="@type='checkbox'">
									<input id="{@name}" type="checkbox" name="{@name}" value="true" accesskey="{@accesskey}">
									<x:if test="$value='t' or @checked='true'">
										<x:attribute name="checked">checked</x:attribute>
									</x:if>
									</input>
								</x:when>
								<x:when test="@type='spinner'">
									<div class="spinner">
										<input id="{@name}" name="{@name}" type="text" class="yui-spinner-value" value="{$value}"/>
									</div>
								</x:when>
								<x:otherwise>
									<select name="{@name}" accesskey="{@accesskey}">
										<x:if test="count(@multiple)">
											<x:attribute name="multiple">multiple</x:attribute>
										</x:if>
										<x:for-each select="document(concat($domain,'xml/types.xml'))/types/type[@id=current()/@type]//item">
											<x:variable name="optionValue">
												<x:choose>
													<x:when test="count(@value)=1"><x:value-of select="@value"/></x:when>
													<x:otherwise><x:value-of select="."/></x:otherwise>
												</x:choose>
											</x:variable>
											<option value="{$optionValue}">
											<x:if test="$value=@value">
												<x:attribute name="selected">selected</x:attribute>
											</x:if><x:value-of select="$langdoc//*[local-name()=current()/@langElement]"/>
											</option>
										</x:for-each>
									</select>
								</x:otherwise>
							</x:choose>
						</div>
					</x:when>
					<x:otherwise>
						<x:copy-of select="."/>
					</x:otherwise>
				</x:choose>
			</x:for-each>
			<input value="{$langdoc/submit/node()}" type="submit" accesskey="s"/>
		</form>
	</x:template>

<!--
	datasource is element with data for node
	context is template schema
-->
	<x:template name="template">
		<x:param name="datasource"/>
		<x:choose>
			<x:when test="local-name(.)='ml'">
				<x:copy-of select="$langdoc//*[local-name()=current()/@name]/*"/>
			</x:when>
			<x:when test="local-name(.)='node'">
				<x:copy-of select="$datasource//*[local-name()=current()/@name]/node()"/>
			</x:when>
			<x:when test="local-name(.)='attr'">
				<x:value-of select="$datasource/@*[local-name()=current()/@name]"/>
			</x:when>
			<x:when test="not(name())">
				<x:value-of select="normalize-space(.)"/>
			</x:when>
			<x:otherwise>
				<x:element name="{local-name()}">
					<x:for-each select="@*">
						<x:attribute name="{local-name()}">
							<x:variable name="temp">
								<x:value-of select="."/>
								<x:for-each select="parent::*/pars[@for=local-name(current())]/node()">
									<x:call-template name="template">
										<x:with-param name="datasource" select="$datasource"/>
									</x:call-template>
								</x:for-each>
							</x:variable>
							<x:value-of select="translate($temp, ' ', '_')"/>
						</x:attribute>
					</x:for-each>
					<x:for-each select="node()[local-name()!='pars']">
						<x:call-template name="template">
							<x:with-param name="datasource" select="$datasource"/>
						</x:call-template>
					</x:for-each>
				</x:element>
			</x:otherwise>
		</x:choose>
	</x:template>
</x:stylesheet>
