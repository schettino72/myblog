# -*- coding: utf-8 -*-

import os

########################################
# Configuration, please edit
########################################

# Data about this site
BLOG_AUTHOR = "schettino72"
BLOG_TITLE = "Rounder Wheels"
BLOG_URL = "http://blog.schettino72.net"
BLOG_EMAIL = "schettino72@gmail.com"
BLOG_DESCRIPTION = "on programming"

# post_pages contains (wildcard, destination, template, use_in_feed) tuples.
#
# The wildcard is used to generate a list of reSt source files
# (whatever/thing.txt).
# That fragment must have an associated metadata file (whatever/thing.meta),
# and opcionally translated files (example for spanish, with code "es"):
#     whatever/thing.txt.es and whatever/thing.meta.es
#
# From those files, a set of HTML fragment files will be generated:
# cache/whatever/thing.html (and maybe cache/whatever/thing.html.es)
#
# These files are combinated with the template to produce rendered
# pages, which will be placed at
# output / TRANSLATIONS[lang] / destination / pagename.html
#
# where "pagename" is specified in the metadata file.
#
# if use_in_feed is True, then those posts will be added to the site's
# rss feeds.
#

post_pages = (
    ("_posts/*.md", "posts", "post.tmpl", True),
)

# One or more folders containing files to be copied as-is into the output.
# The format is a dictionary of "source" "relative destination".
# Default is:
FILES_FOLDERS = {'_files': '' }
# Which means copy 'files' into 'output'

# What is the default language?
DEFAULT_LANG = "en"

# What other languages do you have?
# The format is {"translationcode" : "path/to/translation" }
# the path will be used as a prefix for the generated pages location
TRANSLATIONS = {
    DEFAULT_LANG: "",
    #"es": "./es",
    }

# Paths for different autogenerated bits. These are combined with the
# translation paths.

# Final locations are:
# output / TRANSLATION[lang] / TAG_PATH / index.html (list of tags)
# output / TRANSLATION[lang] / TAG_PATH / tag.html (list of posts for a tag)
# output / TRANSLATION[lang] / TAG_PATH / tag.xml (RSS feed for a tag)
TAG_PATH = "categories"

# If TAG_PAGES_ARE_INDEXES is set to True, each tag's page will contain
# the posts themselves. If set to False, it will be just a list of links.
TAG_PAGES_ARE_INDEXES = False

# Final location is output / TRANSLATION[lang] / INDEX_PATH / index-*.html
INDEX_PATH = ""
# Final locations for the archives are:
# output / TRANSLATION[lang] / ARCHIVE_PATH / ARCHIVE_FILENAME
# output / TRANSLATION[lang] / ARCHIVE_PATH / YEAR / index.html
ARCHIVE_PATH = "archive"
ARCHIVE_FILENAME = "index.html"
# Final locations are:
# output / TRANSLATION[lang] / RSS_PATH / rss.xml
RSS_PATH = ""

# Slug the Tag URL easier for users to type, special characters are
# often removed or replaced as well.
SLUG_TAG_PATH = True

# A list of redirection tuples, [("foo/from.html", "/bar/to.html")].
#
# A HTML file will be created in output/foo/from.html that redirects
# to the "/bar/to.html" URL. notice that the "from" side MUST be a
# relative URL.
#
# If you don't need any of these, just set to []

REDIRECTIONS = []

# Commands to execute to deploy. Can be anything, for example,
# you may use rsync:
# "rsync -rav output/* joe@my.site:/srv/www/site"
# And then do a backup, or ping pingomatic.
# To do manual deployment, set it to []
DEPLOY_COMMANDS = []

# Where the output site should be located
# If you don't use an absolute path, it will be considered as relative
# to the location of conf.py
#OUTPUT_FOLDER = '.'
OUTPUT_FOLDER = '_output'

CACHE_FOLDER = '_cache'

# Filters to apply to the output.
# A directory where the keys are either: a file extensions, or
# a tuple of file extensions.
#
# And the value is a list of commands to be applied in order.
#
# Each command must be either:
#
# A string containing a '%s' which will
# be replaced with a filename. The command *must* produce output
# in place.
#
# Or:
#
# A python callable, which will be called with the filename as
# argument.
#
# By default, there are no filters.
FILTERS = {
#    ".jpg": ["jpegoptim --strip-all -m75 -v %s"],
}

##############################################################################
# Image Gallery Options
##############################################################################

# Galleries are folders in galleries/
# Final location of galleries will be output / GALLERY_PATH / gallery_name
GALLERY_PATH = "galleries"
THUMBNAIL_SIZE = 180
MAX_IMAGE_SIZE = 1280
USE_FILENAME_AS_TITLE = True

##############################################################################
# HTML fragments and diverse things that are used by the templates
##############################################################################

# Data about post-per-page indexes
INDEXES_TITLE = ""  # If this is empty, the default is BLOG_TITLE
INDEXES_PAGES = ""  # If this is empty, the default is 'old posts page %d' translated

# Name of the theme to use. Themes are located in themes/theme_name
THEME = '_custom_theme'  # http://bootswatch.com/readable/

DATE_FORMAT = "%Y-%m-%d"

# Show only teasers in the index pages? Defaults to False.
# INDEX_TEASERS = False

# A HTML fragment describing the license, for the sidebar.
# I recomment using the Creative Commons' wizard:
# http://creativecommons.org/choose/
LICENSE = ''
# """
# <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/2.5/ar/">
# <img alt="Creative Commons License BY-NC-SA"
# style="border-width:0; margin-bottom:12px;"
# src="http://i.creativecommons.org/l/by-nc-sa/2.5/ar/88x31.png"></a>"""

# A small copyright notice for the page footer (in HTML)
CONTENT_FOOTER = u'Contents &copy; 2012 schettino72 - Powered by <a href="http://nikola.ralsina.com.ar">Nikola</a>'

# To enable comments via Disqus, you need to create a forum at
# http://disqus.com, and set DISQUS_FORUM to the short name you selected.
# If you want to disable comments, set it to False.
DISQUS_FORUM = 'schettino72blog'

# Enable Addthis social buttons?
# Defaults to true
ADD_THIS_BUTTONS = False

# Modify the number of Post per Index Page
# Defaults to 10
INDEX_DISPLAY_POST_COUNT = 3

# RSS_LINK is a HTML fragment to link the RSS or Atom feeds. If set to None,
# the base.tmpl will use the feed Nikola generates. However, you may want to
# change it for a feedburner feed or something else.
RSS_URL = "http://feeds.feedburner.com/schettino72"
RSS_LINK = """<link rel="alternate" type="application/rss+xml" title="RSS (en)" href="%s">""" % RSS_URL

# A search form to search this site, for the sidebar. You can use a google
# custom search (http://www.google.com/cse/)
# Or a duckduckgo search: https://duckduckgo.com/search_box.html
# This example should work for pretty much any site we generate.
SEARCH_FORM = ""
# This search form is better for the "site" theme where it
# appears on the navigation bar
#SEARCH_FORM = """
#<!-- Custom search -->
#<form method="get" id="search" action="http://duckduckgo.com/" """\
#"""class="navbar-form pull-left">
#<input type="hidden" name="sites" value="%s"/>
#<input type="hidden" name="k8" value="#444444"/>
#<input type="hidden" name="k9" value="#D51920"/>
#<input type="hidden" name="kt" value="h"/>
#<input type="text" name="q" maxlength="255" """\
#"""placeholder="Search&hellip;" class="span2" style="margin-top: 4px;"/>
#<input type="submit" value="DuckDuckGo Search" style="visibility: hidden;" />
#</form>
#<!-- End of custom search -->
#""" % BLOG_URL

# Google analytics or whatever else you use. Added to the bottom of <body>
# in the default template (base.tmpl).
ANALYTICS = """
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-36931321-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
"""

# Put in global_context things you want available on all your templates.
# It can be anything, data, functions, modules, etc.
GLOBAL_CONTEXT = {
    'analytics': ANALYTICS,
    'blog_author': BLOG_AUTHOR,
    'author_url': '',
    'blog_title': BLOG_TITLE,
    'blog_url': BLOG_URL,
    'blog_desc': BLOG_DESCRIPTION,
    'date_format': DATE_FORMAT,
    'translations': TRANSLATIONS,
    'license': LICENSE,
    'search_form': SEARCH_FORM,
    'disqus_forum': DISQUS_FORUM,
    'content_footer': CONTENT_FOOTER,
    'rss_path': RSS_PATH,
    'rss_url': RSS_URL,
    'rss_link': RSS_LINK,
    # Locale-dependent links for the sidebar
    # You should provide a key-value pair for each used language.
    'sidebar_links': {
        DEFAULT_LANG: (
            ('/' + os.path.join(ARCHIVE_PATH, ARCHIVE_FILENAME), 'Archives'),
            ('/categories/index.html', 'Tags'),
            ),
        }
    }
