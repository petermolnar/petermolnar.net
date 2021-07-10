<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
    <xsl:template match="atom:feed">
        <html lang="en">
            <head>
                <title><xsl:value-of select="atom:title"/></title>
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

h2 {
    margin-top: 4em;
}

img {
    display: block;
    max-height: 98vh;
    max-width: 100%;
    width: auto;
    height: auto;
    margin: 0 auto;
    border: 1px solid #000;
}
                </style>
            </head>
            <body>
                <p>
                    <a>
                        <xsl:attribute name="href">
                            <xsl:value-of select="atom:link[@rel='alternate' and @type='text/html']/@href"/>
                        </xsl:attribute>
                        &#171; back to <xsl:value-of select="atom:id" />
                    </a>
                </p>
                <h1><xsl:value-of select="atom:title" /></h1>
                <aside>
                    <p>
                        Hi! You're looking at something called a
                        <strong>feed</strong>, also known as RSS, Atom,
                        etc. It's an easy and simple way to subscribe to
                        or follow website updates.
                    </p>

                    <p>
                        If you've known this already, or already using a
                        feed reader: please copy the URL of this page
                        into it if you want to subscribe.
                    </p>

                    <p>
                        To learn about feeds,
                        <a href="https://aboutfeeds.com">About Feeds</a>
                        is a good place to look, but in essence: imagine
                        a social media feed where have all the control:
                        what to see, from who, in what order, or what form.
                    </p>

                    <p>
                        If you're looking for a feed reader, I can
                    recommend:
                    </p>
                    <ul>
                        <li>
                            <a href="https://www.freshrss.org/">FreshRSS</a>
                            (self-hosted web application)
                        </li>
                        <li>
                            <a href="http://www.lzone.de/liferea/">Liferea</a>
                            (linux desktop)
                        </li>
                    </ul>
                    <p>
                        but in case they are not what you're looking for,
                        have a <a href="https://www.subtome.com/#/store">a look
                        around</a> for more.
                    </p>

                    <p>
                        I also have a <a href="https://groups.google.com/forum/#!forum/petermolnarnet/join">
                        'petermolnarnet' Google Groups</a> in case
                        someone would like to receive updates in email.
                        (The reason for the Groups is to avoid the Spam
                        folder of Gmail).
                    </p>

                    <p>
                        This very page you're looking at is in
                        <a href="https://validator.w3.org/feed/docs/atom.html">ATOM</a>
                        format. To make it look like a webpage in a
                        browser it's transformed with the help of an
                        <a href="/feed/atom.xsl">XSL</a>.
                    </p>
                </aside>
                <xsl:apply-templates select="atom:entry"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="atom:entry" xmlns="http://www.w3.org/1999/xhtml">
        <h2>
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="atom:link[@rel='alternate' and @type='text/html']/@href"/>
                </xsl:attribute>
                <xsl:value-of select="atom:title"/>
            </a>
        </h2>
        <p><time><xsl:value-of select="atom:published" /></time></p>
        <xsl:value-of select="atom:summary" disable-output-escaping="yes" />
        <p>
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="atom:link[@rel='alternate' and @type='text/html']/@href"/>
                </xsl:attribute>
                Continue »
            </a>
        </p>
        <xsl:if test="atom:link[@rel='enclosure']">
            <p>
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="atom:link[@rel='alternate' and @type='text/html']/@href"/>
                    </xsl:attribute>
                    <img>
                        <xsl:attribute name="src">
                            <xsl:value-of select="atom:link[@rel='enclosure']/@href" />
                        </xsl:attribute>
                    </img>
                </a>
            </p>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>
