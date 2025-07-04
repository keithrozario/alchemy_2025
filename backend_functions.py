import json
import uuid
import os
import doc_agent.runners as runners
from doc_agent.helper_functions import run_query_with_file_data
from fastapi import UploadFile
from google.cloud import storage
from google.cloud import bigquery
from doc_agent.tools.doc_tools import AllowedDocuments

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


async def process_file(file: UploadFile, trxn_id: str) -> dict:
    """
    Processes a single file and extracts the data from it.

    Args:
        file: The File uploaded by user to be processed (singular file)
        trxn_id: The Transaction ID for the loan application
    returns:
        doc_data_response: The data extracted from the document, will be a different format depending on the document
    """

    # Randomly generate a session id & user id for each invocation
    # All runners share the same session_service, so the session ID is common across all runners
    USER_ID = trxn_id
    SESSION_ID = uuid.uuid4().hex

    this_session = runners.session_service.create_session(
        user_id=USER_ID, session_id=SESSION_ID, app_name=runners.APP_NAME
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
        user_id=USER_ID, session_id=SESSION_ID, app_name=runners.APP_NAME
    )

    # save the file to GCS
    write_to_gcs(
        blob_in_bytes=file_data_in_bytes,
        file_name=str(file.filename),
        trxn_id=trxn_id,
        file_type=str(file.content_type),
    )  # type: ignore

    return json.loads(doc_data_response)


def write_to_gcs(
    blob_in_bytes: bytes, file_name: str, trxn_id: str, file_type: str
) -> str:
    """
    Receives a file and saves it to a GCS bucket

    Args:
        file: The file to write
    returns:
        location:The GCS URI of the uploaded file.
    """
    bucket_name = os.environ["LOAN_GCS_BUCKET"]
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Create a unique filename for the blob to prevent overwrites.
    blob = bucket.blob(f"uploads/{trxn_id}/{file_name.split('/')[-1]}")
    blob.upload_from_string(data=blob_in_bytes, content_type=file_type)

    return f"gs://{bucket_name}/{blob.name}"


def record_to_bq(full_response: dict):
    """
    Inserts a record into BQ for the application

    Args:
        data: The form data with the full representation of data from the application
    returns:
        status (bool): Boolean indicating if insertion was successful (or not)
    """

    client = bigquery.Client()
    table_id = os.environ["BQ_TABLE"]

    rows_to_insert = [
        {
            "application_id": full_response["trxn_id"],
            "FORM_fullName": full_response.get("form_data", {}).get("full_name", ""),
            "FORM_loan_type": full_response.get("form_data", {}).get("loan_type", ""),
            "FORM_aadhaar_number": full_response.get("form_data", {}).get(
                "aadhar_number", ""
            ),
            "FORM_pan": full_response.get("form_data", {}).get("pan_number", ""),
            "FORM_loan_tenure": full_response.get("form_data", {}).get(
                "loan_tenure", ""
            ),
            "FORM_loan_amount": full_response.get("form_data", {}).get(
                "loan_amount", ""
            ),
            "FORM_property_type": full_response.get("form_data", {}).get(
                "type_of_property", ""
            ),
        }
    ]
    try:
        errors = client.insert_rows_json(
            table_id, rows_to_insert
        )  # Make an API request.
    except:
        return False

    return True


def validate_response(document_data: dict) -> tuple[str, list]:
    """
    Checks if at least one of each document type is in the response
    """

    all_doc_types = {
        member.value
        for member in AllowedDocuments
        if member != AllowedDocuments.UNKNOWN_DOCUMENT
    }
    document_types_uploaded_list = [
        doc.get("document_type")
        for doc in document_data.values()
        if doc.get("document_type")
    ]
    missing_docs = all_doc_types.difference(set(document_types_uploaded_list))

    if missing_docs:
        status = "ERROR"
        messages = [f"Missing documents: {missing_docs}"]
    else:
        status = "SUCCESS"
        messages = ["All documents are present."]

    return status, messages
