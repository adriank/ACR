<?xml version="1.0" encoding="UTF-8"?>
<x:stylesheet xmlns:x="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<x:output method="html" version="4.01" encoding="UTF-8"
		doctype-public="-//W3C//DTD HTML 4.01//EN"
		doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>
<!-- TODO some of these variables should be merged with others -->
	<x:variable name="doc" select="/list"/>
	<x:variable name="lang" select="//object[@name='acf:lang']/@current"/>
<!-- TODO create generator which sets domain -->
<!-- IE don't understand relative paths so domain MUST be predefined -->
	<x:variable name="domain" select="//object[@name='acf:appDetails']/@domain"/>
	<!--<x:variable name="configdoc" select="document(concat($domain,'/xml/config.xml'))/config"/>-->
	<!--<x:variable name="langdoc" select="document(concat($domain,'/texts/',$lang,'.xml'))/t"/>-->
	<x:variable name="config" select="//object[@name='acf:appDetails']/@config"/>
	<x:variable name="configdoc" select="document(concat('','../xml/',$config,'.xml'))/config"/>
	<x:variable name="langdoc" select="document(concat('../texts/',$lang,'.xml'))/t"/>
	<x:variable name="static" select="$configdoc/staticdomain/node()"/>
	<x:variable name="role" select="$doc/object[@name='acf:user']/@role"/>
	<!--<x:variable name="f"><x:value-of select="$domain"/>layouts/<x:value-of select="/document/view/@name"/>.xml</x:variable>-->
	<x:variable name="layoutdoc" select="//object[@name='layout']"/>
	<!--<x:variable name="layoutdoc" select="document($layoutfile)/layout"/>-->
	<x:include href="widgets.xsl"/>

	<x:template match="/">
		<html>
		<head>
			<!-- TODO add datasource support -->
			<title>
				<x:for-each select="$layoutdoc/pagetitle/node()">
					<x:call-template name="template">
						<x:with-param name="datasource"><none/></x:with-param>
					</x:call-template>
				</x:for-each>
				-
				<x:for-each select="$configdoc/name/node()">
					<x:call-template name="template">
						<x:with-param name="datasource"><none/></x:with-param>
					</x:call-template>
				</x:for-each>
			</title>
			<meta name="description" content="{$configdoc/description/node()}"/>
			<meta name="keywords" content="{$configdoc/keywords/node()}"/>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
			<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7"/>
			<!-- export css and js to config.xml -->
			<link rel="stylesheet" type="text/css" href="http://e.acimg.eu/css/yui-rf.css"/>
			<link href="http://e.acimg.eu/css/grids.css" rel="stylesheet" type="text/css"/>
			<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?3.2.0/build/node-menunav/assets/skins/sam/node-menunav.css"/>
			<link href="http://e.acimg.eu/css/style.css" id="customstyles" rel="stylesheet" type="text/css"/>
			<link href="{$static}css/style.css" rel="stylesheet" type="text/css"/>
			<!--<x:if test="$role='admin'">-->
			<!--	<link href="http://e.acimg.eu/css/admin.css" rel="stylesheet" type="text/css"/>-->
			<!--</x:if>-->
			<script type="text/javascript" src="http://yui.yahooapis.com/combo?3.2.0/build/yui/yui-min.js&amp;3.2.0/build/loader/loader-min.js"></script>
			<script type="text/javascript" src="/js/init.js"/>
			<script type="text/javascript"><x:value-of select="$doc//*[@name='layout']/script"/></script>
		</head>
		<body>
			<x:apply-templates select="$layoutdoc"/>
			<x:if test="count(//error)">
				<x:copy-of select="//error"/>
			</x:if>
			<x:if test="$role='admin'">
				<div id="accms-admin"/>
			</x:if>
		</body>
		</html>
	</x:template>

	<x:template match="container">
		<x:variable name="width">
			<x:value-of select="@width"/>
			<x:if test="not(@width)"><x:value-of select="$configdoc/defaultwidth/node()"/></x:if>
		</x:variable>
		<div class="container w{$width} {@name}">
			<x:apply-templates select="./*"/>
		</div>
	</x:template>

	<x:template match="column">
		<div class="column {@type} {@name}">
			<x:apply-templates select="./*"/>
		</div>
	</x:template>

	<x:template match="script|pagetitle"/>
	<x:template match="widget">
		<x:variable name="datasource" select="$doc/*[@name=current()/@datasource]"/>
		<x:variable name="tag">
			<x:value-of select="@tag"/>
			<x:if test="not(@tag)">div</x:if>
		</x:variable>
		<x:element name="{$tag}">
			<x:attribute name="id"><x:value-of select="@name"/></x:attribute>

			<x:variable name="before">
				<x:for-each select="before/node()">
					<x:call-template name="template">
						<x:with-param name="datasource" select="."/>
					</x:call-template>
				</x:for-each>
			</x:variable>
			<x:variable name="type">
				<x:value-of select="@type"/>
				<x:if test="not(@type)">template</x:if>
			</x:variable>

			<x:choose>
				<x:when test="local-name($datasource)='list'">
					<x:attribute name="class">widget <x:value-of select="$type"/>-list</x:attribute>
					<x:copy-of select="$before"/>
					<x:variable name="this" select="."/>
					<x:variable name="subtag">
						<x:value-of select="@subtag"/>
						<x:if test="not(@subtag)">div</x:if>
					</x:variable>
					<x:for-each select="$datasource/object">
						<x:element name="{$subtag}">
							<x:attribute name="class">widget <x:value-of select="$type"/>-item</x:attribute>
							<x:apply-templates mode="widget" select="$this">
								<x:with-param name="datasource" select="."/>
							</x:apply-templates>
						</x:element>
					</x:for-each>
					<x:if test="$role='admin'">
						<div class="accms-optionsPanel"/>
					</x:if>
				</x:when>
				<x:otherwise>
					<x:attribute name="class">widget <x:value-of select="$type"/>-item</x:attribute>
					<x:copy-of select="$before"/>
					<x:apply-templates mode="widget" select=".">
						<x:with-param name="datasource" select="$datasource"/>
					</x:apply-templates>
				</x:otherwise>
			</x:choose>

			<x:for-each select="after/node()">
				<x:call-template name="template">
					<x:with-param name="datasource" select="."/>
				</x:call-template>
			</x:for-each>
		</x:element>
	</x:template>

	<x:template match="access">
		<a href="#" accesskey="{@key}"/>
	</x:template>
	<!-- TODO add required fields support -->
	<x:template match="widget[@type='form']" mode="widget">
		<x:variable name="values" select="$doc//*[@name=current()/@values]"/>
		<form action="{@action}" method="post" enctype="multipart/form-data">
			<x:for-each select="item">
				<x:variable name="value">
					<x:variable name="helper" select="$values/*[name()=current()/@name]"/>
					<x:choose>
						<x:when test="@value">
							<x:copy-of select="$doc//object[@name=current()/@value]/node()"/>
						</x:when>
						<x:when test="not($helper)">
							<x:copy-of select="."/>
						</x:when>
						<x:otherwise>
							<x:copy-of select="$helper/node()"/>
						</x:otherwise>
					</x:choose>
				</x:variable>
				<x:choose>
					<x:when test="local-name()='item' and @type='hidden'">
						<input id="{@name}" type="{@type}" name="{@name}" value="{$value}"/>
					</x:when>
					<x:when test="local-name()='item' and @type!='hidden'">
						<div class="item">
							<x:if test="count(@label)=0 or @label='enabled'">
								<label for="{@name}">
									<x:choose>
										<x:when test="count(@ml)">
											<x:value-of select="$langdoc//*[local-name()=current()/@ml]"/>
										</x:when>
										<x:otherwise>
											<x:value-of select="@name"/>
										</x:otherwise>
									</x:choose>
								</label>
							</x:if>
							<x:choose>
								<x:when test="@type='text' or @type='file' or @type='hidden' or @type='password'">
									<input id="{@name}" type="{@type}" name="{@name}" value="{$value}" accesskey="{@accesskey}"/>
								</x:when>
								<x:when test="@type='textarea'">
									<textarea id="{@name}" name="{@name}" accesskey="{@accesskey}"><x:copy-of select="$value"/></textarea>
								</x:when>
								<x:when test="@type='RTE'">
									<textarea id="{@name}" name="{@name}" accesskey="{@accesskey}" class="accms-RTE"><x:value-of select="$value"/></textarea>
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
				<x:copy-of select="$langdoc//*[local-name()=current()/@name]/node()"/>
			</x:when>
			<x:when test="local-name(.)='node'">
				<x:copy-of select="$datasource//*[local-name()=current()/@name]/node()"/>
			</x:when>
			<x:when test="local-name(.)='attr'">
				<x:value-of select="$datasource/@*[local-name()=current()/@name]"/>
			</x:when>
			<x:when test="not(name())">
				<x:value-of select="."/>
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
					<!-- changed node() -> text()|* -->
					<x:for-each select="text()|*[local-name()!='pars']">
						<x:call-template name="template">
							<x:with-param name="datasource" select="$datasource"/>
						</x:call-template>
					</x:for-each>
				</x:element>
			</x:otherwise>
		</x:choose>
	</x:template>
</x:stylesheet>
