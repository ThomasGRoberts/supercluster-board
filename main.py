import requests

def update_vestaboard():
    api_url = "YOUR_SANITY_API_URL"
    vestaboard_api_key = "7f858a37+fa4b+442b+ac93+df153b0acb25"

    response = requests.get(api_url)
    data = response.json()
    launch_description = data['launchMiniDescription']

    # Prepare the Vestaboard message with yellow tile
    lines = [['' for _ in range(22)] for _ in range(6)]
    words = launch_description.split()
    line_index, char_index = 0, 0

    for word in words:
        if char_index + len(word) <= 22:
            for char in word:
                lines[line_index][char_index] = char
                char_index += 1
            lines[line_index][char_index] = ' '
            char_index += 1
        else:
            line_index += 1
            char_index = 0
            for char in word:
                lines[line_index][char_index] = char
                char_index += 1
            lines[line_index][char_index] = ' '
            char_index += 1

    # Convert to Vestaboard character codes
    char_map = {chr(i): i - 96 for i in range(97, 123)}
    char_map.update({' ': 0, '!': 59, '"': 60, '#': 61, '$': 62, '%': 63, '&': 64})
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char in char_map:
                lines[i][j] = char_map[char]
            else:
                lines[i][j] = 0  # Default to empty space

    # Add the yellow tile in the bottom-right corner
    lines[5][21] = 65

    # Send to Vestaboard API
    vestaboard_url = "https://rw.vestaboard.com/"
    headers = {
        "X-Vestaboard-Read-Write-Key": vestaboard_api_key,
        "Content-Type": "application/json"
    }
    requests.post(vestaboard_url, json=lines, headers=headers)
    return "Vestaboard updated successfully"

if __name__ == "__main__":
    print(update_vestaboard())
