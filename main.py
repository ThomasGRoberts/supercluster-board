import requests
import json
import datetime

# Environment variables (set these in your GitHub Secrets)
SANITY_API_URL = 'YOUR_SANITY_API_URL'  # URL that produces all launch information
VESTABOARD_API_KEY = 'YOUR_VESTABOARD_API_KEY'

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
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Message sent to Vestaboard successfully!")
    else:
        print("Failed to send message to Vestaboard")
        print(response.text)

# Main script execution
if __name__ == "__main__":
    launches = fetch_all_launches()
    most_recent_launch = get_most_recent_launch(launches)
    if most_recent_launch:
        description = format_launch_description(most_recent_launch)
        message_layout = create_vestaboard_message(description)
        send_to_vestaboard(message_layout)
    else:
        print("No launch data available.")

