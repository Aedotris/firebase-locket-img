from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import os
import random
import string
import json

app = Flask(__name__)

def generate_random_string(length=12):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

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

def upload_image(image_path, email, password):
    url = 'https://upanhfirebase.vercel.app/'
    files = {'file': open(image_path, 'rb')}
    data = {'email': email, 'password': password}
    
    response = requests.post(url, data=data, files=files)
    
    response_text = response.text
    if "Image link:" in response_text:
        start_index = response_text.find("Image link: ") + len("Image link: ")
        end_index = response_text.find("\n", start_index)
        if end_index == -1:
            end_index = len(response_text)
        image_url = response_text[start_index:end_index].strip()
        return image_url
    else:
        return None
@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    data = request.json
    
    email = data.get('email')
    password = data.get('password')
    filename = data.get('video_file_path')
    image_path = data.get('thumbnail_image_path')
    
    # Get login details
    login_response = login(email, password)
    localId = login_response.get('localId')
    idToken = login_response.get('idToken')

    if not localId or not idToken:
        return jsonify({"error": "Failed to login"}), 401

    # Upload an image and get the thumbnail URL
    thumbnail_url = upload_image(image_path, email, password)

    if not thumbnail_url:
        return jsonify({"error": "Failed to upload image"}), 400

    # File details
    file_extension = filename.split('.')[-1]
    namevideo = generate_random_string() + '.' + file_extension
    videosize = os.path.getsize(filename)

    # Initial headers for starting the resumable upload
    head = {
        'content-type': 'application/json; charset=UTF-8',
        'authorization': f'Firebase {idToken}',
        'x-goog-upload-protocol': 'resumable',
        'accept': '*/*',
        'x-goog-upload-command': 'start',
        'x-goog-upload-content-length': f'{videosize}',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'x-firebase-storage-version': 'ios/10.23.1',
        'user-agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18',
        'x-goog-upload-content-type': 'video/mp4',
        'x-firebase-gmpid': '1:641029076083:ios:cc8eb46290d69b234fa606'
    }

    data = json.dumps({
        "name": f"users/{localId}/moments/videos/{namevideo}",
        "contentType": "video/mp4",
        "bucket": "",
        "metadata": {
            "creator": localId,
            "visibility": "private"
        }
    })

    url = f'https://firebasestorage.googleapis.com/v0/b/locket-video/o/users%2F{localId}%2Fmoments%2Fvideos%2F{namevideo}?uploadType=resumable&name=users%2F{localId}%2Fmoments%2Fvideos%2F{namevideo}'

    res = requests.post(url, headers=head, data=data)
    upload_url = res.headers.get('X-Goog-Upload-URL')

    if not upload_url:
        return jsonify({"error": "Failed to start upload"}), 400

    head = {
        'content-type': 'application/octet-stream',
        'x-goog-upload-protocol': 'resumable',
        'x-goog-upload-offset': '0',
        'x-goog-upload-command': 'upload, finalize',
        'upload-incomplete': '?0',
        'upload-draft-interop-version': '3',
        'user-agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18'
    }

    with open(filename, 'rb') as f:
        data = f.read()

    res = requests.put(upload_url, headers=head, data=data)

    head = {
        'content-type': 'application/json; charset=UTF-8',
        'authorization': f'Firebase {idToken}',
        'accept': '*/*',
        'x-firebase-storage-version': 'ios/10.23.1',
        'user-agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    # Get the download token
    url = f'https://firebasestorage.googleapis.com/v0/b/locket-video/o/users%2F{localId}%2Fmoments%2Fvideos%2F{namevideo}'
    res = requests.get(url, headers=head)
    response_data = res.json()
    download_tokens = response_data.get("downloadTokens")

    if not download_tokens:
        return jsonify({"error": "Failed to retrieve download token"}), 400

    # Final URL
    final_url = f'https://firebasestorage.googleapis.com/v0/b/locket-video/o/users%2F{localId}%2Fmoments%2Fvideos%2F{namevideo}?alt=media&token={download_tokens}'

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
            "thumbnail_url": thumbnail_url,
            "video_url": final_url,
            "caption": "i love meo beo",
            "sent_to_all": True,
            "md5": "e9cc3f8c9b0c5d049dd8ebc79144a237",
        }
    }

    headers = {
        'Authorization': f'Bearer {idToken}',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18'
    }

    api_url = f'https://api.locketcamera.com/postMomentV2'
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 200:
        return jsonify({"message": "Video uploaded successfully!"}), 200
    else:
        return jsonify({"error": "Failed to post moment"}), 500

if __name__ == '__main__':
    app.run(debug=True)
