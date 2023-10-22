from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
import chromadb
import dotenv
import openai
import os
from lib.query import generate_code, generate_sub_tasks

dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_KEY"]

app = FastAPI()
chroma_client = chromadb.PersistentClient(path="./chromadb")
collection = chroma_client.get_collection("task_to_chunk")

class UserGenerationRequest(BaseModel):
    prompt:str

default_component = """
import React from 'react'

const Component = () => {
return (
<div></div>
)
}

export default Component
""".strip()

@app.post("/")
def read_root(Prompt:UserGenerationRequest):
    
    user_prompt = Prompt.prompt
    print(f"Recieved user prompt of {user_prompt}")
    sub_tasks = generate_sub_tasks(user_prompt)
    
    print("Generated Sub Tasks")
    for task in sub_tasks:
        print(f"-{task}")

    relevant_results = collection.query(
        query_texts=[user_prompt],
        n_results=3
    )
    
    ctx = []
    uniq = set()
    for i in range(len(relevant_results["metadatas"])):
        for code_sample,sample_query in zip(relevant_results["metadatas"][i],relevant_results["documents"][i]):
            if sample_query not in uniq:
                ctx.append(f"Eg.{sample_query}\n```{code_sample}```\n")
                uniq.add(sample_query)

    ctx_string = "".join(ctx)

    generated_code = generate_code(ctx_string,user_prompt)
    print(generated_code)
    with open('../src/generated/component.tsx', 'w') as f:
        f.write(generated_code)
    
    return {
        "code":generated_code
    }

@app.get("/clear")
def clear_component():
    print("---Recieved request to clear")
    with open('../src/generated/component.tsx', 'w') as f:
        f.write(default_component)
    
    return {
        "message":"Ok"
    }