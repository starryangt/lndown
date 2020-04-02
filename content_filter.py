from readability import Document
from dragnet import extract_content
from bs4 import BeautifulSoup
import dragnet

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
        doc = Document(content)
        return ContentResult(doc.title(), doc.summary())

    def process(self, contents):
        return [self.process_one(x) for x in contents]

class DragnetFilter:

    def process_one(self, content):
        soup = BeautifulSoup(content)
        title = soup.title
        f_content = extract_content(content)
        return ContentResult(title, f_content)
    
    def process(self, contents):
        return [self.process_one(x) for x in contents]