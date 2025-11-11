from fastapi import FastAPI
from pydantic import BaseModel
from utils.config import mini_judge_config
from utils.languages import LANGUAGE_EXTENSIONS
from utils.files import store_file
from utils.db import add_new_submission,get_submissions
import uuid
from workers.ce_worker import codeExecutionQueue,execute_code
from pydantic import BaseModel,HttpUrl
from fastapi import Query
from typing import Optional




app = FastAPI()

class PayloadData(BaseModel):
    language:int
    source_code:str
    stdin:str
    webhook_url: Optional[HttpUrl] = None 



@app.get("/")
def index():
    return {
        "message":"Pong",
        "success":True
    }


@app.post("/submit")
async def submit_code(payload: PayloadData):
    # language,source_code_stdin=paylod
    # if 
    # r.rpush(queue_name, data)
    random_id = str(uuid.uuid4())
    fileDetails = store_file(payload.source_code,payload.language,random_id,stdin=payload.stdin)
    add_new_submission(random_id,payload.language,webhook=payload.webhook_url or "")

    codeExecutionQueue.enqueue(execute_code,language=payload.language,folder_path=fileDetails["folder_path"],id=random_id)
    # if(fileDetails.success == False):
    #     return {"status":"failed"}
    
    return {"message":"code submitted","token":random_id}


@app.get("/languages")
async def get_languages():
    return {"message": "Languages available","result":LANGUAGE_EXTENSIONS}

@app.get("/submission")
async def get_submission(tokens: str = Query(...)):
    submissions = get_submissions(ids=tokens)
    return {"message": "Languages available","result":LANGUAGE_EXTENSIONS,"submissions":submissions}