from os import environ
from time import time
from datetime import datetime
from uuid import uuid4
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.dialects.postgresql import CHAR, TIMESTAMP, INET, VARCHAR, SMALLINT
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse


engine = create_engine(environ.get("DATABASE_URI"))

class Base(DeclarativeBase): pass

class Postgre(Base):
    __tablename__ = 'mtech'
    unique_id = Column(CHAR, unique=True, primary_key=True)
    created = Column(TIMESTAMP)
    ip_address = Column(INET)
    http_method = Column(VARCHAR)
    request_uri = Column(VARCHAR)
    http_code = Column(SMALLINT)

    def __init__(self, ip, method, uri, code):
        self.ip_address = ip
        self.http_method = method
        self.request_uri = uri
        self.http_code = code
        self.unique_id = uuid4().__str__()
        self.created = datetime.utcfromtimestamp(time())

app = FastAPI()

@app.post("/api/data")
async def post_data(data:str = Body()):
    data = eval(data).get("log")
    if data == None: 
        return PlainTextResponse("Что-то пошло не так", status_code=418)
    data = data.split()
    if len(data) != 4: 
        return PlainTextResponse("Что-то пошло не так", status_code=418)
    ip = data[0].replace("{","").replace("}","")
    method = data[1].replace("{","").replace("}","")
    uri = data[2].replace("{","").replace("}","")
    code = data[3].replace("{","").replace("}","")
    if not code.isdecimal(): 
        return PlainTextResponse("Что-то пошло не так", status_code=418)
    logging= Postgre(ip,method,uri,int(code))
    with Session(bind=engine) as db:
        db.add(logging)
        db.commit()
    return PlainTextResponse("Лог сохранен", status_code=201)


@app.get("/api/data")
async def get_data(id = None):
    list = []
    with Session(bind=engine) as db:
        if id != None: 
            last = db.get(Postgre,id).created
        else:
            last = datetime.utcfromtimestamp(42)
        logged = db.query(Postgre).filter(Postgre.created > last)
        for l in logged:
            data = {"ip":l.ip_address, "method":l.http_method, "uri":l.request_uri, "status_code":l.http_code}
            report = {"id":l.unique_id, "created":l.created, "log":data}
            list.append(report)
    return list
