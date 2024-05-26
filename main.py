import os
import requests
import json
import datetime

# Retrieve environment variables (set these in your GitHub Secrets)
SANITY_API_URL = os.getenv('SANITY_API_URL')
VESTABOARD_API_KEY = os.getenv('VESTABOARD_API_KEY')

# Character codes for Vestaboard
CHARACTER_CODES = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
    'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19,
    'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
    '1': 27, '2': 28, '3': 29, '4': 30, '5': 31, '6': 32, '7': 33, '8': 34, '9': 35, '0': 36,
    '!': 37, '@': 38, '#': 39, '$': 40, '(': 41, ')': 42, '-': 44, '+': 46, '&': 47, '=': 48,
    ';': 49, ':': 50, "'": 52, '"': 53, '%': 54, ',': 55, '.': 56, '/': 59, '?': 60, '°': 62,
    'Red': 63, 'Orange': 64, 'Yellow': 65, 'Green': 66, 'Blue': 67, 'Violet': 68, 'White': 69, 'Black': 70,
    'Filled': 71
}

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

    # Center-align and vertically align the description on the board
    lines = description.split('\n')
    num_lines = len(lines)
    start_row = (6 - num_lines) // 2
    for i, line in enumerate(lines):
        if i < 6:
            line_chars = [CHARACTER_CODES.get(char, 0) for char in line]  # Convert characters to Vestaboard codes
            line_length = len(line_chars)
            start_index = (22 - line_length) // 2  # Center-align
            message_layout[start_row + i][start_index:start_index + line_length] = line_chars

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
