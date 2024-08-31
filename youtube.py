import os
from googleapiclient.discovery import build
import json

# Use the API key provided
API_KEY = "AIzaSyD581ejlgEVFXDQArw8v13eybZvXtkJ39A"

# YouTube channel ID for @audiolibrary_
CHANNEL_ID = "UCht8qITGkBvXKsR1Byln-wA"

def get_youtube_service():
    return build('youtube', 'v3', developerKey=API_KEY)

def get_channel_videos(youtube, channel_id, max_results=100):
    videos = []

    # First, get the channel's uploaded videos playlist ID
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Now, get the videos from this playlist
    next_page_token = None
    while len(videos) < max_results:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=min(50, max_results - len(videos)),
            pageToken=next_page_token
        ).execute()

        for item in playlist_response['items']:
            video = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'video_id': item['snippet']['resourceId']['videoId'],
                'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
            }
            videos.append(video)

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token or len(videos) >= max_results:
            break

    return videos[:max_results]

def main():
    youtube = get_youtube_service()
    videos = get_channel_videos(youtube, CHANNEL_ID, max_results=100)

    # Save videos to a JSON file
    with open("youtube_audiolibrary_videos.json", "w", encoding='utf-8') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)

    print(f"Fetched {len(videos)} videos from the YouTube Audio Library channel")
    
    # Print the first 5 video URLs as an example
    for video in videos[:5]:
        print(f"Title: {video['title']}")
        print(f"URL: {video['url']}")
        print("---")

if __name__ == "__main__":
    main()