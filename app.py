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
import doc_agent.runners as runners


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
            "runner": runners.aadhar_runner,
        },
        "form_16": {
            "query": "What is the fields in the form 16 document?",
            "runner": runners.form_16_runner
        },
        "salary_slip": {
            "query": "What is the fields in the Salary Slip?",
            "runner": runners.payslip_runner
        },
        "property_sale_deed": {
            "query": "What is the fields in the Property Sale Deed?",
            "runner": runners.property_deed_runner
        },
        "bank_statement": {
            "query": "What is the fields in the Bank Statement?",
            "runner": runners.bank_statement_runner
        }
    }

    r = run_query_with_file_data(
        query="What document is this?",
        doc_data=data,
        doc_mime_type=str(file.content_type),
        runner_instance=runners.document_identification_runner,
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