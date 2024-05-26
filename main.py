import requests
import json
import datetime

# Environment variables (these should be set in your GitHub Secrets)
import os

SANITY_API_URL = os.getenv('SANITY_API_URL')
VESTABOARD_API_KEY = os.getenv('VESTABOARD_API_KEY')

# Function to fetch all launch information from Sanity
def fetch_all_launches():
    response = requests.get(SANITY_API_URL)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print("Failed to fetch data from Sanity API")
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

    # Split description into lines and limit to 6 lines
    lines = description.split('\n')[:6]

    for i, line in enumerate(lines):
        line_chars = [ord(char) - 32 for char in line if 0 <= ord(char) - 32 <= 71]  # Ensure valid range
        line_length = len(line_chars)
        if line_length > 22:
            line_chars = line_chars[:22]  # Truncate if longer than 22 chars

        # Center-align
        start_index = (22 - line_length) // 2
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
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Message sent to Vestaboard successfully!")
    else:
        print("Failed to send message to Vestaboard")
        print("Response:", response.text)

# Main script execution
if __name__ == "__main__":
    if not SANITY_API_URL or not VESTABOARD_API_KEY:
        print("Environment variables SANITY_API_URL and VESTABOARD_API_KEY must be set")
    else:
        launches = fetch_all_launches()
        most_recent_launch = get_most_recent_launch(launches)
        if most_recent_launch:
            description = format_launch_description(most_recent_launch)
            print(f"Launch description: {description}")  # Print the launch description for debugging
            message_layout = create_vestaboard_message(description)
            print(f"Message layout: {message_layout}")  # Print the message layout for debugging
            send_to_vestaboard(message_layout)
        else:
            print("No launch data available.")
