from typing import List, Any, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from enum import Enum
from decimal import Decimal
from datetime import date

class AllowedDocuments(str, Enum):
    SALARY_SLIP = "salary_slip"
    PROPERTY_SALE_DEED = "property_sale_deed"
    AADHAR_CARD = "aadhar_card"
    BANK_STATEMENT = "bank_statement"
    FORM_16 = "form_16"
    UNKNOWN_DOCUMENT = "unknown_document"

class DocumentType(BaseModel):
    document_type: AllowedDocuments

class DocumentData(BaseModel):
    first_name: str = Field(description="The First Name of the main person in the document")
    last_name: str = Field(description="The Last Name of the main person in the document")
    address: str = Field(description="The address in the document")
    document_type: AllowedDocuments

class TaxData(BaseModel):
    first_name: str = Field(description="The First Name of the employee in the document")
    last_name: str = Field(description="The Last Name of the employee in the document")
    address: str = Field(description="The Address of the employee in the document")
    gross_salary: Decimal = Field(description="The Gross Salary of the employee in the document", decimal_places=2)
    assessment_year: int = Field(description="The Year of Assessment in the document in YYYY format. e.g. 2025")
    document_type: AllowedDocuments

class PropertyData(BaseModel):
    first_name: str = Field(description="The First Name of the buyer of the property")
    last_name: str = Field(description="The Last Name of the buyer of the document")
    address: str = Field(description="The current residential Address of the buyer in the document")
    property_price: Decimal= Field(description="The price of the property in the document", decimal_places=2)
    property_address: str = Field(description="The address of the property being sold in the document")
    document_type: AllowedDocuments

class PaySlipData(BaseModel):
    first_name: str = Field(description="The First Name of the employee in the document")
    last_name: str = Field(description="The Last Name of the employee in the document")
    address: str = Field(description="The Address of the employee in the document")
    total_salary: Decimal = Field(description="Total salary for the month in the payslip", decimal_places=2)
    date_of_pay: date = Field(description="The date of the pay in the payslip")
    document_type: AllowedDocuments

class BankStatementData(BaseModel):
    name: str = Field(description="The Name of the person in the bank statement")
    start_date: date = Field(description="The start date of the bank statement")
    end_date: date = Field(description="The end date of the bank statement")
    document_type: AllowedDocuments