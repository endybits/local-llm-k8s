import os

from fastapi import FastAPI, Query, Response
from fastapi.encoders import jsonable_encoder

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
    description= "API chatbot that allow you to use MBZUAI/LaMini-Flan-T5-77M locally/on-premise or in a secure environment",
    version='v0.0.1'
)


## Loading Lamini Model
pretrained_model_path = "./model/"


tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=pretrained_model_path)
base_model = AutoModelForSeq2SeqLM.from_pretrained(
    pretrained_model_name_or_path=pretrained_model_path,
    device_map='auto',
    torch_dtype=torch.float32
)

# Loading Pipeline on LangChain
model_kwargs = {
    "temperature": 1,
    "min_length": 30,
    "max_length": 350,
    "repetition_penalty": 5.0
}

llm = HuggingFacePipeline.from_model_id(
        model_id=pretrained_model_path,
        task='text2text-generation',
        model_kwargs=model_kwargs
        )

template = """{text}"""
prompt = PromptTemplate(input_variables=['text'], template=template)
chatbot = LLMChain(prompt=prompt, llm=llm)


@app.get("/")
def hello():
    return {
        "hello": "This is a LLM model working locally on my own K8s",
        "from Pod": f"{os.environ.get('HOSTNAME', 'DEFAULT_ENV')}"
    }


@app.get('/model')
def model():
    query = "Who is Albert Eistein?"
    bot_response = chatbot.run(query)
    print(bot_response)
    return {
        'query': query,
        'bot_response': bot_response,
        'tech_stuffs': {
            "hostname_pod": f"{os.environ.get('HOSTNAME', 'DEFAULT_ENV')}"
        }
    }


@app.get('/chatbot')
def model(query: str = Query(example="Write a poem to the moon")):
    bot_response = chatbot.run(query)
    response = {
        'query': query,
        'bot_response': bot_response,
        'tech_stuff': {
            "hostname_pod": f"{os.environ.get('HOSTNAME', 'DEFAULT_ENV')}"
        }
    }
    return jsonable_encoder(response)