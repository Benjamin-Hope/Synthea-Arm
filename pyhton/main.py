# from f_content import communication as f_COM
from f_content import speech_recognition as f_SR
from frontend import main as f_frontend
import threading
import sys
import time


def main():
    SpeechRecognition = f_SR.SpeechRecognition()

    while True:
        triggerWord = "Cynthia"
        shutdownWord = "exit"

        print("Listening...")
        text = SpeechRecognition.recognize()
        if triggerWord in text:
            print("You said: ", text)
            if shutdownWord in text or "EX" in text:
                break

response_lock = threading.Lock()

def chat_cleaner(entity, response_lock):
    while True:
        with response_lock:
            if entity.response is not None:
                print(entity.response)
                entity.response = None
        time.sleep(0.01)

if __name__ == "__main__":
    app = f_frontend.SyntheaApp()
    response_lock = threading.Lock()
    
    # Start the chat cleaner thread
    threading.Thread(target=chat_cleaner, args=(app, response_lock), daemon=True).start()
    
    # Run the main app logic
    app.runner()  # Ensure `runner` gracefully exits by setting `app.running = False`

    '''# Create threads for runner and main
    runner_thread = threading.Thread(target=app.runner)
    main_thread = threading.Thread(target=main)

    # Start both threads
    runner_thread.start()
    main_thread.start()

    # if one the threads exits, exit the other
    if not runner_thread.is_alive():
        main_thread.join()
    if not main_thread.is_alive():
        runner_thread.join()

    # exit the program
    sys.exit()'''
