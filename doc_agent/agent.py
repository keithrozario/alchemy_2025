from google.adk.agents import LlmAgent
from doc_agent.tools import doc_tools

MODEL_NAME = "gemini-2.0-flash"


aadhar_agent = LlmAgent(
    model=MODEL_NAME,
    name="aadhar_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the first name, last name and address from an aadhar card
    Here is the document:
    """,
    output_schema=doc_tools.DocumentData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

form_16_agent = LlmAgent(
    model=MODEL_NAME,
    name="form_16_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a form 16 income tax form:
    1. First Name of Employee
    2. Last Name of Employee
    3. Address of Employee
    4. Gross Salary of Employee
    5. The Assessment year of the document
    Here is the document:
    """,
    output_schema=doc_tools.TaxData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)


property_deed_agent = LlmAgent(
    model=MODEL_NAME,
    name="property_deed_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a deed of sale concerning a property:
    1. First Name of Buyer
    2. Last Name of Buyer
    3. Current Residential address of the buyer
    4. The price of the property
    5. The address of the property being sold
    Here is the document:
    """,
    output_schema=doc_tools.PropertyData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

payslip_agent = LlmAgent(
    model=MODEL_NAME,
    name="payslip_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a payslip for an employee:
    1. First Name of Employee
    2. Last Name of Employee
    3. Address of Employee (use n.a. if the payslip does not contain address)
    4. Total pay for the month
    5. Date of the pay
    Here is the document:
    """,
    output_schema=doc_tools.PaySlipData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)



document_identification_agent = LlmAgent(
    model=MODEL_NAME,
    name="document_agent",
    description="Identifies the type of document",
    instruction="""
    You are customer service agent in a bank.
    Your task is to identify if the document is one of the following:

    1. Aadhar Card
    2. Form 16
    3. Salary Slip
    4. Property Sale Deed
    5. Bank Statement

    If you're unable to identify the document, of if the document isn't one listed above reply with 'unknown_document'

    """,
    output_schema=doc_tools.DocumentType,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)