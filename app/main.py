import os

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {
        "hello": "This is a LLM model working locally on my own K8s",
        "from Pod": f"{os.environ.get('HOSTNAME', 'DEFAULT_ENV')}"
    }