import requests
import json

def submit_form_with_files():
    """
    Creates dummy files, prepares form data and files, sends a POST request,
    and cleans up the files.
    """

    # --- 2. Define the endpoint URL and form data ---

    url = "https://alchemy-backend-v2-209692124655.us-central1.run.app/submit"
    url = "http://localhost:8000/submit"

    form_data = {
        "full_name": "John Doe",
        "loan_type": "Personal Loan",
        "aadhar_number": "123456789012",
        "pan_number": "ABCDE1234F",
        "loan_tenure": "12 months",
        "loan_amount": "100000",
        "type_of_property": "House",
    }

    # --- 3. Prepare the files for upload ---
    # To send multiple files for a single form field, create a list of tuples.
    # Each tuple is in the format: ('field_name', (filename, file_object, content_type))
    files = ["./user_uploads/Pan.png"]
    files_to_upload = [
        ("files", (filename, open(filename, "rb"), "image/png"))
        for filename in files
    ]

    print(f"Sending POST request to {url}...")
    response = requests.post(url, data=form_data, files=files_to_upload)
    pretty_json_string = json.dumps(response.json(), indent=4)
    print(pretty_json_string)


if __name__ == "__main__":                       
    submit_form_with_files()

