<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/opml">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            <head>
                <title><xsl:value-of select="head/title"/></title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <style type="text/css">
* {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}

html {
    background-color: #222;
    color: #ccc;
}

body {
    font-family: sans-serif;
    background-color: #222;
    line-height: 1.3em;
    max-width: 86ch;
    margin: 0 auto;
    padding: 0.6em;
}

h1 {
    line-height: 1.3em;
}

a {
    color: #f90;
    text-decoration: none;
    border-bottom: 1px solid transparent;
}
a:hover {
    color: #fff;
    border-bottom: 1px solid #fff;
}

time {
  font-family: monospace;
}

aside {
    border: 1px solid #f90;
    padding: 1em;
}

summary {
    font-weight: bold;
    text-transform: uppercase;
    border-bottom: 3px solid #111;
    padding: 0.6em;
}

details {
    margin-bottom: 4em;
}

svg {
    transform: rotate(0deg);
    fill: currentColor;
    vertical-align:middle;
    margin-right: 0.6em;
}

                </style>
            </head>
            <body>
                <p>
                    <a>
                        <xsl:attribute name="href">
                            <xsl:value-of select="head/ownerId"/>
                        </xsl:attribute>
                        &#171; back to <xsl:value-of select="head/ownerName" />
                    </a>
                </p>
                <h1><xsl:value-of select="head/title"/></h1>
                <aside>
                    <p>
                        Hi! You're looking at blogroll: a curated list
                        of websites I subscribed to for updates, via
                        their <a href="https://aboutfeeds.com">feeds</a>.
                    </p>

                    <p>
                        This very page you're looking at is in
                        <a href="https://en.wikipedia.org/wiki/OPML">OPML</a>
                        format. To make it look like a webpage in a
                        browser it's transformed with the help of
                        <a href="opml.xsl">XSL</a>.
                    </p>

                    <p>
                        OPML was created so people can share their list
                        of followed blogs and websites. Usually it be
                        imported into <a href="https://en.wikipedia.org/wiki/News_aggregator">
                        a feed reader</a>, or, in some of
                        them, one can subscribe to the OPML directly
                        to sync lists of subscriptions.
                    </p>

                </aside>
                <p>Last updated: <time><xsl:value-of select="head/dateCreated"/></time></p>
                <xsl:apply-templates select="body/outline"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="outline" xmlns="http://www.w3.org/1999/xhtml">
        <xsl:choose>
            <xsl:when test="@type">
                <dt><a href="{@htmlUrl}"><xsl:value-of select="@title"/></a></dt>
                <dd>
                    <p>
                        <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M14.5 0h-13c-0.825 0-1.5 0.675-1.5 1.5v13c0 0.825 0.675 1.5 1.5 1.5h13c0.825 0 1.5-0.675 1.5-1.5v-13c0-0.825-0.675-1.5-1.5-1.5zM4.359 12.988c-0.75 0-1.359-0.603-1.359-1.353 0-0.744 0.609-1.356 1.359-1.356 0.753 0 1.359 0.613 1.359 1.356 0 0.75-0.609 1.353-1.359 1.353zM7.772 13c0-1.278-0.497-2.481-1.397-3.381-0.903-0.903-2.1-1.4-3.375-1.4v-1.956c3.713 0 6.738 3.022 6.738 6.737h-1.966zM11.244 13c0-4.547-3.697-8.25-8.241-8.25v-1.956c5.625 0 10.203 4.581 10.203 10.206h-1.963z"></path></svg>
                        <a href="{@xmlUrl}"><xsl:value-of select="@xmlUrl"/></a>
                    </p>
                </dd>
            </xsl:when>
            <xsl:otherwise>
                <details open="open">
                    <summary>
                        <xsl:value-of select="@title"/>
                    </summary>
                    <dl>
                        <xsl:apply-templates select="outline"/>
                    </dl>
                </details>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
