
import PySimpleGUI as sg
import time
from PIL import Image, ImageTk
import io
import base64
import threading
import sys
import os
import cv2

# Add the directory containing the module to the Python path
module_path = os.path.abspath(os.path.join('..', 'f_content'))
if module_path not in sys.path:
    sys.path.append(module_path)

import tts_speach as tts
# Function to play video in a loop and resize frames using a scaling factor

def play_video(window, video_path, image_elem_key, scale_factor=0.7):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Get original dimensions
        original_height, original_width = frame.shape[:2]

        # Calculate new dimensions using the scaling factor
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # Resize frame
        frame = cv2.resize(frame, (new_width, new_height))
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window.write_event_value('-UPDATE-IMAGE-', imgbytes)
    cap.release()


def play_loading_video(window, video_path, image_elem_key, scale_factor=1):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit if end of video

        # Get original dimensions
        original_height, original_width = frame.shape[:2]

        # Calculate new dimensions using the scaling factor
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # Resize frame
        frame = cv2.resize(frame, (new_width, new_height))
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window.write_event_value('-UPDATE-IMAGE-', (image_elem_key, imgbytes))
    cap.release()
    window.write_event_value('-VIDEO-DONE-', image_elem_key)


# Get the absolute path of the current directory
current_directory = os.getcwd()
video_path = os.path.join(current_directory, 'images', 'synthea_goth.mp4')
loading_video_path = os.path.join(current_directory, 'images', 'synthea.mp4')


def f_welcome(window):
    connection = True
    for attempt in range(1, 5):  # Loop for 4 attempts
        time.sleep(1)  # Simulating work
        # Update the loading message in the additional layout
        window['-ATTEMPT-'].update(f"Attempt {attempt}")

    if connection:
        window['-CONNECTION-'].update("Connection Successful",
                                      text_color='dark green')
        window['-ATTEMPT-'].update(visible=False)
        # The text that you want to convert to audio
        mytext = 'CHi there! I’m Synthea—your sharp-witted AI assistant. Think of me as your go-to for quick answers, smart solutions, and a dash of clever efficiency. Ready to tackle what’s next? Let’s dive in!'
        SYNTHEA = tts.TTS()
        SYNTHEA.speak_text(mytext)

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
    r'\images\1.jpg', r'\images\2.jpg', r'\images\3.jpg', r'\images\4.jpg', r'\images\side_military.webp', r'\images\goth.webp',
    r'\images\5.jpg', r'\images\6.jpg', r'\images\7.jpg', r'\images\8.jpg', r'\images\real_anime.webp'
]  # Replace with your image filenames

# Convert images to base64 and get the size of the first image
loading_images_base64 = []
image_size = None
scale_factor = 0.65  # Scale factor to reduce size
for img in loading_images:
    img_base64, img_size = convert_to_base64_and_get_size(
        current_directory + img, scale=scale_factor)
    loading_images_base64.append(img_base64)
    if image_size is None:
        image_size = img_size

# Get screen resolution
screen_width, screen_height = sg.Window.get_screen_size()

# Calculate position to center the window
window_x = (screen_width - image_size[0]) // 2
window_y = (screen_height - image_size[1]) // 2

# Loading Screen Layout with an Image Element
loading_layout = [[sg.Image(key='-LOADING-')]]

# Create the Loading Screen window
loading_window = sg.Window(
    "Loading Screen",
    loading_layout,
    resizable=True,
    location=(window_x, window_y),  # Center the window
    background_color='#1a1f1d',
    finalize=True
)

# Initialize animation variables
frame = 0
start_time = time.time()

# Loading Screen Loop for Animation
'''while time.time() - start_time < 3:  # Keep the loading window open for 3 seconds
    # Update the image in the window to create an animation effect
    loading_window['-LOADING-'].update(
        data=loading_images_base64[frame % len(loading_images_base64)])
    frame += 1
    loading_window.refresh()
    time.sleep(0.1)  # Adjust this for animation speed
'''

# Start the video playback in a separate thread for the loading screen
threading.Thread(target=play_loading_video, args=(
    loading_window, loading_video_path, '-LOADING-', 0.7), daemon=True).start()

# Event loop for the loading screen
while True:
    event, values = loading_window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    elif event == '-UPDATE-IMAGE-':
        key, imgbytes = values['-UPDATE-IMAGE-']
        loading_window[key].update(data=imgbytes)
    elif event == '-VIDEO-DONE-':
        break

loading_window.close()

# Resize the image to half its original size
resized_image_data = resize_image(loading_images_base64[5], 0.7)

# Create a layout for additional controls
additional_layout = [
    [sg.Text("Attempting to Perform a connection to the device",
             key='-CONNECTION-', text_color='blue')],
    # Text element to update with attempts
    [sg.Text("Attempt 0", key='-ATTEMPT-', text_color='red', visible=True)],
    [sg.Button("Cancel", key='Cancel')]
]

# Create a layout with a centered image
layout = [
    [sg.Column([[sg.Image(key='-VIDEO-')]], justification='center',
               background_color='#1a1f1d'),],
    [sg.Column(additional_layout, key='-ADDITIONAL-',
               visible=True, justification='center')]
]

# Create the main window
main_window = sg.Window(
    "Synthea MARK.1",
    layout,
    size=image_size,
    location=(window_x, window_y),  # Center the window
    background_color='#1a1f1d',
    finalize=True
)

# Start the video playback in a separate thread
threading.Thread(target=play_video, args=(
    main_window, video_path, main_window['-VIDEO-']), daemon=True).start()


# Start the function in a separate thread
thread = threading.Thread(target=f_welcome, args=(main_window,))
thread.start()

# Event loop
while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == '-UPDATE-IMAGE-':
        main_window['-VIDEO-'].update(data=values['-UPDATE-IMAGE-'])

main_window.close()
exit
