import json
import uuid
import doc_agent.runners as runners
from doc_agent.helper_functions import run_query_with_file_data
from fastapi import UploadFile

from fastapi import Form
from pydantic import BaseModel

class LoanApplicationForm(BaseModel):
    full_name: str
    loan_type: str
    aadhar_number: str
    pan_number: str
    loan_tenure: str
    loan_amount: str
    type_of_property: str

CONFIG = {
    "aadhar_card": {
        "query": "What are the fields in the Aadhar Card",
        "runner": runners.aadhar_runner,
    },
    "form_16": {
        "query": "What is the fields in the form 16 document?",
        "runner": runners.form_16_runner,
    },
    "salary_slip": {
        "query": "What is the fields in the Salary Slip?",
        "runner": runners.payslip_runner,
    },
    "property_sale_deed": {
        "query": "What is the fields in the Property Sale Deed?",
        "runner": runners.property_deed_runner,
    },
    "bank_statement": {
        "query": "What is the fields in the Bank Statement?",
        "runner": runners.bank_statement_runner,
    },
    "pan_card": {
        "query": "What is the fields in the PAN Card?",
        "runner": runners.pan_card_runner,
    },
}

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

async def process_file(file: UploadFile)-> dict:
    """
    Processes a single file and extracts the data from it.


    Args:
        file: The File uploaded by user to be processed (singular file)
    returns:
        doc_data_response: The data extracted from the document, will be a different format depending on the document
    """

    # Randomly generate a session id & user id for each invocation
    # All runners share the same session_service, so the session ID is common across all runners
    USER_ID = uuid.uuid4().hex
    SESSION_ID = uuid.uuid4().hex

    this_session = runners.session_service.create_session(
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        app_name=runners.APP_NAME
    )

    file_data_in_bytes = await file.read()
    await file.close()

    identification_response = run_query_with_file_data(
        query="What document is this?",
        doc_data=file_data_in_bytes,
        doc_mime_type=str(file.content_type),
        runner_instance=runners.document_identification_runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    try:
        doc_identity = json.loads(identification_response)
        document_type = doc_identity["document_type"]
    except:  # catch all exceptions for now -- terrible practice I know!
        entry = {
            "message": identification_response,
            "severity": "ERROR",
        }
        return entry

    doc_data_response = run_query_with_file_data(
        query=CONFIG[document_type]["query"],
        doc_data=file_data_in_bytes,
        doc_mime_type=str(file.content_type),
        runner_instance=CONFIG[document_type]["runner"],
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runners.session_service.close_session(session=this_session)
    runners.session_service.delete_session(
        user_id=USER_ID, 
        session_id=SESSION_ID,
        app_name=runners.APP_NAME
    )
    
    return json.loads(doc_data_response)
