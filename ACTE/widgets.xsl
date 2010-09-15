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
	<x:template name="menu">
		<li class="yui-menuitem">
			<a class="yui-menuitem-content" href="{@href}">
				<x:value-of select="$langdoc/menu/*[local-name()=current()/@name]"/>
			</a>
		</li>
	</x:template>

	<x:template match="widget[@type='menu']" mode="widget">
		<x:attribute name="class">widget yui3-menu <x:value-of select="@class"/></x:attribute>
		<div class="yui3-menu-content">
		<ul>
			<x:for-each select="./item">
				<li class="yui3-menuitem">
					<x:choose>
						<x:when test="count(item)">
							<a class="yui3-menu-label" href="#{@name}">
								<x:value-of select="$langdoc/menu/*[local-name()=current()/@name]"/>
							</a>
							<div id="{@name}" class="yui3-menu">
								<div class="yui3-menu-content">
									<ul>
										<x:for-each select="item">
											<x:call-template name="menu"/>
										</x:for-each>
									</ul>
								</div>
							</div>
						</x:when>
					 <x:otherwise>
						 <a class="yui-menuitem-content" href="{@href}">
							 <x:value-of select="$langdoc/menu/*[local-name()=current()/@name]"/>
						 </a>
					 </x:otherwise>
				 </x:choose>
				</li>
			</x:for-each>
		</ul>
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
	<x:template match="widget[@type='selectLang']" mode="widget">
		<ul>
			<x:for-each select="$doc/object[@name='acf:lang']/*">
				<li>
					<x:choose>
						<x:when test="local-name()=$doc/object[@name='acf:lang']/@current">
							<img alt="{local-name()}" src="http://e.acimg.eu/flags/{local-name()}.png"/>
						</x:when>
						<x:otherwise>
							<a href="/changeLanguage/{local-name()}"><img alt="{local-name()}" src="http://e.acimg.eu/flags/{local-name()}.png"/></a>
						</x:otherwise>
					</x:choose>
				</li>
			</x:for-each>
		</ul>
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

<!-- template execution order is not deterministic -->
	<x:template match="widget[@type='template']" name="templateWidget" mode="widget">
		<x:param name="datasource" select="@datasource"/>
		<x:choose>
			<x:when test="count(template)">
				<x:for-each select="template/node()">
					<x:call-template name="template">
						<x:with-param name="datasource" select="$datasource"/>
					</x:call-template>
				</x:for-each>
			</x:when>
			<x:otherwise>
				<x:for-each select="node()">
					<x:call-template name="template">
						<x:with-param name="datasource" select="$datasource"/>
					</x:call-template>
				</x:for-each>
			</x:otherwise>
		</x:choose>
	</x:template>

	<x:template match="widget[@type='wiki']" mode="widget">
		<x:param name="datasource" select="@datasource"/>
		<x:if test="$role='admin'">
			<a href="#langid-{$datasource/langid}" class="accms-admin"/>
		</x:if>
		<x:call-template name="templateWidget">
			<x:with-param name="datasource" select="$datasource"/>
		</x:call-template>
	</x:template>

</x:stylesheet>
