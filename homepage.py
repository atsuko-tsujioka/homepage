import grequests
import requests
import urllib
import time
import csv

urllist = list()

i = 0 
with open('homepage.csv', 'r') as a:
    for line in a:
        i+=1
        arr = line[:-1].split(',')
        urllist.append([arr[0],arr[4]])

import aiohttp
import asyncio
import async_timeout

writerlist = []

async def fetch(session, url, id):
    try:
        async with async_timeout.timeout(3000):
            async with session.get(url) as response:
                print([id, str(url),response.status])
                writerlist.append([id, str(url),response.status])
    except Exception as e:
        print([id, str(url),type(e)])
        writerlist.append([id, str(url), type(e)])



async def main():
    with open('result.csv', 'w') as rfile:
        writer = csv.writer(rfile,lineterminator='\n')
        async with aiohttp.ClientSession() as session:
            urls = urllist
            promises = [fetch(session, u[1], u[0]) for u in urls]
            await asyncio.gather(*promises)
        writer.writerows(writerlist)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()    
    loop.run_until_complete(main())