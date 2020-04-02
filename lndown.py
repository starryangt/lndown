import web_gather
import content_filter
from dragnet import extract_content
from epub_writer import epub
from pathlib import Path

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes in a list of urls")
    parser.add_argument('--index', dest='index', type=str, help="File with a list of urls")
    parser.add_argument('--title', dest='title', type=str)

    args = parser.parse_args()
    if args.index:
        with open(args.index, 'r') as f:
            url = f.read()
        
        urls = list(url.split('\n'))
        
        g = web_gather.AIOGatherer()
        r = content_filter.ReadabilityFilter()

        stuff = g.get(urls[:-1])
        final = r.process(stuff)
        
        mdata = {
            'title': args.title,
            'author': "Unknown",
        }
        content_list = []
        for result in final:
            entry = {
                'title': result.title,
                'html': result.content
            }
            content_list.append(entry)
        
        e = epub.EPuB(mdata, content_list)
        current_dir = Path.cwd()
        e.compile(current_dir, current_dir)

