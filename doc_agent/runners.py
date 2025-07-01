from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

import doc_agent.agents as agents

MODEL_NAME = "gemini-2.0-flash"
APP_NAME = "alchemy12"

# Creates one global session service for all runners
session_service = InMemorySessionService()

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
