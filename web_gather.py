import requests
import logging
import time
import eel
from selenium import webdriver

logger = logging.getLogger("HTTP")

'''
WebGatherer
Input: List of URLs
Output: List of strings containing HTML

MUST PRSESERVE ORDER

Just one method:
- `get` (urls: list) -> list
'''

class RequestGatherer:

    def __init__(self, delay=0, retry=0, logger=None):
        self.delay = delay
        self.retry = retry
        self.logger = logger
    
    def get(self, urls):

        def retry_get(retries, delay):
            for _ in range(retries + 1):
                if self.logger: self.logger.log(f"Grabbing {url}")
                if not url: return ""
                r = requests.get(url)
                if r.status_code == 200:
                    return r.text
                else:
                    if self.logger: self.logger.log(f"Error on {url}")
                time.sleep(delay)
            return ""
            
 
        result = []
        for url in urls:
            result.append(retry_get(self.retry, self.delay))

        return result

class SeleniumGatherer:

    def __init__(self, delay=0, retry=0, logger=None):
        self.driver = webdriver.Safari()
        self.logger = logger
        self.delay = delay
    
    def get(self, urls):
        result = []
        for url in urls:
            if not 'http' in url or not 'https' in url:
                continue
            if self.logger: self.logger.log(f"Grabbing {url}")
            self.driver.get(url)
            if self.delay: time.sleep(self.delay)
            result.append(self.driver.page_source)
        if self.logger: self.logger.log("Done")
        return result


