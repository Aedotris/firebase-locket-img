from flask import Flask, request, jsonify
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

@app.route('/upload', methods=['POST'])
def upload_video():
    data = request.json
    
    email = data.get('email')
    password = data.get('password')
    filename = data.get('video_file_path')
    image_path = data.get('thumbnail_image_path')
    caption = data.get('caption')

    # Get login details
    login_response = login(email, password)
    localId = login_response.get('localId')
    idToken = login_response.get('idToken')

    if not localId or not idToken:
        return jsonify({"error": "Failed to login"}), 401

    thumbnail_url = upload_image(image_path, email, password)

    if not thumbnail_url:
        return jsonify({"error": "Failed to upload image"}), 400

    file_extension = filename.split('.')[-1]
    namevideo = generate_random_string() + '.' + file_extension
    videosize = os.path.getsize(filename)

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

    # Data for the initial request
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

    # Read the file data
    with open(filename, 'rb') as f:
        data = f.read()

    # Upload the file
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
    "thumbnail_url": thumbnail_url,
    "md5": "6eec6f8302ff9a797825fe0eafc41ce0",
    "video_url": final_url,
    "analytics": {
      "platform": "ios",
      "google_analytics": {
        "app_instance_id": "6F477E6838D548B882635981F09BB35F"
      },
      "amplitude": {
        "device_id": "F12C84B5-E33B-4632-8F14-F3C0A0E47A08",
        "session_id": {
          "value": "1720293349010",
          "@type": "type.googleapis.com/google.protobuf.Int64Value"
        }
      }
    },
    "sent_to_all": True,
    "caption": caption,
    "overlays": [
      {
        "data": {
          "background": {
            "material_blur": "ultra_thin",
            "colors": []
          },
          "text_color": "#FFFFFFE6",
          "type": "standard",
          "max_lines": {
            "value": "4",
            "@type": "type.googleapis.com/google.protobuf.Int64Value"
          },
          "text": caption
        },
        "alt_text": caption,
        "overlay_id": "caption:standard",
        "overlay_type": "caption"
      }
    ]
  }
}

    # Headers for the postMomentV2 API
    headers = {
        'Authorization': f'Bearer {idToken}',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18'
    }

    # Post to the API
    api_url = f'https://api.locketcamera.com/postMomentV2'
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 200:
        return jsonify({"message": "Video uploaded successfully!"}), 200
    else:
        return jsonify({"error": "Failed to post moment"}), 500

if __name__ == '__main__':
    app.run(debug=True)
