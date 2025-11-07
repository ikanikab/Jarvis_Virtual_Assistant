import re

def extract_yt_term(command):
    # pattern to capture the song name
    pattern = r'play\s+(.*?)(?:\s+on\s+youtube)?$'
    # use research to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # if a match is found, return the extracted song name; otherwise, return true
    return match.group(1) if match else None