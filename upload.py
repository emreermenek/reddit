import os
import json
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google.generativeai as genai

# API ile bağlantı kurmak için gerekli yetkilendirme
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRET_FILE = 'client.json'  # OAuth istemci dosyanızın yolu
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Yetkilendirmeyi kontrol et ve gerekiyorsa giriş yap
def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# JSON dosyasından API anahtarını oku
def load_api_key():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['genai_api_key']

# Gemini API'si ile tag oluşturma
def generate_tags():
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Write tags for your YouTube Short's channel, use trending topic tags and also add some tags about Reddit content. Just write tags and write without '#'. Do not write anything else, just write tags and the total characters will be around 100-200 characters ")
    tags = response.text.strip().split('\n')
    return tags

# Gemini API'si ile title oluşturma
def generate_title(story):
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Generate a title for a youtube shorts video which is telling this story: \n{story}\n just write one title not anyting else")
    title = response.text.strip().split('\n')
    return title

# Gemini API'si ile description oluşturma
def generate_description(story):
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Generate a description for a youtube shorts video which is telling this story: \n{story}\n just write the description not anyting else")
    description = response.text.strip().split('\n')
    return description

# Video yükleme fonksiyonu
def upload_video(file, story):
    youtube = get_authenticated_service()

    #gemini
    tags = generate_tags()
    title = generate_title(story)
    description = generate_description(story)
    # Medya dosyasını yükle
    media = MediaFileUpload(file, mimetype='video/*', resumable=True)
    
    # Video özelliklerini ayarla
    request_body = {
        'snippet': {
            'title': title[0],
            'description': description[0],
            'categoryId': 22,
            'tags': tags 
        },
        'status': {
            'privacyStatus': 'private',  # Video gizliliği: 'public', 'private', 'unlisted'
        }
    }
    
    # Video yükleme işlemi başlat
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print(f"Video uploaded: {response['id']}")

# # Örnek kullanım
# if __name__ == "__main__":
#     upload_video('1.mp4', 'Test Video', 'This is a test description')