<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<xsl:variable name="user" select="Page/User"/>
<xsl:variable name="prod" select="Page/ArtProduct"/>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/static/ProductDetails.css"/>
        <link rel="stylesheet" href="/static/Banner.css"/>
        <link rel="stylesheet" href="/static/Box.css"/>
        <link rel="stylesheet" href="/static/Button.css"/>
        <link rel="stylesheet" href="/static/DropDown.css"/>
        <link rel="stylesheet" href="/static/ContactInfo.css"/>
        <link rel="stylesheet" href="/static/Comments.css"/>
        <link rel="stylesheet" href="/static/ProductCart.css"/>
        <link rel="icon" href="/static/images/icons8-shop-local-16.png"/>
        <title>
            <xsl:value-of select="$prod/name"/>
        </title>
        <script type="text/javascript" src="/static/CartOperations.js" defer="defer"></script>
    </head>
    <body>
    <header>
        <section class="banner">
            <section class="logo">
                <img src="/static/images/banner.jpg" alt="Logo"/>
            </section>
            <form class="search" action="/search" method="GET">
                <div class="search-field">
                    <label for="id_search"></label>
                    <input type="text" id="id_search" name="search" placeholder="Search"/>
                </div>
            </form>
            <section class="user-info">
                <xsl:choose>
                    <xsl:when test="$user/is_auth = 'True' and $user/is_admin = 'False'">
                        <div class="dropdown">
                            <button class="drop-button">
                                <img src="/static/images/loggedIn.jpg" alt="Log"/>
                            </button>
                            <div class="dropdown-content">
                                <a>
                                    <xsl:attribute name="href">
                                        <xsl:value-of select="concat('/profile/', $user/prof_id, '/')"/>
                                    </xsl:attribute>
                                    Profile
                                </a>
                                <form action="/logout/" method="post">
                                    <input type="hidden" name="csrfmiddlewaretoken">
                                        <xsl:attribute name="value">
                                            <xsl:value-of select="Page/csrf_token"/>
                                        </xsl:attribute>
                                    </input>
                                    <button type="submit" class="button">LOG OUT</button>
                                </form>
                            </div>
                        </div>
                        <div class="username-banner">
                            <xsl:value-of select="$user/username"/>
                        </div>
                    </xsl:when>
                    <xsl:otherwise>
                        <form action="/login/" method="get">
                            <button class="button" type="submit">LOG IN</button>
                        </form>
                    </xsl:otherwise>
                </xsl:choose>
            </section>
        </section>
        <nav class="navbar">
            <a href="/">Home</a>
            <a href="/products/">All Pictures</a>
            <xsl:choose>
                <xsl:when test="$user/is_auth = 'True' and $user/is_admin = 'False'">
                    <a>
                        <xsl:attribute name="href">
                            <xsl:value-of select="concat('/profile/', $user/prof_id)"/>
                        </xsl:attribute>
                        Profile
                    </a>
                </xsl:when>
            </xsl:choose>
        </nav>
    </header>
    <main>
        <section class="box product-details-layout">
            <h2><xsl:value-of select="$prod/name"/></h2>
            <img>
                <xsl:attribute name="src">
                    <xsl:value-of select="$prod/image"/>
                </xsl:attribute>
                <xsl:attribute name="alt">
                    <xsl:value-of select="$prod/name"/>
                </xsl:attribute>
                <xsl:attribute name="height">
                    <xsl:value-of select="$prod/image_height"/>
                </xsl:attribute>
                <xsl:attribute name="width">
                    <xsl:value-of select="$prod/image_height"/>
                </xsl:attribute>
            </img>
            <h3>Price</h3>
            <p><xsl:value-of select="$prod/price"/> $ per copy</p>
            <h3>Copies</h3>
            <p><xsl:value-of select="$prod/copies"/></p>
            <h3>Type of Paint</h3>
            <p><xsl:value-of select="$prod/paint_type"/></p>
            <h3>Genre</h3>
            <p><xsl:value-of select="$prod/genre"/></p>
            <h3>Material</h3>
            <p><xsl:value-of select="$prod/material"/></p>
            <h3>Description</h3>
            <article><xsl:value-of select="$prod/description"/></article>
            <h3>Rating</h3>
            <p><xsl:value-of select="$prod/rate"/> / 5</p>
            <button id="addToCart"
                    class="button add-to-cart"
                    data-product-id="{$prod/id}">
                Add to Cart
            </button>
            <h2>Comments</h2>
            <section class="comments-section">
                <xsl:choose>
                    <xsl:when test="$user/is_auth = 'False'">
                        <p>You must be logged in to leave a comment.</p>
                    </xsl:when>
                    <xsl:otherwise>
                        <form method="post">
                            <xsl:attribute name="action">
                                <xsl:value-of select="concat('/products/', $prod/id, '/comment')"/>
                            </xsl:attribute>
                            <label for="id_comment_form">Write your opinion</label>
                            <textarea type="text" id="id_comment_form" name="comment" placeholder="Write comment"></textarea>
                            <input type="hidden" name="csrfmiddlewaretoken">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="Page/csrf_token"/>
                                </xsl:attribute>
                            </input>
                            <button type="submit" class="button">Send</button>
                        </form>
                    </xsl:otherwise>
                </xsl:choose>
            </section>
            <section class="comments-section">
                <xsl:for-each select="Page/Comments/Comment">
                    <div>
                        <h4>Username: <xsl:value-of select="user"/></h4>
                        <p>Commented: <xsl:value-of select="created_at"/></p>
                        <article><xsl:value-of select="text"/></article>
                    </div>
                </xsl:for-each>
            </section>
        </section>
    </main>
    <footer>
        <h3>Contact the Artist!</h3>
        <p>Email: artist@example.com</p>
        <p>Phone: +1234567890</p>
        <address>Address: 123 Art Street, City, Country</address>
        <p>Copyright © 2024 Art Store</p>
    </footer>
    </body>
    </html>
</xsl:template>
</xsl:stylesheet>
