from google.adk.agents import LlmAgent
from doc_agent.tools import doc_tools
from pydantic import BaseModel, Field
from decimal import Decimal

MODEL_NAME = "gemini-2.0-flash"

class AadharData(BaseModel):
    full_name: str = Field(description="The Full Name of the Person")
    date_of_birth: str = Field(description="The Date of Birth of the Person")
    aadhar_number: str = Field(description="The Aadhar card number of the Person")
    document_type: doc_tools.AllowedDocuments

aadhar_agent = LlmAgent(
    model=MODEL_NAME,
    name="aadhar_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the first name, last name and address from an aadhar card

    1. The Full Name of the Person
    2. The Date of Birth of the Person
    3. The Aadhar card number of the Person
    """,
    output_schema=AadharData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

class Form16Data(BaseModel):
    annual_income_gross : Decimal = Field(description="The Gross annual income of the employee in the Form 16", decimal_places=2)
    pan: str = Field(description="The permanent account number (PAN) of the employee")
    address: str = Field(description="The Address of the employee in the document")
    assessment_years: str = Field(description="The Years of Assessment of the document in YYYY-YYYY format. e.g. 2025-2026")
    total_tax: Decimal = Field(description="The total tax paid in the assesssment year", decimal_places=2)
    document_type: doc_tools.AllowedDocuments

form_16_agent = LlmAgent(
    model=MODEL_NAME,
    name="form_16_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a form 16 income tax form:
    1. The total gross salary of the employee in the Form 16 for the assessment year
    2. The permanent account number (PAN) of the employee
    3. The Address of the employee in the document
    4. The Assessment years (plural) of the document in YYYY-YYYY format. e.g. 2025-2026. This must always be two consecutive years
    5. The total tax payable in the assessment year
    6. The full name of the employee in the form 16
    Here is the document:
    """,
    output_schema=Form16Data,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

class PropertyData(BaseModel):
    buyer_name: str= Field(description="The Full Name of the buyer of the property")
    seller_name: str = Field(description="The Full Name of the seller of the property")
    buyer_pan: str = Field(description="The PAN of the buyer of the property")
    seller_pan: str | None = Field(description="The PAN of the seller of the property")
    property_address: str = Field(description="The full address of the property being sold")
    property_price: Decimal = Field(description="The price of the property in the document", decimal_places=2)


property_deed_agent = LlmAgent(
    model=MODEL_NAME,
    name="property_deed_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a deed of sale concerning a property:
    1. The Full Name of the buyer of the property
    2. The Full Name of the seller of the property
    3. The PAN of the buyer of the property
    4. The PAN of the seller of the property (if available)
    5. The full address of the property being sold
    6. The price of the property in the document as a Decimal with 2 decimal places
    Here is the document:
    """,
    output_schema=PropertyData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

class PaySlipData(BaseModel):
    full_name: str = Field(description="The Full Name of the employee in the document")
    employer_name: str = Field(description="The name of the Employer")
    total_salary: Decimal = Field(description="Total salary for the month in the payslip", decimal_places=2)
    salary_month: str = Field(description="The month of the salary in mm-yyyy format (e.g. 01-2023)")
    pan: str = Field(description="The PAN of the employee")
    document_type: doc_tools.AllowedDocuments 

payslip_agent = LlmAgent(
    model=MODEL_NAME,
    name="payslip_agent",
    description="Extracts Data from a document",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a payslip for an employee:
    1. The Full Name of the Employee
    2. The Name of the Employer or company employing the employee
    3. THe Total Salary for the month, as a Decimal with 2 decimal places
    4. The month of the salary in mm-yyyy format (e.g. 01-2023)
    5. The PAN of the employee
    Here is the document:
    """,
    output_schema=PaySlipData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

class BankStatementData(BaseModel):
    name: str = Field(description="The Full Name of the person in the bank statement")
    start_date: str = Field(description="The start date of the bank statement in dd-mm-YYYY format")
    end_date: str = Field(description="The end date of the bank statement dd-mm-YYYY format")
    opening_balance: Decimal = Field(description="The opening balance of the bank statement", decimal_places=2)
    closing_balance: Decimal = Field(description="The closing balance of the bank statement", decimal_places=2)
    document_type: doc_tools.AllowedDocuments

bank_statement_agent = LlmAgent(
    model=MODEL_NAME,
    name="bank_statement_agent",
    description="Extracts Data from a Bank Statement",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a payslip for an employee:
    1. The Full Name of the person in the bank statement
    2. The start date of the bank statement in dd-mm-YYYY format
    3. The end date of the bank statement in dd-mm-YYYY format
    4. The opening balance of the bank statement as a Decimal with 2 decimal places
    5. The closing balance of the bank statement as a Decimal with 2 decimal places
    Here is the document:
    """,
    output_schema=BankStatementData,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)


class PanCardData(BaseModel):
    name: str = Field(description="The Full Name of the person on the PAN card")
    date_of_birth: str = Field(description="The Date of Birth on the PAN card")
    pan: str = Field(description="The PAN of the person")

pan_card_agent = LlmAgent(
    model=MODEL_NAME,
    name="pan_card_agent",
    description="Extracts Data from a Pan Card",
    instruction="""
    You are customer service agent at a bank in India.
    Your task is to extract the following fields from a PAN Card for an employee:
    1. The Full Name of the person on the PAN card
    2. The Date of Birth on the PAN card
    3. The PAN of the person
    Here is the document:
    """,
    output_schema=PanCardData,
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
    6. PAN Card (a id card issued by the income tax department for India)

    If you're unable to identify the document, of if the document isn't one listed above reply with 'unknown_document'

    """,
    output_schema=doc_tools.DocumentType,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)