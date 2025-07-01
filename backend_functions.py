import json
import uuid
import doc_agent.runners as runners
from doc_agent.helper_functions import run_query_with_file_data
from fastapi import UploadFile

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


async def process_file(file: UploadFile):

    # Randomly generate a session & user for each invocation
    # All runners share the same session_service, so the session ID is common
    # between all runners
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
