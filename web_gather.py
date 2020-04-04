import aiohttp
import asyncio
from aiostream import stream, pipe
import requests
import logging
import time
import eel

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


class AIOGatherer:
    def __init__(self, delay=0, retry=0, logger=None):
        self.delay = delay
        self.retry = retry
        self.logger = logger

    async def async_get(self, urls):
        result = []

        #TODO: Error checking
        async with aiohttp.ClientSession() as session:
            async def fetch(url):
                if self.logger: self.logger.log(f"Grabbing {url}")
                for _ in range(self.retry + 1):
                    try:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                return await resp.text()
                            else:
                                logging.error(f"Server returned error status {resp.status} on {url}")
                                if self.logger: self.logger.log(f"Error on {url}")
                                return ""
                    except aiohttp.InvalidURL:
                        logger.error(f"Invalid URL: {url} ")
                    except aiohttp.ClientPayloadError:
                        logging.error(f"Invalid payload")
                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                return ""
            url_stream = stream.iterate(urls) 
            html_stream = stream.map(url_stream, fetch, ordered=True, task_limit=10)

            async with html_stream.stream() as streamer:
                async for item in streamer:
                    result.append(item)
            return result

    def get(self, urls):
        return asyncio.run(self.async_get(urls))
    

