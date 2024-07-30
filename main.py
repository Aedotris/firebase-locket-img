import pyrebase

config = {
    "apiKey": "AIzaSyCQngaaXQIfJaH0aS2l7REgIjD7nL431So",
    "authDomain": "locket-4252a.firebaseapp.com",
    "databaseURL": "locket-4252a.firebaseapp.com",
    "storageBucket": "locket-img",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def upload_file_to_firebase(file_path, user_id, token):
    storage_path = f'users/{user_id}/moments/thumbnails/{file_path.split("/")[-1]}'
    
    # Tải tệp lên Firebase Storage
    storage.child(storage_path).put(file_path, token=token)
    
    # Tạo URL công khai cho tệp đã tải lên
    image_url = storage.child(storage_path).get_url(token)
    return image_url

if __name__ == '__main__':
    file_path = '/Users/aedotris/adu/my-nextjs-app/cc.webp'
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjFkYmUwNmI1ZDdjMmE3YzA0NDU2MzA2MWZmMGZlYTM3NzQwYjg2YmMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQ2FjaGFtd3JpIOKAjyIsInBpY3R1cmUiOiJodHRwczovL2ZpcmViYXNlc3RvcmFnZS5nb29nbGVhcGlzLmNvbTo0NDMvdjAvYi9sb2NrZXQtaW1nL28vdXNlcnMlMkZQV3ZNSkNpWkFDV0ZTaERCM1F3ZENFQ2k3UTYzJTJGcHVibGljJTJGcHJvZmlsZV9waWMud2ViUD9hbHQ9bWVkaWEmdG9rZW49OWQ3NjA0NjgtYmUyMS00YjFlLWE4NmUtZmQwZDcwMDhiMmI3IiwicmV2ZW51ZUNhdEVudGl0bGVtZW50cyI6W10sImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9sb2NrZXQtNDI1MmEiLCJhdWQiOiJsb2NrZXQtNDI1MmEiLCJhdXRoX3RpbWUiOjE3MjIzNTU3NTMsInVzZXJfaWQiOiJQV3ZNSkNpWkFDV0ZTaERCM1F3ZENFQ2k3UTYzIiwic3ViIjoiUFd2TUpDaVpBQ1dGU2hEQjNRd2RDRUNpN1E2MyIsImlhdCI6MTcyMjM1NTc1MywiZXhwIjoxNzIyMzU5MzUzLCJlbWFpbCI6ImxldmluaGtoYW5nNjMxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfbnVtYmVyIjoiKzg0OTA1MjQzNDc3IiwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJsZXZpbmhraGFuZzYzMUBnbWFpbC5jb20iXSwicGhvbmUiOlsiKzg0OTA1MjQzNDc3Il19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.Yd6L7qs7qye1QyjkjZZ_1XUAhq5Py6t-caXCgWzxjAcMuowjTx34DW8XX4M8HYfVrRTHT7UQ9U-lRN-kBD_ZfPoUGf_74EZN4PzJUFt_MTe_zC2-YTIO3DqlBGJE_0-Km7wpMYdNROgrQPPbahJGPshB5lI8hiKzpnR4ZMOtgZgkOF7o7lhx1v9uXbK4wol5lU0StBFmamk3XTrZpV-jSZuGKSQbGvs2quBYUzirrna__m1Jt48anwtFYZWYysbxNm8W7j1L9bdrRNreINGZ8FuGjffahEGSlp1y9lgTZAgoIwUTHiLJOzQ4mLbmTSiG_lw3yxZ_iEYt_umME-GgUQ'  # Thay bằng token thực tế của bạn
    user_id = 'PWvMJCiZACWFShDB3QwdCECi7Q63'  

    image_url = upload_file_to_firebase(file_path, user_id, token)
    print(f'Image URL: {image_url}')
