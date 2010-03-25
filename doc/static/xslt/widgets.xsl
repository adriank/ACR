<?xml version="1.0" encoding="UTF-8"?>
<x:stylesheet xmlns:x="http://www.w3.org/1999/XSL/Transform"
	version="1.0">

	<x:template match="widget[@type='notFound']" mode="widget">
		<x:copy-of select="$langdoc/notFound/node()"/><br/>
		<x:if test="$role='admin'">
			<a href="/admin-new_view/{$doc//view/@name}"><x:value-of select="$langdoc//notFoundAdmin"/></a>
		</x:if>
	</x:template>
<!-- TODO make it template with UL inner element -->
	<x:template match="widget[@type='menu']" mode="widget">
		<ul>
			<x:for-each select="./*">
				<x:sort select="position()" order="descending"/>
				<x:choose>
					<x:when test="$doc/view/@name=.">
						<li class="currentItem">
							<div class="left"/>
							<div class="right"/>
							<span><x:value-of select="$langdoc/menu/*[local-name()=current()]"/></span>
						</li>
					</x:when>
					<x:otherwise>
						<li class="item">
							<div class="left"/>
							<div class="right"/>
							<a href="/{.}">
								<x:value-of select="$langdoc/menu/*[local-name()=current()]"/>
							</a>
						</li>
					</x:otherwise>
				</x:choose>
			</x:for-each>
		</ul>
	</x:template>

	<x:template match="@lang" mode="schema">
		<div class="lang"><x:value-of select="$langdoc/words/language"/>: <img src="http://e.fstatic.eu/flags/{.}.png" alt="{.}"/>
		</div>
	</x:template>

	<x:template match="@create_date|@modification_date" mode="schema">
			<x:value-of select="concat(substring(.,0,11),' ',substring(.,11,6))"/>
	</x:template>

	<x:template match="widget[@type='paginate']" mode="widget">
		<x:variable name="pars" select="$doc//*[local-name()=current()/@parsSource]"/>
		<x:variable name="offset" select="$pars/offset/node()"/>
		<x:variable name="limit" select="$pars/limit/node()"/>
		<x:variable name="q" select="$pars/quantity/node()"/>
		<x:variable name="pages" select="ceiling($q div $limit)+1"/>
		<x:if test="$limit &lt; $q">
			<x:if test="$offset+1 &gt; $limit">
				<span class="previous"><a href="/{$doc//view/@name}/{$offset -$limit}/{$limit}"><x:value-of select="$langdoc//previousPage/node()"/></a></span>
			</x:if>
			<x:for-each select="($doc//node()|$doc//@*)[position() &lt; $pages]">
				<x:choose>
					<x:when test="position()=floor($offset div $limit)+1">
						<span class="current"><x:value-of select="position()"/></span>
					</x:when>
					<x:otherwise>
						<a class="number" href="/{$doc//view/@name}/{(position()-1)*$limit}/{$limit}"><x:value-of select="position()"/></a>
					</x:otherwise>
				</x:choose>
			</x:for-each>
			<x:if test="$q - $offset &gt; $limit">
				<span class="next"><a href="/{$doc//view/@name}/{$offset+$limit}/{$limit}"><x:value-of select="$langdoc/nextPage/node()"/></a></span>
			</x:if>
		</x:if>
	</x:template>
<!-- TODO delete logo widget -->
	<x:template match="widget[@type='logo']" mode="widget">
		<a href="{$domain}">
			<x:copy-of select="./node()"/>
		</a>
	</x:template>

	<x:template match="widget[@type='selectLang']" mode="widget">
		<ul>
			<x:for-each select="$doc/langs/*">
				<li>
					<x:choose>
						<x:when test="local-name()=$doc/langs/@current">
							<img alt="{local-name()}" src="http://e.fstatic.eu/flags/{local-name()}.png"/>
						</x:when>
						<x:otherwise>
							<a href="/changeLanguage/{local-name()}"><img alt="{local-name()}" src="http://e.fstatic.eu/flags/{local-name()}.png"/></a>
						</x:otherwise>
					</x:choose>
				</li>
			</x:for-each>
		</ul>
		<x:value-of select="$langdoc/words/language/node()"/>:
	</x:template>

	<x:template match="chapter" mode="article">
		<div class="chapter"><x:apply-templates mode="article"/></div>
	</x:template>

	<x:template match="source" mode="article">
		<div class="source">
			<pre>
				<x:if test="count(@lang)">
					<x:attribute name="class">sh_<x:value-of select="@lang"/></x:attribute>
				</x:if>
				<x:copy-of select="./node()"/></pre>
		</div>
	</x:template>

	<x:template match="ol|ul|img|table|code|p|span|a" mode="article">
		<x:copy-of select="."/>
	</x:template>

	<x:template match="title" mode="article">
		<a name="{.}"/>
		<x:element name="h{count(ancestor::chapter)+1}"><x:apply-templates mode="article" select="./node()"/></x:element>
	</x:template>

	<x:template name="toc">
		<ol class="toc">
			<x:for-each select="chapter">
				<li>
					<a class="toc" href="#{title}"><x:apply-templates mode="article" select="title/node()"/></a>
					<x:if test="count(.//chapter)&gt;0">
						<x:call-template name="toc"/>
					</x:if>
				</li>
			</x:for-each>
		</ol>
	</x:template>

	<x:template match="widget[@type='article']" mode="widget">
		<x:if test="$role='admin'">
			<div class="edit">
				<a href="/admin-edit_article/{$doc//article/item/@id}">edit</a>
			</div>
		</x:if>
		<x:apply-templates select="$doc//object[@name='article']//text" mode="article"/>
	</x:template>

	<x:template match="text" mode="article">
		<x:if test="$role='admin'">
			<x:variable name="text"><x:value-of select="//document/text"/></x:variable>
			<x:variable name="wos" select="translate(normalize-space($text),' ','')"/>
			<!-- TODO internationalization -->
			<h4>Stats:</h4>
			Words: <x:value-of select="string-length(normalize-space($text)) - string-length($wos) +1"/><br/>
			Chars (with spaces): <x:value-of select="string-length(normalize-space($text))"/><br/>
			Chars (w/o spaces): <x:value-of select="string-length($wos)"/><br/>
		</x:if>
		<h1><x:value-of select="//document/metainfo/booktitle"/></h1>
		<div class="Subtitle"><x:value-of select="//document/metainfo/booksubtitle"/></div>
		<x:if test="count(//document/metainfo/abstract)">
			<h2><x:value-of select="$langdoc/abstract"/></h2>
			<p class="abstract"><x:value-of select="//document/metainfo/abstract"/></p>
		</x:if>
		<x:if test="count(//title) and not(contains(//toc/node(),'false'))">
			<div id="toc">
				<h3><x:value-of select="$langdoc/toc/node()" />:</h3><br/>
				<x:call-template name="toc"/>
			</div>
		</x:if>
		<x:apply-templates mode="article"/>
	</x:template>

<!-- TODO tagCloud widget -->
	<x:template match="widget[@type='tagCloud']" mode="widget">
		<x:for-each select="tag">
		</x:for-each>
	</x:template>

	<x:template match="widget[@type='siteMap']" mode="widget">
		<x:variable name="datasource" select="$doc//*[local-name()=current()/@datasource]"/>
		<x:variable name="width" select="99.9 div count($datasource/category)"/>
		<x:for-each select="$datasource/category">
			<div class="block" style="width:{$width}%;">
				<h3><x:value-of select="$langdoc//*[local-name()=current()/@langElement]"/></h3>
				<ul>
					<x:for-each select="item">
						<li><a href="{@link}"><x:value-of select="$langdoc//*[local-name()=current()/@langElement]"/></a></li>
					</x:for-each>
				</ul>
			</div>
		</x:for-each>
		<div style="clear:both;"/>
	</x:template>

	<x:template match="widget[@type='rmotp']" mode="widget">
		<div class="center">
			<div class="title"><x:value-of select="$langdoc//*[local-name()='rmotp']"/></div>
			<div class="content">
				<x:value-of select="$langdoc//*[local-name()='rmotpText']"/>
				<x:apply-templates select="widget" mode="widget"/>
			</div>
		</div>
	</x:template>
	<x:template match="widget[@type='debug']" mode="widget">
		<x:if test="count($doc/debug)">
			<h1>Debug information</h1>
			<h2>Execution Log</h2>
			<table>
				<thead><td>Severity</td><td>Origin</td><td>File</td><td>Message</td></thead>
				<x:for-each select="$doc/debug/executionLog/item">
					<tr class="{@level}"><td><x:value-of select="@level"/></td><td><x:value-of select="@origin"/></td><td><x:value-of select="@file"/>[<x:value-of select="@line"/>]</td><td><x:value-of select="message"/></td></tr>
				</x:for-each>
			</table>
			<h2>Info</h2>
			<div class="info"><x:copy-of select="$doc/debug/info"/></div>
		</x:if>
	</x:template>
	<!-- interface:
		datasource - source element name in XML file; name MUST be unique; element content MUST be list of elements with name 'item'; 'item' elements can have both, subelements and attributes, any of them is supported
		showOnEmpty - default 'yes', if set to 'no' it not shows when no data is in list
	-->
	<!-- TODO: replace @schema with something more generic -->
	<x:template match="widget[@type='list']" mode="widget">
		<x:variable name="template" select="./template/node()"/>
		<x:if test="count($doc/*[local-name()=current()/@datasource]//object)&gt;0 or not(@showOnEmpty='no')">
			<x:variable name="name" select="@schema"/>
			<x:if test="$role='admin'">
				<div class="edit">
					<a href="/admin-new_{$name}">new</a>
				</div>
			</x:if>
			<!-- context changing for-each -->
			<x:for-each select="before/node()">
				<x:call-template name="template">
					<x:with-param name="datasource" select="."/>
				</x:call-template>
			</x:for-each>
			<x:variable name="schema" select="item"/>
			<x:if test="count($doc//*[local-name()=current()/@datasource]//object)=0">
				<x:copy-of select="$langdoc/noData/node()"/>
			</x:if>
			<x:for-each select="$doc//list[@name=current()/@datasource]/object">
				<x:variable name="item" select="."/>
				<!--<div class="widget {$template/parent::*/@name}">-->
					<x:if test="$role='admin'">
						<div class="edit">
							<a href="/admin-edit_{$name}/{./@id}">edit</a>
						</div>
					</x:if>
					<!-- TODO add wrapping element e.g. table or ul support -->
					<x:for-each select="$template">
						<x:call-template name="template">
							<x:with-param name="datasource" select="$item"/>
						</x:call-template>
					</x:for-each>
				<!--</div>-->
			</x:for-each>
			<x:for-each select="after/node()">
				<x:call-template name="template">
					<x:with-param name="datasource" select="."/>
				</x:call-template>
			</x:for-each>
		</x:if>
	</x:template>

<!-- template execution order is not deterministic -->
	<x:template match="widget[@type='template']" mode="widget">
		<x:variable name="datasource" select="$doc//*[@name=current()/@datasource]"/>
		<x:for-each select="*|text()|$doc//*[local-name()=current()/@docElement]|$langdoc//*[local-name()=current()/@langElement]">
			<x:call-template name="template">
				<x:with-param name="datasource" select="$datasource"/>
			</x:call-template>
		</x:for-each>
	</x:template>
</x:stylesheet>
