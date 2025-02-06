import os
import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import requests
import google.generativeai as genai

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Load client secrets file, put the path of your file
    client_secrets_file = "client.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_local_server()

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    return youtube

def generate_tags_with_genai(text):
    # Configure GenAI
    genai.configure(api_key="AIzaSyA3YGSeFftJl7FlgYSCs3GWYq2X_SuIDyY")
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate content
    response = model.generate_content(text)
    
    # Extract tags from the response
    tags = response.text.split()  # Assuming tags are space-separated
    print(tags)
    return tags

def upload_video(youtube, tags):
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": "Erbebeğe tten giriş",
            "description": "This is the most awesome description ever",
            "tags": tags
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    # Upload the video (assuming you have a video file path)
    media_file = "1.mp4"
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file)
    )
    response = request.execute()
    print(f"Video uploaded: {response}")

if __name__ == "__main__":
    # Authenticate YouTube
    youtube = authenticate_youtube()

    # Example text to generate tags
    example_text = "Create Trend Youtube Shorts tag for reddit stories just write the tags without '#'"

    # Generate tags using GenAI API
    tags = generate_tags_with_genai(example_text)

    # Upload video to YouTube with generated tags
    upload_video(youtube, tags)