import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

click_positions = []
current_picture = ""

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
canvas_height = int(app_height*0.9)
canvas_weight = int(app_width*0.7)

canvas = tk.Canvas(app, width=canvas_weight, height=canvas_height, bg="#D3D3D3", borderwidth=1)
canvas.place(relx = 0.05, rely = 0.07, relheight=0.9, relwidth=0.7)



def select_image():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename()

    if file_path:
        image = Image.open(file_path)
        
        global current_picture
        current_picture = file_path.split("/")[-1]

        orig_size = image.size
        print(orig_size)

        image = image.resize((canvas_weight, canvas_height))

        # Convert the image to Tkinter-compatible format
        image_tk = ImageTk.PhotoImage(image)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        canvas.image = image_tk  # Save a reference to avoid garbage collection


b_select_image = tk.Button(app, command=select_image, text = "select image")
b_select_image.place(relx = 0.05, rely=0.03)

b_next = tk.Button(app, text=">")

"""
# Bind mouse left-click event to the canvas
canvas.bind("<Button-1>", on_click)



def on_click(event):
    # Add mouse click position to the list
    click_positions.append((event.x, event.y))











# Create a button to select an image
select_button = tk.Button(app, text="Select Image", command=select_image)
select_button.pack()"""

# Start the tkinter event loop
app.mainloop()

# Print the list of mouse click positions
print(click_positions)