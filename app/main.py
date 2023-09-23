import os

from fastapi import FastAPI
from fastapi import Request

import asyncio

# LLM
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Text generation
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

import copy


app = FastAPI(
    title='API LLM LaMini-Flan-T5-77M K8s',
    description= "API chatbot that allow you to use MBZUAI/LaMini-Flan-T5-77M locally/on-premise or in a secure environment"
    version='v0.0.1'
)

@app.get("/")
def hello():
    return {
        "hello": "This is a LLM model working locally on my own K8s",
        "from Pod": f"{os.environ.get('HOSTNAME', 'DEFAULT_ENV')}"
    }