import tkinter as tk
import cv2
import pandas as pd

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

def select_item_in_listbox(listbox, item_to_select):
    for index, item in enumerate(listbox.get(0, 'end')):
        if item == item_to_select:
            listbox.selection_clear(0, 'end')  # Clear any existing selections
            listbox.selection_set(index)  # Select the item
            listbox.see(index)  # Ensure the item is visible
            break


"""
# Create an empty DataFrame
df = pd.DataFrame(columns=get_features_names("features.txt"))

# Write the DataFrame to a CSV file
df.to_csv("data.csv", index=False)
"""
df = pd.read_csv("data.csv")
print (df)

#print(get_features_names("features.txt"))

