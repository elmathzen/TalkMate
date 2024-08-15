import re


def split_text_and_code(text):
    # Define a regex pattern for code detection
    pattern = r'(```.*?```)'  # This pattern matches text within triple backticks
    
    # Use regex split to separate text and code
    segments = re.split(pattern, text, flags=re.DOTALL)
    
    return segments