"""Local build settings; run from the repository root."""
from pathlib import Path

AUTHOR = "COBALT consortium"
SITENAME = "COBALT"
SITESUBTITLE = "Making the darkness visible"
DESCRIPTION = "Searching for non-accreting black holes in binary star systems through the gravitational lensing of light from their companion stars."
CONTACT_EMAIL = "M.J.Middleton@soton.ac.uk"
SITEURL = ""
TIMEZONE = "Europe/London"
DEFAULT_LANG = "en"
PATH = "content"
THEME = "themes/cobalt"
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["cache_bust"]
OUTPUT_PATH = "output"
ARTICLE_PATHS = ["articles"]
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["assets", "legacy"]
EXTRA_PATH_METADATA = {
    f"legacy/{path.name}": {"path": path.name}
    for path in Path("content/legacy").glob("*.md")
}
ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}.html"
ARTICLE_SAVE_AS = ARTICLE_URL
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
DIRECT_TEMPLATES = ["index"]
INDEX_SAVE_AS = "news/index.html"
DEFAULT_PAGINATION = False
AUTHOR_SAVE_AS = AUTHORS_SAVE_AS = ""
CATEGORY_SAVE_AS = CATEGORIES_SAVE_AS = ""
TAG_SAVE_AS = TAGS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
USE_FOLDER_AS_CATEGORY = False
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = [
    ("Home", "/"), ("About", "/about/"), ("Science", "/science/"),
    ("Citizen Science", "/CitizenScience/"), ("Alerts", "/Alerts/"),
    ("News", "/news/"), ("Members", "/Members/"),
]
FEED_ALL_ATOM = None
FEED_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
SUMMARY_MAX_LENGTH = 50
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.extra": {}, "markdown.extensions.meta": {},
        "pymdownx.arithmatex": {"generic": True},
    },
    "output_format": "html5",
}
