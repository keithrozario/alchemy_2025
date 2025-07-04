import json
import click
import requests

"""
Run this file to test an api.
Specify --env variable to use different environments.

e.g. 
python test_post.py --env local
python test_post.py --env prod_pranshu

"""


def get_mime_type(file_path):
    """
    Args:
        file_path: Path of the file
    returns:
        mime_type: Mime type of the file, based on the extension of the file.
    """
    if file_path.endswith(".pdf"):
        return "application/pdf"
    elif file_path.endswith(".png"):
        return "image/png"
    elif file_path.endswith(".jpg"):
        return "image/jpeg"
    elif file_path.endswith(".jpeg"):
        return "image/jpeg"

    return "application/octet-stream"


@click.command()
@click.option("--env", default="local", type=str)
def submit_form_with_files(env: str):
    """
    Test the API by submitting 6 documents from the user_upload folder

    Args:
        env: specifies the environment, local for localhost, else will submit to the webpage.
    returns:
        response (dict): Returns the response objects from the API calls
    """

    if env == "local":
        url = "http://localhost:8000/submit"
    elif env == "prod":
        url = "https://alchemy-backend-v2-209692124655.us-central1.run.app/submit"
    elif env == "prod_v3":
        url = "https://alchemy-backend-v3-209692124655.us-central1.run.app/submit"
    elif env == "prod_pranshu":
        url = "https://alchemy-backend-v3-941915649485.us-central1.run.app/submit"
    else:
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

    # To send multiple files for a single form field, create a list of tuples.
    # Each tuple is in the format: ('field_name', (filename, file_object, content_type))
    file_paths = [
        "./user_uploads/Pan.png",
        "./user_uploads/bank_statement.pdf",
        "./user_uploads/Aadhar.png",
        "./user_uploads/form_16.pdf",
        "./user_uploads/property_deed.pdf",
        # "./user_uploads/payslip.pdf",
    ]
    files_to_upload = [
        ("files", (file_path, open(file_path, "rb"), get_mime_type(file_path)))
        for file_path in file_paths
    ]

    headers = {}
    try:
        with open("token.txt", "r") as token_file:
            token = token_file.read().strip()
            headers = {"Authorization": f"Bearer {token}"}
    except FileNotFoundError:
        print("no token file found, calling unauthenticated")

    print(f"Sending POST request to {url}...")
    response = requests.post(
        url, data=form_data, files=files_to_upload, headers=headers
    )
    try:
        pretty_json_string = json.dumps(response.json(), indent=4)
        print(pretty_json_string)
    except json.JSONDecodeError:  # usually some error that we should print to the user
        print(response.text)



if __name__ == "__main__":
    submit_form_with_files()
