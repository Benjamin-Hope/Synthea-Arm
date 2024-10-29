from f_content import tts_speach as tts
from f_content import speech_recognition as f_SR
import PySimpleGUI as sg
import time
from PIL import Image, ImageTk
import io
import base64
import threading
import sys
import os
import cv2
import asyncio


class SyntheaApp:
    def __init__(self):
        self.window_x = None
        self.window_y = None
        self.video_path = None
        self.loading_video_path = None
        self.exit_condition = False
        self.current_directory = os.getcwd()
        self.response = None
        self.module_path = os.path.abspath(os.path.join('..', 'f_content'))
        if self.module_path not in sys.path:
            sys.path.append(self.module_path)

    def rec(self):
        self.SpeechRecognition = f_SR.SpeechRecognition()
        print("Listening...")
        while True:
            triggerWord = "Cynthia"
            shutdownWord = "exit"

            text = self.SpeechRecognition.recognize()
            if triggerWord in text:
                print("You said: ", text)
                self.response = text
                if shutdownWord in text or "EX" in text:
                    self.exit_condition = True
                    break

    def play_video(self, window, video_path, image_elem_key, scale_factor=0.7):
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
            window.write_event_value(
                '-UPDATE-IMAGE-', (image_elem_key, imgbytes))
        cap.release()

    def play_loading_video(self, window, video_path, image_elem_key, scale_factor=1):
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
            window.write_event_value(
                '-UPDATE-IMAGE-', (image_elem_key, imgbytes))
        cap.release()
        window.write_event_value('-VIDEO-DONE-', image_elem_key)

    def f_welcome(self, window):
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
            mytext = 'Welcome I’m Synthea, How can I help you today Sir?'
            Synthea = tts.TTS()
            Synthea.speak_text(mytext)
            threading.Thread(target=self.rec).start()
        else:
            # After the delay, hide the additional layout
            window['-ADDITIONAL-'].update(visible=False)

    def convert_to_base64_and_get_size(self, image_path, scale=1.0):
        with Image.open(image_path) as img:
            # Resize the image
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_size = img.size  # Get image size (width, height)
            return base64.b64encode(buffer.getvalue()).decode("utf-8"), img_size

    def run_loading_screen(self):
        # Paths to your loading animation images
        loading_images = [
            r'\frontend\images\side_military.webp', r'\frontend\images\goth.webp'
        ]  # Replace with your image filenames

        # Convert images to base64 and get the size of the first image
        loading_images_base64 = []
        image_size = None
        scale_factor = 0.65  # Scale factor to reduce size
        for img in loading_images:
            img_base64, img_size = self.convert_to_base64_and_get_size(
                self.current_directory + img, scale=scale_factor)
            loading_images_base64.append(img_base64)
            if image_size is None:
                image_size = img_size

        # Get screen resolution
        screen_width, screen_height = sg.Window.get_screen_size()

        # Calculate position to center the window
        self.window_x = (screen_width - image_size[0]) // 2
        self.window_y = (screen_height - image_size[1]) // 2

        # Loading Screen Layout with an Image Element
        loading_layout = [[sg.Image(key='-LOADING-')]]

        # Create the Loading Screen window
        loading_window = sg.Window(
            "Loading Screen",
            loading_layout,
            resizable=True,
            location=(self.window_x, self.window_y),  # Center the window
            background_color='#1a1f1d',
            finalize=True
        )

        # Start the video playback in a separate thread for the loading screen
        threading.Thread(target=self.play_loading_video, args=(
            loading_window, self.loading_video_path, '-LOADING-', 0.7), daemon=True).start()

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

    def run_main_window(self):
        # Get the current working directory
        '''self.video_path = os.path.join(
            self.current_directory, 'frontend\images', 'synthea_goth.mp4')'''
        self.video_path = os.path.join(
            self.current_directory, 'frontend\images', 'stear_synthea.mp4')

        # Create a layout for additional controls
        additional_layout = [
            [sg.Text("Attempting to Perform a connection to the device",
                     key='-CONNECTION-', text_color='blue')],
            # Text element to update with attempts
            [sg.Text("Attempt 0", key='-ATTEMPT-',
                     text_color='red', visible=True)],
            [sg.Button("Cancel", key='Cancel')]
        ]

        # Create a layout with a centered image
        layout = [
            [sg.Column([[sg.Image(key='-VIDEO-')]],
                       justification='center', background_color='#000000'),], #background_color='#1a1f1d')
            [sg.Column(additional_layout, key='-ADDITIONAL-',
                       visible=True, justification='center')]
        ]

        # Create the main window
        main_window = sg.Window(
            "Synthea MARK.1",
            layout,
            location=(self.window_x, self.window_y),  # Center the window
            background_color='#000000',
            resizable=True,
            finalize=True
        )

        # Start the video playback in a separate thread
        threading.Thread(target=self.play_video, args=(
            main_window, self.video_path, '-VIDEO-', 0.6), daemon=True).start()

        # Start the function in a separate thread
        thread = threading.Thread(target=self.f_welcome, args=(main_window,))
        thread.start()

        # Event loop
        while True:
            event, values = main_window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif self.exit_condition:
                break
            elif event == '-UPDATE-IMAGE-':
                key, imgbytes = values['-UPDATE-IMAGE-']
                main_window[key].update(data=imgbytes)

        main_window.close()
        sys.exit()

    async def runner(self):
        self.video_path = os.path.join(
            self.current_directory, 'frontend\images', 'synthea_goth.mp4')
        self.loading_video_path = os.path.join(
            self.current_directory, 'frontend\images', 'synthea.mp4')
        self.run_loading_screen()
        self.run_main_window()
