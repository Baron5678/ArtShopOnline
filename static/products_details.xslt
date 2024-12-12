<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
        <html>
            <head>
                <title>
                    <xsl:value-of select="Product/name"/>
                </title>
                <script type="text/javascript" src="../static/AddToCart.js"></script>
            </head>
        <body>
            <h2><xsl:value-of select="Product/name"/></h2>
            <section>
                    <img>
                        <xsl:attribute name="src">
                            <xsl:value-of select="Product/image"/>
                        </xsl:attribute>
                        <xsl:attribute name="alt">
                            <xsl:value-of select="Product/name"/>
                        </xsl:attribute>
                        <xsl:attribute name="height">
                            200
                        </xsl:attribute>
                        <xsl:attribute name="width">
                            200
                        </xsl:attribute>
                    </img>
            </section>
            <section>
                <p><xsl:value-of select="Product/price"/></p>
                <p><xsl:value-of select="Product/paint_type"/></p>
                <p><xsl:value-of select="Product/genre"/></p>
                <p><xsl:value-of select="Product/material"/></p>
            </section>
            <button id="addToCart" onclick="addToCartFunction()" data-product-id="{Product/id}">Add to Cart</button>
         </body>
        </html>
</xsl:template>
</xsl:stylesheet>
