import eel
from web_gather import AIOGatherer, RequestGatherer
from content_filter import ReadabilityFilter
from pathlib import Path
from epubwriter import EPuB
import logging

eel.init("client/dist")

scraper_dict = {
    "sync": RequestGatherer,
    "async": AIOGatherer
}

content_dict = {
    "readability": ReadabilityFilter
}

print(eel._js_functions)
eel.log("fuck")
@eel.expose
def hello_world(x):
    print("Hello ", x)

@eel.expose
def compile(metadata, urls):
    just_urls = map(lambda x: x['href'], urls)

    delay = int(metadata.get("delay", 0))
    retry = int(metadata.get("retry", 0))
    
    scraper = scraper_dict.get(metadata.get("scraper", "async"), AIOGatherer)(delay, retry, eel)
    content_filter = content_dict.get(metadata.get("parser", "readability"), ReadabilityFilter)()

    eel.log(f"Grabbing sites (delay {delay}, retry {retry} )...")
    try:
        HTML = scraper.get(just_urls)
    except Exception as e:
        eel.log(f"Error: {e}")
        return

    eel.log("Filtering content...")
    try:
        filtered_content = content_filter.process(HTML)
    except Exception as e:
        eel.log(f"Error: {e}")
        return

    content_list = [{'title': x.title, 'html': x.content} for x in filtered_content] 
    eel.log("Creating EPUB")
    e = EPuB(metadata, content_list)
    
    try: 
        working_dir = Path.cwd()
        e.compile(working_dir, working_dir)
    except Exception as e:
        eel.log(f"Error: {e}")
        return
    eel.log("Done")


eel.start("index.html")

