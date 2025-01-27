import os
import re
import streamlit as st

def time_to_seconds(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 4:
        days, hours, minutes, seconds = map(int, parts)
        return days * 86400 + hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")

def extract_test_case(lines, start, end):
    return "\n".join(lines[start:end+1])

def split_test_case_file(input_filename):
    # Create the main "test cases" folder if it doesn't exist
    main_folder = "features"
    os.makedirs(main_folder, exist_ok=True)

    with open(input_filename, 'r') as file:
        content = file.read()

    # Split the content into individual test cases
    test_cases = re.split(r'\n\n(?=Test Case \d+:)', content.strip())

    for test_case in test_cases:
        # Extract the test case number and title
        match = re.match(r'Test Case (\d+): (.+)', test_case)
        if match:
            case_number = match.group(1)
            case_title = match.group(2)

            # Create a folder for each test case
            folder_name = f"test_case_{case_number}"
            folder_path = os.path.join(main_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # Create and write to the test case file
            file_name = f"test_case_{case_number}.txt"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as f:
                f.write(test_case)

    st.success(f"Test cases split into individual files in the '{main_folder}' folder.")
