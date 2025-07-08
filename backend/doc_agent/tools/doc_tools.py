from enum import Enum
from pydantic import BaseModel


class AllowedDocuments(str, Enum):
    SALARY_SLIP = "salary_slip"
    PROPERTY_SALE_DEED = "property_sale_deed"
    AADHAR_CARD = "aadhar_card"
    BANK_STATEMENT = "bank_statement"
    FORM_16 = "form_16"
    PAN_CARD = "pan_card"
    UNKNOWN_DOCUMENT = "unknown_document"


class DocumentType(BaseModel):
    document_type: AllowedDocuments
