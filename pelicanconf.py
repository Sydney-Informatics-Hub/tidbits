#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import alchemy

AUTHOR = "Sydney Informatics Hub"
SITENAME = "SIH Tech Tidbits"
SIH_URL = "https://www.sydney.edu.au/research/facilities/sydney-informatics-hub.html"
SITESUBTITLE = f"Useful tips, libraries and tools from the <a href='{SIH_URL}'>Sydney Informatics Hub</a> team"
SITEURL = ""

PATH = "content"
STATIC_PATHS = ["images", "downloads", "static"]

TIMEZONE = "Australia/Sydney"

DEFAULT_LANG = "en"

# Theme settings
THEME = alchemy.path()
THEME_TEMPLATES_OVERRIDES = ["custom_templates"]
THEME_CSS_OVERRIDES = ["/static/css/tag_cloud.css"]
THEME_JS_OVERRIDES = [
    "https://code.jquery.com/jquery-3.6.0.min.js",
    "/static/js/tipuesearch.min.js",
    "/static/js/tipuesearch_set.js",
    "/tipuesearch_content.js",
    "/static/js/activate_search.js",
]
PYGMENTS_STYLE = "paraiso-dark"
DEFAULT_PAGINATION = 10

# General content settings
SUMMARY_MAX_LENGTH = 30

# Plugin settings
PLUGINS = ["pelican.plugins.tag_cloud", "pelican.plugins.tipue_search"]
DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "search"]

# Tag cloud settings
TAG_CLOUD_STEPS = 5
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SORTING = "alphabetically"
TAG_CLOUD_BADGE = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()
# Social widget
SOCIAL = ()


# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
