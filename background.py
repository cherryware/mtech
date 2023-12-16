from os import environ
from time import sleep
from datetime import datetime
from aiohttp import ClientSession
from asyncio import run

t = int(environ.get("REQUESTS_DELAY"))
file = environ.get("TARGET_FILE")
url = environ.get("SOURCE_URL")


def processing(string):
    f = open(file, 'a')
    f.write(string+'\n')
    f.close()


def read_file():
    try: 
        f = open(file)
    except FileNotFoundError:
        return None
    else:
        last = eval(f.readlines()[-1])
        f.close()
        del last['log']
        last['created'] = datetime.strptime(last['created'],'%Y-%m-%dT%H:%M:%S.%f')
        return last


async def collection():
    async with ClientSession() as session:
        while True:
            sleep(t/1000)
            last = read_file()
            if last != None: ext = '?id='+last['id']
            else: ext = ''
            async with session.get(url+ext) as resopnce:
                data = await resopnce.json()
                for d in data:
                    time = datetime.strptime(d['created'],'%Y-%m-%dT%H:%M:%S.%f')
                    if last == None or time > last['created']: last = {'id':d['id'],'created':time}
                    processing(d.__str__())

run(collection())