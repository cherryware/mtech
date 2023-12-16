from os import environ
from time import sleep
from threading import Thread
from random import randint, choice
from string import ascii_lowercase as ascii
from requests import post
from json import dumps
from uuid import uuid4


t = int(environ.get("THREADS"))
ms = int(environ.get("REQUESTS_DELAY"))
url = environ.get("TARGET_URL")


def processing(file, string):
    code = post(url, json=dumps({"log": string}))
    f = open("./logs/" + file, 'a')
    f.write(string+' >>> ' + str(code) + '\n')
    f.close()


def generation():
    file = uuid4().__str__()[0:8] + ".log"
    while True: 
        ip = '{}.{}.{}.{}'.format(randint(0,255),randint(0,255),randint(0,255),randint(0,255))
        method = choice(['GET','POST','PUT','PATCH','DELETE'])
        uri = choice(['http://','https://','ftp://'])
        for i in range(randint(3,10)):
            uri += choice(ascii)
        uri += choice(['.com','.net','.org'])
        if (randint(0,1) > 0): 
            uri += '/'
            for i in range(randint(5,7)):
                uri += choice(ascii)
        code = choice([100,103,200,201,204,206,301,302,303,304,307,308,401,403,404,406,407,409,410,412,416,418,451,500,501,502,503,504])
        string = '{' + ip + '}' + ' {' + method + '}' + ' {' + uri + '}' + ' {' + str(code) + '}'
        processing(file, string)
        sleep(randint(0,ms)/1000)


sleep(7)
threads = []
for i in range(0, t):
    th = Thread(target=generation)
    threads.append(th)
    th.start()

for th in threads:
    th.join()
