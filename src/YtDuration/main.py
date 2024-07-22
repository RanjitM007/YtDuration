import requests
from bs4 import BeautifulSoup
import re

def YtDuration(video_url: str):
    """
    Get the duration of a YouTube video without using the YouTube Data API.
    
    Args:
        video_url (str): The URL of the YouTube video.
        
    Returns:
        str: The duration of the video in HH:MM:SS format.
        
    Raises:
        ValueError: If the URL is invalid, the page cannot be retrieved, or the duration cannot be found.
    """
    
    def get_youtube_video_duration(video_url):
        """
        Extracts the duration of the YouTube video from the provided URL.
        
        Args:
            video_url (str): The URL of the YouTube video.
        
        Returns:
            str: The duration of the video in HH:MM:SS format.
            
        Raises:
            ValueError: If the URL is invalid, the page cannot be retrieved, or the duration cannot be found.
        """
        # Validate the URL
        if not re.match(r'https?://(www\.)?youtube\.com/watch\?v=', video_url):
            raise ValueError("Invalid YouTube URL")

        # Send a request to the YouTube video page
        response = requests.get(video_url)
        if response.status_code != 200:
            raise ValueError("Failed to retrieve the YouTube page")

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script tag containing the video duration
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'approxDurationMs' in script.string:
                # Extract the duration in milliseconds
                duration_match = re.search(r'"approxDurationMs":"(\d+)"', script.string)
                if duration_match:
                    duration_ms = int(duration_match.group(1))
                    duration_seconds = duration_ms // 1000
                    return seconds_to_hms(duration_seconds)
        
        raise ValueError("Duration not found")

    def seconds_to_hms(seconds):
        """
        Converts seconds to a HH:MM:SS formatted string.
        
        Args:
            seconds (int): The duration in seconds.
        
        Returns:
            str: The duration in HH:MM:SS format.
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # Try to get the duration of the video and handle any errors
    try:
        duration = get_youtube_video_duration(video_url)
        print("Video Duration:", duration)
    except ValueError as e:
        print("Error:", e)
        duration = None
    
    return duration


