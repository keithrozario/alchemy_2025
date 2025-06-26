# To Deploy

gcloud run deploy alchemy-backend --source . \
--region us-central1 \
--project default-krozario \
--allow-unauthenticated \
--service-account adk-cloudrun@default-krozario.iam.gserviceaccount.com \
--min 1

# Sample Output

If you submit the samples, you'll get the following:

```json
{
  "form_data": {
    "full_name": "Rahul Sharma",
    "aadhar_number": "123456789012",
    "pan_number": "ABCDE1234F",
    "loan_tenure": "120",
    "loan_amount": "1000000",
    "type_of_property": "Residential",
    "address": "1600 Pennslyvania Avenue"
  },
  "document_data": {
    "Aadhar.png": {
      "full_name": "Rahul Sharma",
      "date_of_birth": "15/08/1990",
      "aadhar_number": "1234 5678 9012",
      "document_type": "aadhar_card"
    },
    "bank_statement.pdf": {
      "name": "Sri. Rahul Sharma",
      "start_date": "01-01-2025",
      "end_date": "31-05-2025",
      "opening_balance": "195000.00",
      "closing_balance": "500000.00",
      "document_type": "bank_statement"
    },
    "form_16.pdf": {
      "annual_income_gross": "45,00,000.00",
      "pan": "ABCDE1234F",
      "address": "H.No. 123, ABC Apartments, Sector 10, Dwarka,New Delhi, Delhi - 110075",
      "assessment_years": "2025-2026",
      "total_tax": "11,00,611.20",
      "document_type": "form_16"
    },
    "Pan.png": {
      "name": "RAHUL SHARMA",
      "date_of_birth": "15-08-1990",
      "pan": "ABCDE1234F"
    },
    "payslip.pdf": {
      "full_name": "Rahul Sharma",
      "employer_name": "Cymbal Corporation",
      "total_salary": "260583.00",
      "salary_month": "05-2025",
      "pan": "ABCDE1234F",
      "document_type": "salary_slip"
    },
    "property_deed.pdf": {
      "buyer_name": "Rahul Sharma",
      "seller_name": "Sunder Lal",
      "buyer_pan": "ABCDE1234F",
      "seller_pan": null,
      "property_address": "Flat No. A-404, on the 4th Floor of the building known as \"Sunshine Apartments\", located at Sector 75, Noida, District Gautam Budh Nagar, Uttar Pradesh, PIN - 201301",
      "property_price": "20000000.00"
    }
  }
}
```

# To run locally

    $ uv venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    $ uvicorn app:app

# To test the API locally

The following script pushes a single file to the API via HTTP

    $ python3 test_post.py

