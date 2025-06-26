import uuid
import json
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from doc_agent.helper_functions import run_query_with_file_data

from doc_agent.agent import aadhar_agent, form_16_agent, property_deed_agent, payslip_agent, document_identification_agent

MODEL_NAME = "gemini-2.0-flash"
APP_NAME = "alchemy_team_12"
USER_ID = "test_user"
SESSION_ID = uuid.uuid4().hex

### Since all users are anonymous, we create a single session for use
### Since we do not need to save the sessions, we use an InMemorySessionService
session_service = InMemorySessionService()
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

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





class DocumentProcessor:
    def __init__(self, app_name, user_id):
        self.session_id = uuid.uuid4().hex
        self.user_id = user_id
        self.app_name = app_name

        self.session_service = InMemorySessionService()
        self.session_service.create_session(app_name=self.app_name, user_id=self.user_id, session_id=self.session_id )

        self.aadhar_runner = Runner(
            agent=aadhar_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )

        self.form_16_runner = Runner(
            agent=form_16_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )

        self.property_deed_runner = Runner(
            agent=property_deed_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )

        self.payslip_runner = Runner(
            agent=payslip_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )

        self.document_identification_runner= Runner(
            agent=document_identification_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )
    
    def process_single_document(self, doc_data: bytes, doc_mime_type: str)->dict:
        """
        Process a single document, and returns the data fields and document types.
        Args:
            doc_data (bytes): The document in bytes format, could be png or pdf
            doc_mime_type (str): The mime type of the document
        returns:
            doc_data_fields: The document fields in json format as a dict
        """

        r = run_query_with_file_data(
                query="What document is this?",
                doc_data=doc_data,
                doc_mime_type=doc_mime_type,
                runner_instance=self.document_identification_runner,
                user_id=self.user_id,
                session_id=self.session_id,
            )
        try:
            response = json.loads(r)
        except json.JSONDecodeError:
            return {"Error": "Unable to identify document"}


        if response['document_type'] == 'aadhar_card':
            r = run_query_with_file_data(
                query="What are the fields in the aadhar_card",
                doc_data=doc_data,
                doc_mime_type=doc_mime_type,
                runner_instance=self.aadhar_runner,
                user_id=self.user_id,
                session_id=self.session_id,
            )
        elif response['document_type'] == 'form_16':
            r = run_query_with_file_data(
                query="What is the fields in the form 16 document?",
                doc_data=doc_data,
                doc_mime_type=doc_mime_type,
                runner_instance=self.form_16_runner,
                user_id=self.user_id,
                session_id=self.session_id,
            )
        elif response['document_type'] == 'property_sale_deed':
            r = run_query_with_file_data(
                query="What is the fields in the Property Sale Deed?",
                doc_data=doc_data,
                doc_mime_type=doc_mime_type,
                runner_instance=self.property_deed_runner,
                user_id=self.user_id,
                session_id=self.session_id,
            )
        elif response['document_type'] == 'salary_slip':
            r = run_query_with_file_data(
                query="What is the fields in the Salary Slip?",
                doc_data=doc_data,
                doc_mime_type=doc_mime_type,
                runner_instance=self.payslip_runner,
                user_id=self.user_id,
                session_id=self.session_id,
            )
        
        return json.loads(r)