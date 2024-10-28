import cv2
from PIL import Image, ImageTk
import PySimpleGUI as sg
import os

def play_video(video_path):
    # Check if the file exists
    if not os.path.exists(video_path):
        print(f"Error: The video file '{video_path}' does not exist.")
        return

    # Open the video file using OpenCV
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video. The video codec might not be supported.")
        return
    else:
        print("Success: Video opened successfully.")

    # Define the layout of the GUI window
    layout = [[sg.Image(filename="", key="-IMAGE-")],
              [sg.Button("Play"), sg.Button("Pause"), sg.Button("Exit")]]

    # Create the window
    window = sg.Window("Video Player", layout, finalize=True)
    
    playing = False

    # Main loop
    while True:
        event, values = window.read(timeout=20)
        
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Play":
            playing = True
        elif event == "Pause":
            playing = False

        # If the video is playing, read the next frame
        if playing:
            ret, frame = cap.read()
            
            if not ret:
                print("Warning: End of video or cannot read the frame.")
                break  # Exit if end of video

            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert the frame to a PIL image, then to ImageTk format
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            
            # Update the image in the PySimpleGUI window
            window["-IMAGE-"].update(data=img)

    # Release the video capture object and close the GUI window
    cap.release()
    window.close()

# Run the function with your video path
play_video("C:\\Users\\Christopher Takacs\\OneDrive\\Ambiente de Trabalho\\Root\\My Projects\\Engineering\\Synthea-Arm\\pyhton\\frontend\\images\\synthea_goth.mp4")
