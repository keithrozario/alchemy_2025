# To Deploy

    export PROJECT_ID="project-alchemy-team12"
    gcloud config set project $PROJECT_ID

    gcloud iam service-accounts create "web-backend-sa" \
    --description="Web Backend Service Account" \
    --display-name="Web Backend"

    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:web-backend-sa@$PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/run.invoker

    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:web-backend-sa@$PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/storage.objectCreator

    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:web-backend-sa@$PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/aiplatform.user

    gcloud run deploy alchemy-backend-v3 --source . \
    --region us-central1 \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --service-account web-backend-sa@$PROJECT_ID.iam.gserviceaccount.com  \
    --min 1 \
    --memory 2Gi \
    --cpu 1

# Sample Output

If you submit the samples, you'll get the following:

```json
{
    "form_data": {
        "full_name": "John Doe",
        "loan_type": "Personal Loan",
        "aadhar_number": "123456789012",
        "pan_number": "ABCDE1234F",
        "loan_tenure": "12 months",
        "loan_amount": "100000",
        "type_of_property": "House"
    },
    "document_data": {
        "./user_uploads/Pan.png": {
            "name": "RAHUL SHARMA",
            "date_of_birth": "15-08-1990",
            "pan": "ABCDE1234F",
            "document_type": "pan_card"
        },
        "./user_uploads/bank_statement.pdf": {
            "name": "Sri. Rahul Sharma",
            "start_date": "01-01-2025",
            "end_date": "31-05-2025",
            "opening_balance": "195000.00",
            "closing_balance": "500000.00",
            "document_type": "bank_statement"
        },
        "./user_uploads/Aadhar.png": {
            "full_name": "Rahul Sharma",
            "date_of_birth": "15/08/1990",
            "aadhar_number": "1234 5678 9012",
            "document_type": "aadhar_card"
        },
        "./user_uploads/form_16.pdf": {
            "annual_income_gross": "45,00,000.00",
            "pan": "ABCDE1234F",
            "address": "H.No. 123, ABC Apartments, Sector 10, Dwarka, New Delhi, Delhi - 110075",
            "assessment_years": "2025-2026",
            "total_tax": "11,00,611.20",
            "document_type": "form_16"
        },
        "./user_uploads/property_deed.pdf": {
            "buyer_name": "Rahul Sharma",
            "seller_name": "Sunder Lal",
            "buyer_pan": "ABCDE1234F",
            "seller_pan": null,
            "property_address": "Flat No. A-404, on the 4th Floor of the building known as \"Sunshine Apartments\", located at Sector 75, Noida, District Gautam Budh Nagar, Uttar Pradesh, PIN - 201301",
            "property_price": "20000000.00",
            "document_type": "property_sale_deed"
        },
        "./user_uploads/payslip.pdf": {
            "full_name": "Rahul Sharma",
            "employer_name": "Cymbal Corporation",
            "total_salary": "260583.00",
            "salary_month": "05-2025",
            "pan": "ABCDE1234F",
            "document_type": "salary_slip"
        }
    },
    "status": "SUCCESS",
    "messages": [
        "Form submitted successfully"
    ],
    "trxn_id": "95960a44f9c44204baf53bf587f193e1",
    "preliminary_assessment": "Some string to describe preliminary assessment"
}
```

# To run locally

As a prerequsite, set your environment variables (or .env file) to something like below:

  GOOGLE_GENAI_USE_VERTEXAI=TRUE
  GOOGLE_CLOUD_PROJECT=project-alchemy-team12
  GOOGLE_CLOUD_LOCATION=us-central1
  LOAN_GCS_BUCKET=alchemy-loan-documents-uploads
  GRPC_VERBOSITY=ERROR
  GLOG_minloglevel=2

Then run:

    $ uv venv
    $ source .venv/bin/activate
    $ uv sync --locked
    $ uv run uvicorn app:app --reload

# To test the API locally

The following script will test the api locally

    $ python3 test_api.py --env local

