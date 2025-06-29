from doc_agent.helper_functions import run_query_with_file_data
from doc_agent.runners import SESSION_ID, USER_ID
import doc_agent.runners as runners
import json

def write_to_bq(user_response: dict):
    print("hello")


async def process_file(file):
    data = await file.read()
    await file.close()

    config = {
        "aadhar_card": {
            "query": "What are the fields in the Aadhar Card",
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
        },
        "pan_card": {
            "query": "What is the fields in the PAN Card?",
            "runner": runners.pan_card_runner
        }
    }

    identification_response = run_query_with_file_data(
        query="What document is this?",
        doc_data=data,
        doc_mime_type=str(file.content_type),
        runner_instance=runners.document_identification_runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    try:
        doc_identity = json.loads(identification_response)
        document_type = doc_identity['document_type']
    except: # catch all exceptions for now
        entry = {
            "message": identification_response,
            "severity": "ERROR",
        }
        print(json.dumps(entry))
        return f"Error {identification_response}"

    doc_data_response = run_query_with_file_data(
        query=config[document_type]['query'],
        doc_data=data,
        doc_mime_type=str(file.content_type),
        runner_instance=config[document_type]['runner'],
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    return json.loads(doc_data_response)