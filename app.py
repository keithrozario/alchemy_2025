import asyncio
import os
from typing import List 
from dotenv import load_dotenv

from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend_functions import process_file
from backend_functions import LoanApplicationForm, get_form_data

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
    logging.info("Loan Application Received", extra={"json_fields": form_data.model_dump()})

    tasks = [process_file(file) for file in files]
    results = await asyncio.gather(*tasks)    
    response = {file.filename: result for file, result in zip(files, results)}

    logging.info("Loan Application Processed", extra={"json_fields": response})
    return {
        "form_data": form_data.model_dump(),
        "document_data": response,
        "status": "SUCCESS",
        "message": "Form submitted successfully"
    }


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    logging.info("Web Request Received", extra={"json_fields": request})
    return templates.TemplateResponse("index.html", {"request": request})
