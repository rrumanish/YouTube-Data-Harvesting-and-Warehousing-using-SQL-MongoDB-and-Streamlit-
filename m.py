
import streamlit as st
from googleapiclient.discovery import build
import pymongo
from pymongo import MongoClient
from sqlalchemy import create_engine
from bson import ObjectId
import pandas as pd
from googleapiclient.errors import HttpError

# Connect to MongoDB Atlas
atlas_username = 'rrumanish'
atlas_password = 'YO3abEvy99URfN4U'
atlas_cluster = 'ManishM'
client = MongoClient(f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}.hywezt7.mongodb.net/?retryWrites=true&w=majority")
# mongodb+srv://rrumanish:<password>@manishm.hywezt7.mongodb.net/
# mongodb+srv://rrumanish:<password>@manishm.hywezt7.mongodb.net/?retryWrites=true&w=majority

db = client['youtube_data']
collection = db['channel_data']

# Set Streamlit app title
st.title("YouTube Data Harvesting and Warehousing")

# Display input field for YouTube channel ID
channel_id = st.text_input("Enter YouTube Channel ID")

# Retrieve videos for a given YouTube channel ID
def get_channel_videos(youtube, channel_id, api_key):
    videos = []
    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        maxResults=10
    )
    response = request.execute()

    video_ids = [item['id']['videoId'] for item in response['items']]
    video_request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
    )
    video_response = video_request.execute()

    videos.extend(video_response['items'])
    return videos

def parse_duration(duration):
    duration = duration[2:]  # Remove 'PT' prefix
    hours = duration.count('H')
    minutes = duration.count('M')
    seconds = duration.count('S')

    duration_str = ''
    if hours > 0:
        duration_str += f'{hours}h '
    if minutes > 0:
        duration_str += f'{minutes}m '
    if seconds > 0:
        duration_str += f'{seconds}s'

    return duration_str.strip()


    # Initialize YouTube Data API client
youtube = build('youtube', 'v3', developerKey='AIzaSyAqbVuDwF7IWGsZv6OvJ_zZx3EdZaDi9Kg')

# Make API request to get channel data
request = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=channel_id
        )
response = request.execute()

if 'items' in response:
            channel_data = response['items'][0]
            snippet = channel_data['snippet']
            statistics = channel_data['statistics']
            content_details = channel_data.get('contentDetails', {})
            related_playlists = content_details.get('relatedPlaylists', {})

            # Extract relevant data
            data = {
                'Channel_Name': {
                    'Channel_Name': snippet.get('title', ''),
                    'Channel_Id': channel_id,
                    'Subscription_Count': int(statistics.get('subscriberCount', 0)),
                    'Channel_Views': int(statistics.get('viewCount', 0)),
                    'Channel_Description': snippet.get('description', ''),
                    'Playlist_Id': related_playlists.get('uploads', '')
                }
            }

            # Retrieve video data
            videos = get_channel_videos(youtube, channel_id, 'AIzaSyAqbVuDwF7IWGsZv6OvJ_zZx3EdZaDi9Kg')
            for video in videos:
                video_id = video['id']
                video_data = {
                    'Video_Id': video_id,
                    'Video_Name': video['snippet'].get('title', ''),
                    'Video_Description': video['snippet'].get('description', ''),
                    'Tags': video['snippet'].get('tags', []),
                    'PublishedAt': video['snippet'].get('publishedAt', ''),
                    'View_Count': int(video['statistics'].get('viewCount', 0)),
                    'Like_Count': int(video['statistics'].get('likeCount', 0)),
                    'Dislike_Count': int(video['statistics'].get('dislikeCount', 0)),
                    'Favorite_Count': int(video['statistics'].get('favoriteCount', 0)),
                    'Comment_Count': int(video['statistics'].get('commentCount', 0)),
                    'Duration': parse_duration(video['contentDetails'].get('duration', '')),
                    'Thumbnail': video['snippet'].get('thumbnails', {}).get('default', {}).get('url', ''),
                    'Caption_Status': video['snippet'].get('localized', {}).get('localized', 'Not Available'),
                    'Comments': {}
                }
                data[video_id] = video_data

# Retrieve channel data using YouTube API
if st.button("Retrieve Channel Data"):
    try:


            # Display channel data
            st.write("Channel Name:", data['Channel_Name']['Channel_Name'])
            st.write("Subscribers:", data['Channel_Name']['Subscription_Count'])
            st.write("Total Videos:", len(videos))

            # Display video data
            st.subheader("Video Data:")
            for video_id, video_data in data.items():
              if video_id != 'Channel_Name':
                st.write("Video Name:", video_data['Video_Name'])
                st.write("Video Description:", video_data['Video_Description'])
                st.write("Published At:", video_data['PublishedAt'])
                st.write("View Count:", video_data['View_Count'])
                st.write("Like Count:", video_data['Like_Count'])
                st.write("Dislike Count:", video_data['Dislike_Count'])
                st.write("Comment Count:", video_data['Comment_Count'])
                st.write("Duration:", video_data['Duration'])
                st.write("Thumbnail:", video_data['Thumbnail'])
    except Exception as e:
        st.error(f"Error retrieving channel data: {str(e)}")

# Store data in MongoDB Atlas
if st.button("Store Data in MongoDB Atlas"):
    collection.insert_one(data)
    st.success("Data stored successfully in MongoDB Atlas!")

# Retrieve data from MongoDB Atlas
if st.button("Retrieve Data from MongoDB Atlas"):
    retrieved_data = collection.find_one({'Channel_Name.Channel_Id': channel_id})
    if retrieved_data:
        st.subheader("Retrieved Data:")
        st.write("Channel Name:", retrieved_data['Channel_Name']['Channel_Name'])
        st.write("Subscribers:", retrieved_data['Channel_Name']['Subscription_Count'])
        st.write("Total Videos:", len(videos))
        for video_id, video_data in retrieved_data.items():
            if video_id != 'Channel_Name' and not isinstance(video_data, ObjectId):
                st.write("Video Name:", video_data['Video_Name'])
                st.write("Video Description:", video_data['Video_Description'])
                st.write("Published At:", video_data['PublishedAt'])
                st.write("View Count:", video_data['View_Count'])
                st.write("Like Count:", video_data['Like_Count'])
                st.write("Dislike Count:", video_data['Dislike_Count'])
                st.write("Comment Count:", video_data['Comment_Count'])
                st.write("Duration:", video_data['Duration'])
                st.write("Thumbnail:", video_data['Thumbnail'])
    else:
        st.warning("Data not found in MongoDB Atlas!")

