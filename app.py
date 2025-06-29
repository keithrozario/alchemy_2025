import asyncio
import os
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend_functions import process_file
from loan_application import LoanApplicationForm, get_form_data

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = "TRUE"
os.environ['GOOGLE_CLOUD_PROJECT'] = "default-krozario"
os.environ['GOOGLE_CLOUD_LOCATION'] = "us-central1"

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
    tasks = [process_file(file) for file in files]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    document_data = {}
    for file, result in zip(files, results):
        if isinstance(result, Exception):
            print(f"Error processing file {file.filename}: {result}")
            document_data[file.filename] = {
                "error": f"Failed to process file: {file.filename}"
            }
        else:
            document_data[file.filename] = result

    return {
        "form_data": form_data.model_dump(),
        "document_data": document_data,
    }


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
