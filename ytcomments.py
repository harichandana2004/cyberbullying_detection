import os
import pandas as pd
from googleapiclient.discovery import build

def youtube_authenticate(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def get_video_comments(youtube, video_id):
    comments = []
    video_comments = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100  
    ).execute()

    while video_comments:
        for item in video_comments['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in video_comments:
            video_comments = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=video_comments['nextPageToken']  
            ).execute()
        else:
            break

    return comments

def save_comments_to_csv(comments, filename):
    df = pd.DataFrame(comments, columns=["Comment"])
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Saved {len(comments)} comments to {filename}")

if __name__ == "__main__":

    api_key = "AIzaSyCozCP-mBLrb5bZ126LLx-E7yGAyotp_hE"

    video_id = "qqG96G8YdcE" 
    
    youtube = youtube_authenticate(api_key)
   
    comments = get_video_comments(youtube, video_id)

    if comments:
        save_comments_to_csv(comments, "yt_comments1.csv")
    else:
        print("No comments found.")
