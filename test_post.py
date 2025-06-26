import requests
import json

def submit_form_with_files():
    """
    Creates dummy files, prepares form data and files, sends a POST request,
    and cleans up the files.
    """

    # --- 2. Define the endpoint URL and form data ---
    url = "http://127.0.0.1:8000/submit"
    form_data = {
        "first_name": "Rahul",
        "last_name": "Sharma",
        "address": "1600 Pennslyvania Avenue",
    }

    # --- 3. Prepare the files for upload ---
    # To send multiple files for a single form field, create a list of tuples.
    # Each tuple is in the format: ('field_name', (filename, file_object, content_type))
    files = ["./user_uploads/Pan.png"]
    files_to_upload = [
        ("files", (filename, open(filename, "rb"), "image/png"))
        for filename in files
    ]

    try:
        # --- 4. Send the POST request ---
        print(f"Sending POST request to {url}...")
        response = requests.post(url, data=form_data, files=files_to_upload)
        response.raise_for_status()  # Raise an exception for bad status codes

        print("Request successful!")
        pretty_json_string = json.dumps(response.json(), indent=4)
        print(pretty_json_string)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    finally:
        # --- 5. Clean up: close files and remove them ---
        for _, file_tuple in files_to_upload:
            file_tuple[1].close()
        print("\nCleaned up dummy files.")

if __name__ == "__main__":
    submit_form_with_files()

