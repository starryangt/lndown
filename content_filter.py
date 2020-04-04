from readability import Document
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("CONTENT")

'''
ContentFilter
One method
- `process` : (content: list) -> list

Input: 
    - List of HTML strings

Result:
    - List of Result Objects
'''

class ContentResult:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def __repr__(self):
        return f'{self.title}: {self.content}'
    
    def __str__(self):
        return self.__repr__()

class ReadabilityFilter:

    def process_one(self, content):
        try:
            doc = Document(content)
            return ContentResult(doc.title(), doc.summary())
        except Exception as e:
            logger.error(f"Readability failed on {content.title} with error {e}") 
            return ContentResult('', '')

    def process(self, contents):
        return [self.process_one(x) for x in contents]
