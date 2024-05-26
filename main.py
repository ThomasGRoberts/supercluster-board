import requests
import json
import datetime
import os

# Environment variables (set these in your GitHub Secrets)
SANITY_API_URL = os.getenv('SANITY_API_URL')
VESTABOARD_API_KEY = os.getenv('VESTABOARD_API_KEY')

# Function to fetch all launch information from Sanity
def fetch_all_launches():
    try:
        response = requests.get(SANITY_API_URL)
        response.raise_for_status()
        return response.json().get('result', [])
    except requests.RequestException as e:
        print(f"Error fetching data from Sanity API: {e}")
        return []

# Function to identify the most recently created launch
def get_most_recent_launch(launches):
    if not launches:
        return None
    most_recent_launch = max(launches, key=lambda x: x['_createdAt'])
    return most_recent_launch

# Function to format the launch description for Vestaboard
def format_launch_description(launch):
    launch_description = launch.get('launchMiniDescription', 'No description available')
    return launch_description

# Function to create the Vestaboard message layout
def create_vestaboard_message(description):
    # Initialize the board with empty values
    message_layout = [[0 for _ in range(22)] for _ in range(6)]

    # Center-align and left-align the description on the board
    lines = description.split('\n')
    for i, line in enumerate(lines):
        if i < 6:
            line_chars = [ord(char) - 32 for char in line]  # Convert characters to Vestaboard codes
            line_length = len(line_chars)
            start_index = (22 - line_length) // 2  # Center-align
            message_layout[i][start_index:start_index + line_length] = line_chars

    # Add yellow tile in the bottom-right-hand corner (character code 65)
    message_layout[-1][-1] = 65

    return message_layout

# Function to send the message to Vestaboard
def send_to_vestaboard(message_layout):
    url = 'https://rw.vestaboard.com/'
    headers = {
        'X-Vestaboard-Read-Write-Key': VESTABOARD_API_KEY,
        'Content-Type': 'application/json'
    }
    data = json.dumps(message_layout)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        print("Message sent to Vestaboard successfully!")
    except requests.RequestException as e:
        print(f"Failed to send message to Vestaboard: {e}")
        print(response.text)

# Main script execution
if __name__ == "__main__":
    launches = fetch_all_launches()
    print(f"Fetched launches: {launches}")
    most_recent_launch = get_most_recent_launch(launches)
    print(f"Most recent launch: {most_recent_launch}")
    if most_recent_launch:
        description = format_launch_description(most_recent_launch)
        print(f"Formatted description: {description}")
        message_layout = create_vestaboard_message(description)
        print(f"Message layout: {message_layout}")
        send_to_vestaboard(message_layout)
    else:
        print("No launch data available.")
