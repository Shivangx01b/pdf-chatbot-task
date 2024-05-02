from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from celery import Celery
from celery.result import AsyncResult
import redis
from core.vectordb import dbhandler
from core.agent import gptagent
import os
app = FastAPI()




#Redis broker
redis_url = "redis://localhost:6379"
redis_client = redis.from_url(redis_url)

# Celery Task Manager
celery_app = Celery("tasks", broker=redis_url, backend=redis_url)



# To answer your questions
@app.post("/query")
async def query_index(query: Request):
    req_info = await query.json()


    #Parse the incoming request json
    taskid = req_info['taskid']
    query_to_ask = req_info['question']


    task_result = AsyncResult(taskid)

    #Check if task is finished
    if task_result.state == "SUCCESS":
       
        
        #Get the stored vectors
        query_engine = dbhandler.VectorDbHandler.getindex()
        response = query_engine.query(query_to_ask)

        # Add one agent to check if answer is word to work match with question asked
        prompt = gptagent.OpenAIGPT3Agent.get_prompt(query_to_ask, response)

        llm_gpt_response = gptagent.OpenAIGPT3Agent.getconversation(prompt)
        
        return JSONResponse(content={"question": str(query_to_ask), "answer": str(llm_gpt_response)}, status_code=200)
    
    # Check if task id is still in pending
    elif task_result.state in ["PENDING", "STARTED"]:
        return JSONResponse(content={"status": "Your task {0} is still processing".format(taskid)}, status_code=200)
    
    # Give failure if task id fails
    else:
        return JSONResponse(content={"status": "Seems like something went wrong with taskid {0}".format(taskid)}, status_code=500)



# Upload pdf files here 
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Should be pdf content type
    if file.content_type != "application/pdf":
        return JSONResponse(content={"error": "Only PDF files are allowed"}, status_code=400)
    
    UPLOAD_DIRECTORY = "./data"
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    #Save the pdf file
    with open(file_location, "wb") as file_object:
        file_object.write(await file.read())

    task = process_pdf.delay()
    return JSONResponse(content={"task_id": task.id}, status_code=202)

@celery_app.task
def process_pdf():
    dbhandler.VectorDbHandler.storeindex()
    
    