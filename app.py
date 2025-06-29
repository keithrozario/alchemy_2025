from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    Request,
    UploadFile,
)
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
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


class LoanApplicationForm(BaseModel):
    full_name: str
    loan_type: str
    aadhar_number: str
    pan_number: str
    loan_tenure: str
    loan_amount: str
    type_of_property: str


def get_form_data(
    full_name: str = Form(...),
    loan_type: str = Form(...),
    aadhar_number: str = Form(...),
    pan_number: str = Form(...),
    loan_tenure: str = Form(...),
    loan_amount: str = Form(...),
    type_of_property: str = Form(...),
) -> LoanApplicationForm:
    return LoanApplicationForm(
        full_name=full_name,
        loan_type=loan_type,
        aadhar_number=aadhar_number,
        pan_number=pan_number,
        loan_tenure=loan_tenure,
        loan_amount=loan_amount,
        type_of_property=type_of_property,
    )


@app.post("/submit")
async def submit(
    form_data: LoanApplicationForm = Depends(get_form_data),
    files: List[UploadFile] = File(...),
):

    response = {}

    for index, file in enumerate(files):
        response[file.filename] = await process_file(file)

    return {
        "form_data": form_data.model_dump(),
        "document_data": response
    }


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
