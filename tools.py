import tkinter as tk

def get_features_names(file_path):
    """
    returns the non-zero lines in the list format 
    """
    non_empty_lines = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Check if the line is not empty
                non_empty_lines.append(line)
    
    return non_empty_lines

print(get_features_names("features.txt"))