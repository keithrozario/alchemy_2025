import asyncio
import os
import uuid
import json
from typing import List 
from dotenv import load_dotenv

from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend_functions import process_file, write_to_gcs, LoanApplicationForm, get_form_data, validate_response

load_dotenv()

# Imports the Cloud Logging client library and local
import logging
# check if we're in CloudRun
if "PORT" in os.environ and "K_SERVICE" in os.environ and "K_REVISION" in os.environ:
    import google.cloud.logging
    client = google.cloud.logging.Client()
    client.setup_logging()
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")


@app.post("/submit")
async def submit(
    form_data: LoanApplicationForm = Depends(get_form_data),
    files: List[UploadFile] = File(...),
):
    """
    Accepts loan application form data and files, processes them concurrently,
    and returns the extracted data.
    """
    
    trxn_id = uuid.uuid4().hex # generates random transaction id
    logging.info(f"Loan Application Received {trxn_id}", extra={"json_fields": form_data.model_dump()})

    tasks = [process_file(file, trxn_id) for file in files]
    results = await asyncio.gather(*tasks)    
    response = {file.filename: result for file, result in zip(files, results)}

    status, messages = validate_response(response)

    logging.info(f"Loan Application Processed {trxn_id}", extra={"json_fields": response})
    user_response = {
        "form_data": form_data.model_dump(),
        "document_data": response,
        "status": status,
        "messages": messages,
        "trxn_id": trxn_id,
        "preliminary_assessment": "Some string for now!"
        }
    write_to_gcs(
        blob_in_bytes=json.dumps(user_response, indent=4).encode('utf-8'), 
        file_name=f"{trxn_id}.json",
        trxn_id=trxn_id,
        file_type="application/json"
    )
    return user_response


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    logging.info("Web Request Received", extra={"json_fields": request})
    return templates.TemplateResponse("index.html", {"request": request})
