from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService

import uuid
import json
import os
from pathlib import Path

from doc_agent.helper_functions import run_query_with_file_data
from doc_agent.agents import aadhar_agent, form_16_agent, property_deed_agent, payslip_agent, document_identification_agent

APP_NAME = "test_app"
USER_ID = "test_user_456"
SESSION_ID = uuid.uuid4().hex
MODEL_NAME = "gemini-2.0-flash"

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = "TRUE"
os.environ['GOOGLE_CLOUD_PROJECT'] = "default-krozario"
os.environ['GOOGLE_CLOUD_LOCATION'] = "us-central1"
os.environ["AGENT_ENGINE_ID"] = "1263761072779689984"

session_service = InMemorySessionService()
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
artifact_service = InMemoryArtifactService()

aadhar_runner = Runner(
    agent=aadhar_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

form_16_runner = Runner(
    agent=form_16_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

property_deed_runner = Runner(
    agent=property_deed_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

payslip_runner = Runner(
    agent=payslip_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

document_identification_runner= Runner(
    agent=document_identification_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

test_data = [
    {
        "path" : Path("./user_uploads/property_deed.pdf"),
        "mime_type" : "application/pdf"
    },
    {
        "path" : Path("./user_uploads/form_16.pdf"),
        "mime_type" : "application/pdf"
    },
    {
        "path" : Path("./user_uploads/aadhar.png"),
        "mime_type" : "image/png"
    },
    {
        "path": Path("./user_uploads/payslip.pdf"),
        "mime_type": "application/pdf"
    }
]

for data in test_data:

    doc_path = data['path']
    doc_mime_type = data['mime_type']

    with open(doc_path, 'rb') as f:
        doc_data = f.read()

    r = run_query_with_file_data(
        query="What document is this?",
        doc_data=doc_data,
        doc_mime_type=doc_mime_type,
        runner_instance=document_identification_runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    response = json.loads(r)
    print(r)

    if response['document_type'] == 'aadhar_card':
        r = run_query_with_file_data(
            query="What are the fields in the aadhar_card",
            doc_data=doc_data,
            doc_mime_type=doc_mime_type,
            runner_instance=aadhar_runner,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
    elif response['document_type'] == 'form_16':
        r = run_query_with_file_data(
            query="What is the fields in the form 16 document?",
            doc_data=doc_data,
            doc_mime_type=doc_mime_type,
            runner_instance=form_16_runner,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
    elif response['document_type'] == 'property_sale_deed':
        r = run_query_with_file_data(
            query="What is the fields in the Property Sale Deed?",
            doc_data=doc_data,
            doc_mime_type=doc_mime_type,
            runner_instance=property_deed_runner,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
    elif response['document_type'] == 'salary_slip':
        r = run_query_with_file_data(
            query="What is the fields in the Salary Slip?",
            doc_data=doc_data,
            doc_mime_type=doc_mime_type,
            runner_instance=payslip_runner,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
    
    print(r)