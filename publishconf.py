"""Production build settings."""
from pathlib import Path
from runpy import run_path

globals().update({
    key: value
    for key, value in run_path(str(Path(__file__).with_name("pelicanconf.py"))).items()
    if key.isupper()
})

SITEURL = "https://cobalt-lensing.github.io"
FEED_ALL_ATOM = "feed.xml"
DELETE_OUTPUT_DIRECTORY = True
