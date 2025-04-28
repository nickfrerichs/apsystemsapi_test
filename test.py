import hashlib
import hmac
import base64
import uuid
import time
import requests,urllib
import config

# Replace these with your actual API details
APP_ID = config.app_id
APP_SECRET = config.secret
API_BASE = "https://api.apsystemsema.com:9282"
REQUEST_PATH = "/user/api/v2/systems/details/"+config.sid
REQUEST_PATH = "/user/api/v2/systems/inverters/"+config.sid
API_URL = API_BASE+REQUEST_PATH
HTTP_METHOD = "GET"  # or "POST", "DELETE", depending on the API call
SIGNATURE_METHOD = "HmacSHA256"  # or "HmacSHA1"

# Generate the required headers and signature
def generate_signature():
   # timestamp = str(int(time.time()))
    timestamp = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4()).replace("-", "")
    
    path_part = REQUEST_PATH.rsplit("/",1)[1]
    # Build the string to sign
    string_to_sign = f"{timestamp}/{nonce}/{APP_ID}/{path_part}/{HTTP_METHOD}/{SIGNATURE_METHOD}"
    
    # Create the signature using HMAC with SHA256 or SHA1
    if SIGNATURE_METHOD == "HmacSHA256":
        signature = hmac.new(APP_SECRET.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    elif SIGNATURE_METHOD == "HmacSHA1":
        signature = hmac.new(APP_SECRET.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha1).digest()
    else:
        raise ValueError("Unsupported signature method")

    # Base64 encode the signature
    return base64.b64encode(signature).decode("utf-8"), timestamp, nonce

# Make the API request with the required headers
def make_api_request():
    signature, timestamp, nonce = generate_signature()

    headers = {
        "X-CA-AppId": APP_ID,
        "X-CA-Timestamp": timestamp,
        "X-CA-Nonce": nonce,
        "X-CA-Signature-Method": SIGNATURE_METHOD,
        "X-CA-Signature": signature
    }

    # Send the request
    response = requests.get(API_URL, headers=headers)
    
    # Handle response
    if response.status_code == 200:
        print("Request successful:", response.json())
    else:
        print(f"Request failed with status code {response.status_code}:", response.text)

# Run the request
make_api_request()
