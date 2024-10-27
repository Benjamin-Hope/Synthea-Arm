import PySimpleGUI as sg
import time
import os
from PIL import Image
import io
import base64
import threading
from transformers import GPT2LMHeadModel, GPT2Tokenizer  # Importing the necessary libraries

# Load the GPT-2 model and tokenizer
model_name = "gpt2"  # You can use a smaller or larger model if desired
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

model.config.pad_token_id = model.config.eos_token_id

# Function with a 3-second delay to simulate a long-running task
def my_function(window):
    connection = True
    for attempt in range(1, 5):  # Loop for 4 attempts
        time.sleep(1)  # Simulating work
        # Update the loading message in the additional layout
        window['-ATTEMPT-'].update(f"Attempt {attempt}")
        
    if connection:
        window['-CONNECTION-'].update("Connection Successful", text_color='dark green')
        window['-ATTEMPT-'].update(visible=False)
        
    else:
        # After the delay, hide the additional layout
        window['-ADDITIONAL-'].update(visible=False)

# Function to convert image to base64 and get image size
def convert_to_base64_and_get_size(image_path, scale=1.0):
    with Image.open(image_path) as img:
        # Resize the image
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size)
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_size = img.size  # Get image size (width, height)
        return base64.b64encode(buffer.getvalue()).decode("utf-8"), img_size

def resize_image(image_data, scale):
    img = Image.open(io.BytesIO(base64.b64decode(image_data)))
    new_size = (int(img.width * scale), int(img.height * scale))
    image = img.resize(new_size)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Get the current working directory
current_directory = os.getcwd()
# Paths to your loading animation images
loading_images = [
    r'\images\1.jpg', r'\images\2.jpg', r'\images\3.jpg', r'\images\4.jpg',
    r'\images\5.jpg', r'\images\6.jpg', r'\images\7.jpg', r'\images\8.jpg'
]  # Replace with your image filenames

# Convert images to base64 and get the size of the first image
loading_images_base64 = []
image_size = None
scale_factor = 0.65  # Scale factor to reduce size
for img in loading_images:
    img_base64, img_size = convert_to_base64_and_get_size(current_directory + img, scale=scale_factor)
    loading_images_base64.append(img_base64)
    if image_size is None:
        image_size = img_size

# Get screen resolution
screen_width, screen_height = sg.Window.get_screen_size()

# Calculate position to center the window
window_x = (screen_width - image_size[0]) // 2
window_y = (screen_height - image_size[1]) // 2

# Loading Screen Layout with an Image Element
loading_layout = [[sg.Image(data=loading_images_base64[0], key='-LOADING-')]]

# Create the Loading Screen window
loading_window = sg.Window(
    "Loading Screen", 
    loading_layout, 
    size=image_size, 
    location=(window_x, window_y),  # Center the window
    finalize=True
)

# Initialize animation variables
frame = 0
start_time = time.time()

# Loading Screen Loop for Animation
while time.time() - start_time < 3:  # Keep the loading window open for 3 seconds
    # Update the image in the window to create an animation effect
    loading_window['-LOADING-'].update(data=loading_images_base64[frame % len(loading_images_base64)])
    frame += 1
    loading_window.refresh()
    time.sleep(0.1)  # Adjust this for animation speed

loading_window.close()

# Resize the image to half its original size
resized_image_data = resize_image(loading_images_base64[2], 0.7)

# Create a layout for additional controls
additional_layout = [
    [sg.Text("Attempting to Perform a connection to the device", key='-CONNECTION-', text_color='blue')],
    [sg.Text("Attempt 0", key='-ATTEMPT-', text_color='red', visible=True)],  # Text element to update with attempts
    [sg.Button("Cancel", key='Cancel')]
]

# Create a layout with a centered image
layout = [
    [sg.Column([[sg.Image(data=resized_image_data)]], justification='center')],
    [sg.Column(additional_layout, key='-ADDITIONAL-', visible=True, justification='center')]
]

# Create the main window
main_window = sg.Window(
    "Synthea MARK.1",
    layout,
    size=image_size,
    location=(window_x, window_y),  # Center the window
    finalize=True
)

# Start the function in a separate thread
thread = threading.Thread(target=my_function, args=(main_window,))
thread.start()

# Main Screen Event Loop
while True:
    event, values = main_window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break

main_window.close()
