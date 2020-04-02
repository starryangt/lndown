import aiohttp
import asyncio
from aiostream import stream, pipe
import logging

logger = logging.getLogger("HTTP")

'''
WebGatherer
Input: List of URLs
Output: List of strings containing HTML

MUST PRSESERVE ORDER

Just one method:
- `get` (urls: list) -> list
'''

class AIOGatherer:
    def __init__(self):
        pass

    async def async_get(self, urls):
        result = []

        #TODO: Error checking
        async with aiohttp.ClientSession() as session:
            async def fetch(url):
                try:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            return await resp.text()
                        else:
                            logging.error(f"Server returned error status {resp.status}")
                except aiohttp.InvalidURL:
                    logger.error(f"Invalid URL: {url} ")
                except aiohttp.ClientPayloadError:
                    logging.error(f"Invalid payload")
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
            url_stream = stream.iterate(urls) 
            html_stream = stream.map(url_stream, fetch, ordered=True, task_limit=10)

            async with html_stream.stream() as streamer:
                async for item in streamer:
                    result.append(item)
            return result

    def get(self, urls):
        return asyncio.run(self.async_get(urls))
    
