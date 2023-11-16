import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import json

click_positions = []
current_picture = ""



haarcascade = "haarcascade_frontalface_alt2.xml"
detector = cv2.CascadeClassifier(haarcascade)


app = tk.Tk()
app.title("Image Viewer")

# Get the screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set the application window size
app_width = int(screen_width * 0.8)
app_height = int(screen_height * 0.8)
app.geometry(f"{app_width}x{app_height}")

# Create a canvas to display the images
canvas_relheight = 0.9
canvas_relwidth = 0.5

canvas_width = int(app_width*canvas_relwidth)
canvas_height = int(app_height * canvas_relheight)

canvas = tk.Canvas(app, width=int(app_height*canvas_relwidth), 
                   height=int(app_height * canvas_relheight), bg="#D3D3D3", borderwidth=1)

canvas.place(relx = 0.05, rely = 0.07, 
             relheight=canvas_relheight, relwidth=canvas_relwidth)


def on_click(event):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Calculate the relative position
    relative_x = event.x / canvas_width
    relative_y = event.y / canvas_height

    # Add relative position to the list
    # click_positions.append((relative_x, relative_y))
    print(relative_x, relative_y)

canvas.bind("<Button-1>", on_click)


# CSV file manipulation
with open('data.json', 'r') as file:
    # Load the JSON data
    data = json.load(file)





def select_image():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename()

    if file_path:
        image = Image.open(file_path)
        
        global current_picture
        current_picture = file_path.split("/")[-1]

        faces = detector.detectMultiScale(cv2.imread(file_path))
        face_coordinates = faces[0]
        # getting values in this format [[280  46 210 210]]
        # (640, 480) = (x, y)
        x_len = 320
        y_len = 300
        if len(faces) == 1:
            center_x = int(face_coordinates[0] + face_coordinates[2]/2)
            center_y = int(face_coordinates[1] + face_coordinates[3]/2)

            x_topright = center_x + x_len//2
            if x_topright < x_len: x_topright = x_len
            if x_topright > 640 : x_topright = 640

            y_topright = center_y + y_len//2
            if y_topright < y_len: y_topright = y_len
            if y_topright > 480 : y_topright = 480

            bbox = (x_topright-x_len, y_topright-y_len, x_topright, y_topright)
            image = image.crop(bbox)
            print (image.size)
            print ("cropped with the coordinates", bbox)

            print("Faces:\n", face_coordinates)
            

        orig_size = image.size
        print(orig_size)

        image = image.resize((canvas_width, canvas_height))

        # Convert the image to Tkinter-compatible format
        image_tk = ImageTk.PhotoImage(image)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        canvas.image = image_tk  # Save a reference to avoid garbage collection

        
        
        

b_select_image = tk.Button(app, command=select_image, text = "select image")
b_select_image.place(relx = 0.05, rely=0.03)

b_next = tk.Button(app, text=">")

# Start the tkinter event loop
app.mainloop()

# Print the list of mouse click positions
print(click_positions)