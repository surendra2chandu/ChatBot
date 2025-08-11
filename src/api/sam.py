from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/addition/")
def add(a:int , b: int):
    return a+b