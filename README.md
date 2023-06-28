**YouTube-Data-Harvesting-and-Warehousing-using-SQL-MongoDB-and-Streamlit**

**Problem Statement**
The task is to build a Streamlit app that permits users to analyze data from multiple YouTube channels. Users can input a YouTube channel ID to access data like channel information, video details, and user engagement. The app should facilitate storing the data in a MongoDB database and allow users to collect data from up to 10 different channels. Additionally, it should offer the capability to migrate selected channel data from the data lake to a SQL database for further analysis. The app should enable searching and retrieval of data from the SQL database, including advanced options like joining tables for comprehensive channel information.



**Technology Stack Used**
Python
MySQL
MongoDB
Google Client Library


****Approach: ****
Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.
Connect to the YouTube API: You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.
Store data in a MongoDB data lake: Once you retrieve the data from the YouTube API, you can store it in a MongoDB data lake. MongoDB is a great choice for a data lake because it can handle unstructured and semi-structured data easily.
Migrate data to a SQL data warehouse: After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQL database such as MySQL or PostgreSQL for this.
Query the SQL data warehouse: You can use SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input. You can use a Python SQL library such as SQLAlchemy to interact with the SQL database.
Display data in the Streamlit app: Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.
Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing it in a MongoDB data lake, migrating it to a SQL data warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.



**SQL Query Output need to displayed as table in Streamlit Application:**
1) What are the names of all the videos and their corresponding channels?
2)Which channels have the most number of videos, and how many videos do they have?
3)What are the top 10 most viewed videos and their respective channels?
4)How many comments were made on each video, and what are their corresponding video names?
5)Which videos have the highest number of likes, and what are their corresponding channel names?
6)What is the total number of likes and dislikes for each video, and what are their corresponding video names?
7)What is the total number of views for each channel, and what are their corresponding channel names?
8)What are the names of all the channels that have published videos in the year 2022?
9)What is the average duration of all videos in each channel, and what are their corresponding channel names?
10Which videos have the highest number of comments, and what are their corresponding channel names?
   
**Results: **
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a MongoDB database, migrates it to a SQL data warehouse, and enables users to search for channel details and join tables to view data in the Streamlit app.
