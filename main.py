import eel
from web_gather import AIOGatherer
from content_filter import ReadabilityFilter, DragnetFilter
from pathlib import Path
from epub_writer import epub

eel.init("client/dist")

scraper_dict = {
    "http": AIOGatherer
}

content_dict = {
    "readability": ReadabilityFilter,
    "dragnet": DragnetFilter
}

@eel.expose
def hello_world(x):
    print("Hello ", x)

@eel.expose
def compile(metadata, urls):
    just_urls = map(lambda x: x['href'], urls)

    scraper = scraper_dict.get(metadata.get("scraper", "http"), AIOGatherer)()
    content_filter = content_dict.get(metadata.get("parser", "readability"), ReadabilityFilter)()

    HTML = scraper.get(just_urls)
    filtered_content = content_filter.process(HTML)

    content_list = [{'title': x.title, 'html': x.content} for x in filtered_content] 
    e = epub.EPuB(metadata, content_list)
    
    working_dir = Path.cwd()
    e.compile(working_dir, working_dir)

    

    


eel.start("index.html")

