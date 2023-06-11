# MyTube
MyTube is a web application that allows users to save YouTube playlists and watch videos from their playlists in one convinient place. This README file provides an overview of the project and guides users on how to set up and use the application.

## Demo
You can watch a demo of the MyTube project on [YouTube](https://youtu.be/cl2S9rl2kGs).

## Features

- User Registration: Users can create an account to access the features of the website.
- Playlist Management: Users can create new playlists, view their existing playlists, and remove playlists.
- YouTube Playlist Import: Users can import YouTube playlists by providing the playlist URL.
- Video Playback: Users can watch videos from their playlists.
- Account Settings: Users can change their username and password.

## Technologies Used

The MyTube web application is built using the following technologies:

- Python: Programming language used for the backend development.
- Flask: Web framework used for building the application.
- SQLite: Database management system used to store user information, playlists, and videos.
- HTML/CSS: Frontend languages used for designing and styling the web pages.
- JavaScript: Programming language used for client-side interactions.
- PyTube: Python library used for parsing YouTube URLs and retrieving video information.
- Flask-Session: Flask extension used for managing user sessions.

## Installation

To run the MyTube web application on your local machine, follow these steps:

1. Navigate to the project directory: `cd mytube`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `flask run`
4. Open your web browser and visit `http://localhost:5000` to access the MyTube application.

## Usage

1. Register a new account or log in with your existing account.
2. On the homepage, you can view your existing playlists and create new playlists.
3. To import a YouTube playlist, provide the playlist URL and a title for the playlist. Click on the submit button.
4. You can watch videos from your playlists by clicking on the playlist and navigating to the playlist page.
5. In the account settings, you can change your username and password.
6. Log out of your account by clicking on the "Logout" button.
