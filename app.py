from fastapi import Form, File, UploadFile, Request, FastAPI
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from backend_functions import process_file


# Environment variables for local testing
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
    full_name: str = Form(...),
    loan_type: str = Form(...),
    aadhar_number: str = Form(...),
    pan_number: str = Form(...),
    loan_tenure: str = Form(...),
    loan_amount: str = Form(...),
    type_of_property: str = Form(...),
    files: List[UploadFile] = File(...),
):

    response = {}

    for index, file in enumerate(files):
        response[file.filename] = await process_file(file)

    return {
        "form_data": {
            "full_name" : full_name,
            "aadhar_number": aadhar_number,
            "pan_number": pan_number,
            "loan_tenure": loan_tenure,
            "loan_amount": loan_amount,
            "type_of_property": type_of_property,
            "loan_type": loan_type,
        },
        "document_data": response
    }


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

