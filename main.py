import tkinter as tk
from tkinter import filedialog, ttk, Listbox


from PIL import Image, ImageTk
import cv2
import json

import os
import numpy as np

with open('data.json', 'r') as file: data = json.load(file)

def select_item_in_listbox(listbox, item_to_select):
    for index, item in enumerate(listbox.get(0, 'end')):
        if item == item_to_select:
            listbox.selection_clear(0, 'end')  # Clear any existing selections
            listbox.selection_set(index)  # Select the item
            listbox.see(index)  # Ensure the item is visible
            break

def update_tree_from_json(file_name):
     # Check if file_name is in the JSON data
    if file_name in data['content']:
        # If it is, update the Treeview
        for index, item_id in enumerate(tree.get_children()):
            # Get the new value for this row
            new_value = data['content'][file_name][index]
            
            # Update the row without changing the first column
            tree.item(item_id, values=(tree.item(item_id)['values'][0], new_value))
    else:
        # If it isn't, clear the Treeview
        for item_id in tree.get_children():
            tree.item(item_id, values=(tree.item(item_id)['values'][0], ''))

def update_circles_on_canvas():
    # Clear all items except the image
    for item_id in canvas.find_all():
        if item_id != current_image_id:
            canvas.delete(item_id)

    # Draw the circles
    for i, item_id in enumerate(tree.get_children()):
        # Get the coordinates from the second column
        coords = tree.item(item_id)['values'][1]

        # If the column is not empty
        if coords:
            x, y = map(int, coords.split())
            x, y = normalize_to_event(x, y)

            r = 5
            canvas.create_oval(x - r, y - r, x + r, y + r, fill='red')
            canvas.create_text(x, y - r - 10, text=str(i+1), fill="red", font=('bold'))

def normalize_to_event(abs_x, abs_y):
    # normalize the coordinates with respect to the resized image on the canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    event_x = (abs_x - orig_x)/x_len * canvas_width
    event_y = (abs_y - orig_y)/y_len * canvas_height
    return event_x, event_y

def normalize_to_absolute(event_x, event_y):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    relative_x = event_x / canvas_width
    relative_y = event_y / canvas_height

    abs_coord_x = int(relative_x*x_len + orig_x)
    abs_coord_y = int(relative_y*y_len + orig_y)

    return abs_coord_x, abs_coord_y

def auto_pick_landmarks():
    global current_picture
    global current_folder
    file_path = os.path.join(current_folder, current_picture)

    img = cv2.imread(file_path)
    faces = detector.detectMultiScale(img)
    #face_coordinates = faces[0]

    if len(faces) >= 1:
        # Detect landmarks of the biggest
        index, box = max(enumerate(faces), key=lambda x: x[1][2])
        _, landmarks = landmark_detector.fit(img, np.array([faces[index].tolist()]))

        selected_indices = [17, 21, 22, 26, 36, 39, 42, 45, 0, 30, 16, 48, 54, 8]
        selected_landmarks = [landmarks[0][0][i] for i in selected_indices]
        for i, item in enumerate(tree.get_children()):
            coords = selected_landmarks[i]
            # Convert to integers and then to string
            text = ' '.join(map(str, map(int, map(round, coords))))
            # Update the second column of the item
            tree.set(item, '#2', text)
        update_circles_on_canvas()

current_picture = ""
current_folder = ""
current_image_id = ""

is_resized = False
x_len = 360
y_len = 310

orig_x = 0
orig_y = 0



haarcascade = "haarcascade_frontalface_alt2.xml"
detector = cv2.CascadeClassifier(haarcascade)

# https://www.google.com/url?sa=i&url=https%3A%2F%2Fanswers.opencv.org%2Fquestion%2F192167%2Ffacemarklbf-training-fewer-landmark-points-than-68%2F&psig=AOvVaw1Qt5otMj4qtC0pPcrgD6g7&ust=1700545351471000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCJiow57v0YIDFQAAAAAdAAAAABAE
LBFmodel = "lbfmodel.yaml"
landmark_detector  = cv2.face.createFacemarkLBF()
landmark_detector.loadModel(LBFmodel)

app = tk.Tk()
app.title("Image Viewer")

# Get the screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set the application window size
app_width = int(screen_width * 0.8)
app_height = int(screen_height * 0.8)
app.geometry(f"{app_width}x{app_height}")



# define columns
columns = ('name', 'coordinates')

tree = ttk.Treeview(app, columns=columns, show='headings')

# define headings
tree.heading('name', text='Name')
tree.heading('coordinates', text='Coordinates')
tree.place(relx=0.6, rely = 0.07, relwidth=0.2, relheight=0.86)
tree.column('name', width=50)
tree.column('coordinates', width=100)

# take all values except for the addresses
for value in data["header"][1:]:
    tree.insert('', 'end', values=(value, '', '', ''))


def save_data ():
    entry = [tree.item(item_id)['values'][1] for item_id in tree.get_children()]
    last_folder = os.path.basename(current_folder)
    idx = f"{last_folder}/{current_picture}"
    data["content"][idx] = entry
    #print (data)
    with open("data.json", 'w') as json_file: json.dump(data, json_file)

save_button = tk.Button(app, text = "Save data", command=save_data)
save_button.place(relx=0.6, rely = 0.93, relwidth=0.2, relheight=0.04)

auto_pick_button = tk.Button(app, text = "Auto", command=auto_pick_landmarks)
auto_pick_button.place(relx=0.9, rely = 0.03, relwidth=0.05, relheight=0.03)



frame_listbox = tk.Frame(app, background="gray") 
frame_listbox.place(relx = 0.81, rely = 0.07, relheight=0.9, relwidth=0.14)
images_listbox = Listbox (frame_listbox, selectmode="single", exportselection=0)
images_listbox.place(relwidth = 1, relheight = 1)

listbox_scrollbar = tk.Scrollbar(frame_listbox)
listbox_scrollbar.pack(side="right", fill="y")
images_listbox.config(yscrollcommand = listbox_scrollbar.set)
listbox_scrollbar.config(command = images_listbox.yview)

def on_select(evt):
    # Note here that Tkinter passes an event object to on_select()
    w = evt.widget
    index = int(w.curselection()[0])
    file_name = w.get(index)
    file_path = os.path.join(current_folder, file_name)
    open_image(file_path)

images_listbox.bind('<<ListboxSelect>>', on_select)


def go_to_next_line():
    selected = images_listbox.curselection()
    if selected:
        next_index = selected[0] + 1

        if next_index < images_listbox.size():
            images_listbox.selection_clear(selected)
            images_listbox.selection_set(next_index)
            images_listbox.see(next_index)
            images_listbox.event_generate("<<ListboxSelect>>")

def go_to_previous_line():
    selected = images_listbox.curselection()
    if selected:
        prev_index = selected[0] - 1
        if prev_index >= 0:
            images_listbox.selection_clear(selected)
            images_listbox.selection_set(prev_index)
            images_listbox.see(prev_index)
            images_listbox.event_generate("<<ListboxSelect>>")

next_button = tk.Button(app, text=">", command=go_to_next_line)
next_button.place(relx = 0.56, rely=0.45, relheight=0.1, relwidth=0.03)

prev_button = tk.Button(app, text="<", command=go_to_previous_line)
prev_button.place(relx = 0.01, rely=0.45, relheight=0.1, relwidth=0.03)


# Create a canvas to display the images
canvas_relheight = 0.9
canvas_relwidth = 0.5

canvas_width = int(app_width*canvas_relwidth)
canvas_height = int(app_height * canvas_relheight)

canvas = tk.Canvas(app, width=int(app_height*canvas_relwidth), 
                   height=int(app_height * canvas_relheight), bg="#D3D3D3", borderwidth=1)

canvas.place(relx = 0.05, rely = 0.07, 
             relheight=canvas_relheight, relwidth=canvas_relwidth)


def iter_tree(coord):
    # If nothing is selected, select the first item
    if not tree.selection():
        first_item = tree.get_children()[0]
        tree.selection_set(first_item)
        tree.item(first_item, values=(tree.item(first_item)['values'][0], coord))
    else:
        # If something is selected, update the values at the selected row
        selected_item = tree.selection()[0]  # get selected item
        tree.item(selected_item, values=(tree.item(selected_item)['values'][0], coord))

        # Move selection to next item
        next_item = tree.next(selected_item)
        if next_item:  # if next_item exists
            tree.selection_set(next_item)
        else:  # Loop back to first item if at the end
            first_item = tree.get_children()[0]
            tree.selection_set(first_item)

def on_click(event):
    abs_coord_x, abs_coord_y = normalize_to_absolute (event.x, event.y)
    print(abs_coord_x, abs_coord_y)
    iter_tree((abs_coord_x, abs_coord_y))
    update_circles_on_canvas()

canvas.bind("<Button-1>", on_click)





def select_image():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename()

    if file_path:
        open_image (file_path)
    
        # UPDATE LISTBOX
        global current_folder
        file_names = os.listdir(current_folder)
        # Perform a natural sort on the file names
        sorted_file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x)[0].split('_')[1]))
        images_listbox.delete(0, tk.END)
        for file_name in sorted_file_names:
            images_listbox.insert(tk.END, file_name)
            

        select_item_in_listbox(images_listbox, file_path.split("/")[-1])
        

def open_image(file_path):
    image = Image.open(file_path)
    
    global current_picture
    current_picture = os.path.split(file_path)[-1]

    folder_path = os.path.dirname(file_path)

    global current_folder
    current_folder = folder_path

    last_folder = os.path.basename(current_folder)
    idx = f"{last_folder}/{current_picture}"
    update_tree_from_json (idx)

    
    faces = detector.detectMultiScale(cv2.imread(file_path))
    print (faces)
    
    # getting values in this format [[280  46 210 210]]
    # (640, 480) = (x, y)

    global is_resized
    is_resized = False
    global orig_x
    global orig_y
    orig_x = 0
    orig_y = 0

    if len(faces) >= 1:
        # Get the index of the box with the biggest area for zoom
        index, box = max(enumerate(faces), key=lambda x: x[1][2])
        face_coordinates = faces[index]
        
        is_resized = True
        center_x = int(face_coordinates[0] + face_coordinates[2]/2)
        center_y = int(face_coordinates[1] + face_coordinates[3]/2)

        x_topright = center_x + x_len//2
        if x_topright < x_len: x_topright = x_len
        if x_topright > 640 : x_topright = 640

        y_topright = center_y + y_len//2
        if y_topright < y_len: y_topright = y_len
        if y_topright > 480 : y_topright = 480

        # Updating the origin
        orig_x = x_topright-x_len
        orig_y = y_topright-y_len

        bbox = (x_topright-x_len, y_topright-y_len, x_topright, y_topright)
        image = image.crop(bbox)
        print (image.size)
        print ("cropped with the coordinates", bbox)

        print("Faces:\n", face_coordinates)
    
        

    #orig_size = image.size
    #print(orig_size)

    image = image.resize((canvas_width, canvas_height))

    # Convert the image to Tkinter-compatible format
    image_tk = ImageTk.PhotoImage(image)

    # Display the image on the canvas
    canvas.delete("all")
    global current_image_id
    current_image_id = canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
    canvas.image = image_tk  # Save a reference to avoid garbage collection
    update_circles_on_canvas()
        
        
        

b_select_image = tk.Button(app, command=select_image, text = "select image")
b_select_image.place(relx = 0.05, rely=0.03)

b_next = tk.Button(app, text=">")

# Start the tkinter event loop
app.mainloop()

# Print the list of mouse click positions
#print(click_positions)