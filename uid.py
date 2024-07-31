import requests
import os
import random
import string
import json

# Function to generate a random string
def generate_random_string(length=12):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Login function to get localId and idToken
def login(email, password):
    url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCQngaaXQIfJaH0aS2l7REgIjD7nL431So'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en',
        'Content-Type': 'application/json',
        'Host': 'www.googleapis.com',
        'X-Ios-Bundle-Identifier': 'com.locket.Locket'
    }
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Prompt user for input file, email, and password
filename = input("Enter the path to the image file: ")
email = input("Enter your email: ")
password = input("Enter your password: ")

# Get login details
login_response = login(email, password)
localId = login_response['localId']
idToken = login_response['idToken']

# File details
file_extension = filename.split('.')[-1]
nameimg = generate_random_string() + '.' + file_extension
imagesize = os.path.getsize(filename)

# Initial headers for starting the resumable upload
head = {
    'content-type': 'application/json; charset=UTF-8',
    'authorization': f'Bearer {idToken}',
    'x-goog-upload-protocol': 'resumable',
    'accept': '*/*',
    'x-goog-upload-command': 'start',
    'x-goog-upload-content-length': f'{imagesize}',
    'accept-language': 'vi-VN,vi;q=0.9',
    'x-firebase-storage-version': 'ios/10.13.0',
    'user-agent': 'com.locket.Locket/1.43.1 iPhone/17.3 hw/iPhone15_3 (GTMSUF/1)',
    'x-goog-upload-content-type': 'image/webp',
    'x-firebase-gmpid': '1:641029076083:ios:cc8eb46290d69b234fa606'
}

# Data for the initial request
data = json.dumps({
    "name": f"users/{localId}/moments/thumbnails/{nameimg}",
    "contentType": "image/*",
    "bucket": "",
    "metadata": {
        "creator": localId,
        "visibility": "private"
    }
})

# URL for the initial request
url = f'https://firebasestorage.googleapis.com/v0/b/locket-img/o/users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}?uploadType=resumable&name=users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}'

# Start the resumable upload
res = requests.post(url, headers=head, data=data)
upload_url = res.headers['X-Goog-Upload-URL']

# Headers for uploading the file
head = {
    'content-type': 'application/octet-stream',
    'x-goog-upload-protocol': 'resumable',
    'x-goog-upload-offset': '0',
    'x-goog-upload-command': 'upload, finalize',
    'upload-incomplete': '?0',
    'upload-draft-interop-version': '3',
    'user-agent': 'com.locket.Locket/1.43.1 iPhone/17.3 hw/iPhone15_3 (GTMSUF/1)'
}

# Read the file data
with open(filename, 'rb') as f:
    data = f.read()

# Upload the file
res = requests.put(upload_url, headers=head, data=data)

# Headers for retrieving the download token
head = {
    'content-type': 'application/json; charset=UTF-8',
    'authorization': f'Bearer {idToken}',
    'accept': '*/*',
    'x-firebase-storage-version': 'ios/10.13.0',
    'user-agent': 'com.locket.Locket/1.43.1 iPhone/17.3 hw/iPhone15_3 (GTMSUF/1)',
    'accept-language': 'vi-VN,vi;q=0.9'
}

# Get the download token
url = f'https://firebasestorage.googleapis.com/v0/b/locket-img/o/users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}'
res = requests.get(url, headers=head)
response_data = res.json()
download_tokens = response_data.get("downloadTokens")

# Print the final URL
final_url = f'https://firebasestorage.googleapis.com/v0/b/locket-img/o/users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}?alt=media&token={download_tokens}'
print(final_url)

# Prepare the payload for the postMomentV2 API
payload = {
    "data": {
        "analytics": {
            "amplitude": {
                "device_id": "80BCD363-8EEF-489E-8390-1EA07C6C793A",
                "session_id": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1722330999759"
                }
            },
            "experiments": {
                "flag_4": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "43"
                },
                "flag_10": {
                    "value": "505",
                    "@type": "type.googleapis.com/google.protobuf.Int64Value"
                },
                "flag_22": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203"
                },
                "flag_23": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "400"
                },
                "flag_19": {
                    "value": "51",
                    "@type": "type.googleapis.com/google.protobuf.Int64Value"
                },
                "flag_18": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203"
                },
                "flag_16": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "303"
                },
                "flag_15": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501"
                },
                "flag_14": {
                    "value": "500",
                    "@type": "type.googleapis.com/google.protobuf.Int64Value"
                },
                "flag_25": {
                    "value": "23",
                    "@type": "type.googleapis.com/google.protobuf.Int64Value"
                }
            },
            "google_analytics": {
                "app_instance_id": "3D214A6F31014DA2AF41518404480945"
            },
            "platform": "ios"
        },
        "thumbnail_url": final_url,
        "caption": "cmm",
        "sent_to_all": True,
        "md5": "e9cc3f8c9b0c5d049dd8ebc79144a237",
    }
}

# Headers for the postMomentV2 API
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Authorization': f'Bearer {idToken}',
    'Connection': 'keep-alive',
    'content-type': 'application/json',
    'user-agent': 'com.locket.Locket/1.82.0 iPhone/18.0 hw/iPhone12_1',
    'baggage': 'sentry-environment=production,sentry-public_key=78fa64317f434fd89d9cc728dd168f50,sentry-release=com.locket.Locket@1.82.0+3,sentry-trace_id=01d4ec6852fc4cc18bf110230a45599a',
    'host': 'api.locketcamera.com',
    'accept-encoding': 'gzip, deflate, br',
    'content-length': str(len(json.dumps(payload)))
}

# URL for the postMomentV2 API
url = 'https://api.locketcamera.com/postMomentV2'

# Send the request to the postMomentV2 API
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response
print(response.status_code)
print(response.json())
