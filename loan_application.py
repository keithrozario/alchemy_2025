from fastapi import Form
from pydantic import BaseModel


class LoanApplicationForm(BaseModel):
    full_name: str
    loan_type: str
    aadhar_number: str
    pan_number: str
    loan_tenure: str
    loan_amount: str
    type_of_property: str


def get_form_data(
    full_name: str = Form(...),
    loan_type: str = Form(...),
    aadhar_number: str = Form(...),
    pan_number: str = Form(...),
    loan_tenure: str = Form(...),
    loan_amount: str = Form(...),
    type_of_property: str = Form(...),
) -> LoanApplicationForm:
    return LoanApplicationForm(
        full_name=full_name,
        loan_type=loan_type,
        aadhar_number=aadhar_number,
        pan_number=pan_number,
        loan_tenure=loan_tenure,
        loan_amount=loan_amount,
        type_of_property=type_of_property,
    )
