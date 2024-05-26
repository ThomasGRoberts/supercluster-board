# Function to create the Vestaboard message layout
def create_vestaboard_message(description):
    # Initialize the board with empty values
    message_layout = [[0 for _ in range(22)] for _ in range(6)]
    
    words = description.split(' ')
    current_row = []
    current_line_length = 0
    total_word_count = len(words)
    median_row = len(message_layout) // 2  # Calculate the median row index
    
    # Calculate the total number of characters in the message
    total_chars = sum(len(word) for word in words) + (len(words) - 1)  # Account for spaces between words
    
    row_index = 0
    
    for word in words:
        word_length = len(word)
        
        # If the word fits in the current line, add it
        if current_line_length + word_length <= 22:
            current_row.append(word)
            current_line_length += word_length + 1  # +1 for the space
        else:
            # Calculate the number of empty spaces to add before the line to center-align the text
            num_empty_spaces = (22 - total_chars) // 2
            
            # Calculate the starting column index to center-align the text
            start_col_index = num_empty_spaces
            
            # Place the current row on the board with center alignment
            for i, word in enumerate(current_row):
                word_length = len(word)
                col_index = start_col_index + sum(len(current_row[j]) for j in range(i)) + i
                if col_index < 22:
                    for char in word:
                        if col_index < 22:
                            message_layout[row_index][col_index] = char_to_code.get(char, 0)
                            col_index += 1
            
            # Move to the next row
            row_index += 1
            if row_index >= 6:  # Vestaboard has only 6 rows
                break
            # Reset variables for the next row
            current_row = [word]
            current_line_length = word_length + 1
    
    # Add any remaining words in the current row
    if row_index < 6:
        # Calculate the number of empty spaces to add before the line to center-align the text
        num_empty_spaces = (22 - total_chars) // 2
        
        # Calculate the starting column index to center-align the text
        start_col_index = num_empty_spaces
        
        # Place the remaining row on the board with center alignment
        for i, word in enumerate(current_row):
            word_length = len(word)
            col_index = start_col_index + sum(len(current_row[j]) for j in range(i)) + i
            if col_index < 22:
                for char in word:
                    if col_index < 22:
                        message_layout[row_index][col_index] = char_to_code.get(char, 0)
                        col_index += 1
    
    # Add yellow tile in the median row to vertically align the text
    for i in range(22):
        message_layout[median_row][i] = 65

    return message_layout
