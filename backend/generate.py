import json
from typing import List
import openai
import instructor
import dotenv
from lib.types import MultiTaskType, Task, TaskToCode 
import os
import chromadb
from chromadb.api import API
from pathlib import Path
import uuid
import time
import asyncio 

instructor.patch()
dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_KEY"]


data_dir = Path(Path.cwd(),"data","tasks.json")
trial_run = ["Toast"]

async def generate_task_given_chunk(chunk:str,retries=3)->List[str]:
    for _ in range(retries):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                temperature=0.3,
                stream=False,
                max_retries=2,
                functions=[MultiTaskType.openai_schema],
                function_call={"name": MultiTaskType.openai_schema["name"]},
                messages=[
                {
                    "role": "system",
                    "content": f"As an experienced programmer using the NextJS Framework with the @shadcn/ui and tailwindcss library, you are tasked with brainstorming some tasks that could have resulted in the following code chunk being produced."
                },
                {
                    "role":"assistant",
                    "content":"Examples of such tasks could be adding a toast component to display temporary messages, using a specific variant avaliable in the @shadcn/ui library or configuring a component that toggles between two display states"
                },
                {
                "role":"assistant",
                "content": "Tasks should be as diverse as possible while staying relevant. Generate at most 4 Tasks."
                    },
                { 
                    "role": "user",
                    "content": f"{chunk}",
                },
            ],
                max_tokens=1000,
            )    
            res = MultiTaskType.from_response(completion)
            return [i.task for i in list(res)[0][1]]
        except Exception as e:
            print("----Encountered an exception")
            print(e)
            await asyncio.sleep(60)

    print("Failed to generate a response after 3 attempts")
    return []
        
    

    

def extract_examples_from_data(doc_data):
    return [i["code"] for i in doc_data["docs"]["examples"]]

def generate_code_tasks():
    mapping = {}

    # First read in the dump.json file
    with open('dump.json') as f:
        data = json.load(f)

    for idx,raw_data in enumerate(data):
        mapping[raw_data["name"]] = idx

    code_examples = []
    
    queries = {}

    for key in mapping.keys():
        print(f"---Processing {key}")
        start = time.time()
        code_examples:List[str] = extract_examples_from_data(data[mapping[key]])
        loop = asyncio.get_event_loop()
        tasks = [generate_task_given_chunk(code_example) for code_example in code_examples]
        results = loop.run_until_complete(asyncio.gather(*tasks))

        print(f"Finished processing {key} in {time.time()-start}")
        for code_example, potential_tasks in zip(code_examples, results):
            if key not in queries:
                queries[key] = {}
            queries[key][code_example] = potential_tasks
        with open(data_dir,"w+") as f:
            json.dump(queries, f)
    return queries

def generate_embeddings(chroma_client:API):
    # We first check to see if we have previously generated a query json obj
    if not data_dir.is_file():
        queries = generate_code_tasks()
        with open(data_dir,"w+") as f:
            json.dump(queries, f)
    
    with open(data_dir,"r") as f:
        queries = json.load(f)
    
    collection_name = 'task_to_chunk'
    try:
        collection = chroma_client.get_collection(collection_name)
        chroma_client.delete_collection(collection_name)
        print(f"Deleted {collection_name}.")
    except Exception as e:
        print(f"Collection {collection_name} does not exist...creating now")
    # We generate the task list, and we have the code. The next step is to then embed each of the individual tasks into a chromadb database
    collection:chromadb.Collection = chroma_client.get_or_create_collection(collection_name)
    

    start = time.time()

    # Then we embed the individual queries
    for component in queries.keys():
        for chunk in queries[component].keys():
            for task in queries[component][chunk]:
                id = uuid.uuid4()
                collection.add(
                    documents=[task],
                    metadatas=[{
                        "chunk":chunk,
                        "component":component,
                    }],
                    ids=[id.__str__()]
                )

    print(f"Embedding Complete in {time.time() - start}s")

    
if __name__ == "__main__":
    chroma_client = chromadb.PersistentClient(path="./chromadb")
    # Generate Embeddings
    generate_embeddings(chroma_client = chroma_client)

    

    
    

    