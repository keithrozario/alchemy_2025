from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Annotated, Any, List

from pydantic import BaseModel, BeforeValidator, Field


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
