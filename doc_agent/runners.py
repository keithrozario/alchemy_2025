import json
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

import doc_agent.agents as agents
from doc_agent.helper_functions import run_query_with_file_data

MODEL_NAME = "gemini-2.0-flash"
APP_NAME = "alchemy_team_12"
USER_ID = "test_user"
SESSION_ID = uuid.uuid4().hex

### Since all users are anonymous, we create a single session for use
### Since we do not need to save the sessions, we use an InMemorySessionService
session_service = InMemorySessionService()
session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

aadhar_runner = Runner(
    agent=agents.aadhar_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
pan_card_runner = Runner(
    agent=agents.pan_card_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

form_16_runner = Runner(
    agent=agents.form_16_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

property_deed_runner = Runner(
    agent=agents.property_deed_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

payslip_runner = Runner(
    agent=agents.payslip_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

document_identification_runner = Runner(
    agent=agents.document_identification_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

bank_statement_runner = Runner(
    agent=agents.bank_statement_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
