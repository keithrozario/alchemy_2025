from typing import List
from pydantic import BaseModel, Field
from enum import Enum

class AllowedDocuments(str, Enum):
    SALE_DEED = "Sale Deed"
    PROPERTY_DEED = "Property Deed"
    GOVERNMENT_ID = "Government ID"

class DocumentData(BaseModel):
    first_name: str = Field(description="The First Name of the main person in the document")
    last_name: str = Field(description="The Last Name of the main person in the document")
    address: str = Field(description="The address in the document")
    document_type: AllowedDocuments