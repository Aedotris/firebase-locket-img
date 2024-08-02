import requests
import os
import random
import string
import json
import base64
import hashlib
from moviepy.editor import VideoFileClip
import time

def generate_random_string(length=12):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def decode_base64_md5(base64_md5):
    md5_bytes = base64.b64decode(base64_md5)
    return md5_bytes.hex()

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
    login_response = login(email, password)
    localId = login_response.get('localId')
    idToken = login_response.get('idToken')

    if not localId or not idToken:
        print("Failed to login")
        return None, None

    file_extension = image_path.split('.')[-1]
    nameimg = generate_random_string() + '.' + file_extension
    imagesize = os.path.getsize(image_path)

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

    data = json.dumps({
        "name": f"users/{localId}/moments/thumbnails/{nameimg}",
        "contentType": "image/*",
        "bucket": "",
        "metadata": {
            "creator": localId,
            "visibility": "private"
        }
    })

    url = f'https://firebasestorage.googleapis.com/v0/b/locket-img/o/users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}?uploadType=resumable&name=users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}'

    res = requests.post(url, headers=head, data=data)
    upload_url = res.headers.get('X-Goog-Upload-URL')

    if not upload_url:
        print("Failed to start upload")
        return None, None

    head = {
        'content-type': 'application/octet-stream',
        'x-goog-upload-protocol': 'resumable',
        'x-goog-upload-offset': '0',
        'x-goog-upload-command': 'upload, finalize',
        'upload-incomplete': '?0',
        'upload-draft-interop-version': '3',
        'user-agent': 'com.locket.Locket/1.43.1 iPhone/17.3 hw/iPhone15_3 (GTMSUF/1)'
    }

    with open(image_path, 'rb') as f:
        data = f.read()

    # Upload the file
    res = requests.put(upload_url, headers=head, data=data)

    head = {
        'content-type': 'application/json; charset=UTF-8',
        'authorization': f'Bearer {idToken}',
        'accept': '*/*',
        'x-firebase-storage-version': 'ios/10.13.0',
        'user-agent': 'com.locket.Locket/1.43.1 iPhone/17.3 hw/iPhone15_3 (GTMSUF/1)',
        'accept-language': 'vi-VN,vi;q=0.9'
    }

    url = f'https://firebasestorage.googleapis.com/v0/b/locket-img/o/users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}'
    res = requests.get(url, headers=head)
    response_data = res.json()
    download_tokens = response_data.get("downloadTokens")
    md5_base64 = response_data.get("md5Hash")

    if not download_tokens or not md5_base64:
        print("Failed to retrieve download token or MD5 hash")
        return None, None

    md5_hex = decode_base64_md5(md5_base64)

    final_url = f'https://firebasestorage.googleapis.com/v0/b/locket-img/o/users%2F{localId}%2Fmoments%2Fthumbnails%2F{nameimg}?alt=media&token={download_tokens}'
    return final_url, md5_hex

def convert_mov_to_mp4(video_file_path):
    if video_file_path.endswith('.mov'):
        video = VideoFileClip(video_file_path)
        new_video_file_path = video_file_path.replace('.mov', '.mp4')
        video.write_videofile(new_video_file_path, codec='libx264')
        return new_video_file_path
    return video_file_path

def main():
    email = input("Enter email: ")
    password = input("Enter password: ")
    video_file_path = input("Enter video file path: ")
    thumbnail_image_path = input("Enter thumbnail image path: ")
    caption = input("Enter caption: ")

    video_file_path = convert_mov_to_mp4(video_file_path)
    
    login_response = login(email, password)
    localId = login_response.get('localId')
    idToken = login_response.get('idToken')

    if not localId or not idToken:
        print("Failed to login")
        return

    thumbnail_url, md5_hex = upload_image(thumbnail_image_path, email, password)

    if not thumbnail_url:
        print("Failed to upload image")
        return

    timestamp = int(time.time())
    namevideo = generate_random_string() + f'_{timestamp}.mp4'
    videosize = os.path.getsize(video_file_path)

    head = {
        'content-type': 'application/json; charset=UTF-8',
        'authorization': f'Bearer {idToken}',
        'x-goog-upload-protocol': 'resumable',
        'accept': '*/*',
        'x-goog-upload-command': 'start',
        'x-goog-upload-content-length': f'{videosize}',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'x-firebase-storage-version': 'ios/10.23.1',
        'user-agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18',
        'x-goog-upload-content-type': 'video/mp4'
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
        print("Failed to start upload")
        return

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
    with open(video_file_path, 'rb') as f:
        data = f.read()

    # Upload the file
    res = requests.put(upload_url, headers=head, data=data)

    head = {
        'content-type': 'application/json; charset=UTF-8',
        'authorization': f'Bearer {idToken}',
        'accept': '*/*',
        'x-firebase-storage-version': 'ios/10.23.1',
        'user-agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    url = f'https://firebasestorage.googleapis.com/v0/b/locket-video/o/users%2F{localId}%2Fmoments%2Fvideos%2F{namevideo}'
    res = requests.get(url, headers=head)
    response_data = res.json()
    download_tokens = response_data.get("downloadTokens")

    if not download_tokens:
        print("Failed to retrieve download token")
        return

    final_video_url = f'https://firebasestorage.googleapis.com/v0/b/locket-video/o/users%2F{localId}%2Fmoments%2Fvideos%2F{namevideo}?alt=media&token={download_tokens}'

    payload = {
        "data": {
            "thumbnail_url": thumbnail_url,
            "md5": md5_hex,
            "video_url": final_video_url,
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

    headers = {
        'Authorization': f'Bearer {idToken}',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'com.locket.Locket/1.79.0 iPad/17.1.2 hw/iPad13_18'
    }

    api_url = 'https://api.locketcamera.com/postMomentV2'
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Video uploaded successfully!")
    else:
        print("Failed to post moment")

if __name__ == '__main__':
    main()
