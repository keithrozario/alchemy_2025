from fastapi import Form, File, UploadFile, Request, FastAPI
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import os
from doc_agent.helper_functions import run_query_with_file_data
import json


app = FastAPI()
templates = Jinja2Templates(directory="templates")

from doc_agent.runners import SESSION_ID, USER_ID
from doc_agent.runners import aadhar_runner, form_16_runner, property_deed_runner, payslip_runner, document_identification_runner


os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = "TRUE"
os.environ['GOOGLE_CLOUD_PROJECT'] = "default-krozario"
os.environ['GOOGLE_CLOUD_LOCATION'] = "us-central1"
# os.environ["AGENT_ENGINE_ID"] = "1263761072779689984"


@app.post("/submit")
async def submit(
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    files: List[UploadFile] = File(...),
):

    response = {}

    for index, file in enumerate(files):
        response[file.filename] = await process_file(file)

    return {
        "form_data": {"first_name": first_name, "last_name": last_name, "address": address},
        "document_data": response
    }


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def process_file(file):
    data = await file.read()

    config = {
        "aadhar_card": {
            "query": "What are the fields in the aadhar_card",
            "runner": aadhar_runner,
        },
        "form_16": {
            "query": "What is the fields in the form 16 document?",
            "runner": form_16_runner
        }
    }

    r = run_query_with_file_data(
        query="What document is this?",
        doc_data=data,
        doc_mime_type=str(file.content_type),
        runner_instance=document_identification_runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    response = json.loads(r)
    document_type = response['document_type']
    
    r = run_query_with_file_data(
        query=config[document_type]['query'],
        doc_data=data,
        doc_mime_type=str(file.content_type),
        runner_instance=config[document_type]['runner'],
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    await file.close()

    return json.loads(r)