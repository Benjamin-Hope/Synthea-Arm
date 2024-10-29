# from f_content import communication as f_COM
from f_content import speech_recognition as f_SR
from f_content import tts_speach as f_TTS
from frontend import main as f_frontend
import threading
import subprocess
import sys,os, signal,time,random
from f_content import commands_h as f_CH
import asyncio

'''def main():
    SpeechRecognition = f_SR.SpeechRecognition()

    while True:
        triggerWord = "Cynthia"
        shutdownWord = "exit"

        print("Listening...")
        text = SpeechRecognition.recognize()
        if triggerWord in text:
            print("You said: ", text)
            if shutdownWord in text or "EX" in text:
                break'''

response_lock = threading.Lock()

def cleaner(path):
    # if the file exists in the path remove it
    if os.path.exists(path):
        os.remove(path)

def reboot():
    print("Rebooting script...")
    reboot_messages = [
    "Taking a quick refresh! I’ll be back in a moment.",
    "Just a brief reboot—I’ll be back in no time!",
    "Restarting to keep things running smoothly. See you in a sec!",
    "I’ll be right back! Just refreshing myself for peak performance.",
    "Taking a quick break to reboot. Be back shortly!",
    "A little refresh, and I’ll be good as new!",
    "Restarting to serve you better! Hang tight.",
    "Be right back! Just a small reboot for optimal assistance.",
    "Briefly stepping away to reboot. I’ll be back shortly!",
    "Time for a quick refresh. I’ll reconnect in just a moment!",
    "Just a moment—I’m rebooting to stay sharp!",
    "Doing a quick restart. I’ll be with you again in no time!",
    "Powering down briefly for a fresh start. Catch you soon!",
    "Rebooting to keep things running smoothly. Hang tight!",
    "Just a quick reboot to keep me in top form. See you in a sec!"
]

    #get current audio file
    path = os.path.abspath(os.path.join('audio', 'reboot.mp3'))
    cleaner(path)
    SYNTHEA = f_TTS.TTS()
    SYNTHEA.output_file = path
    random_index = random.randint(0, len(reboot_messages)-1)
    SYNTHEA.speak_text('Right away ...' + reboot_messages[random_index])
    time.sleep(1)  # Optional delay
    app.exit_condition = True
    subprocess.Popen([sys.executable] + sys.argv)
    os.kill(os.getpid(), signal.SIGTERM)
    sys.exit()

def shutdown():
    print("Shutting down script...")
    list = ["Until next time! Let me know if you need anything else.",
"Take care, and I’m here whenever you need!",
"Wishing you a productive and wonderful day ahead!",
"Goodbye for now! Reach out if you need anything further.",
"Stay awesome! I'll be here when you're ready.",
"Signing off for now—let me know if anything else comes up!",
"Here’s to a great day ahead! Talk soon.",
"Happy to help! Just a message away if you need me.",
"Thank you, and don’t hesitate to reconnect!",
"Wishing you all the best until next time!",
"Take it easy, and I’ll be here when you’re ready!",
"Looking forward to assisting you again soon!",
"Catch you later—always here if you need a hand!",
"Let’s connect again soon! Have a great day.",
"Signing off, but always here for support!"]
    #get current audio file
    path = os.path.abspath(os.path.join('audio', 'shutdown.mp3'))
    cleaner(path)
    SYNTHEA = f_TTS.TTS()
    SYNTHEA.output_file = path
    random_index = random.randint(0, len(list)-1)
    SYNTHEA.speak_text(list[random_index] + '... Goodbye!')
    time.sleep(1)  # Optional delay
    app.exit_condition = True
    #sys.exit()
    os.kill(os.getpid(), signal.SIGTERM)
    os._exit(1)

def chat_cleaner(entity, response_lock, command_entity):
    while True:
        with response_lock:
            if entity.response is not None:
                user_command = entity.response
                user_segment = command_entity.parse_command(user_command)
                print(user_segment)
                entity.response = None
                if user_segment == "reboot":
                    reboot()
                elif user_segment == "shutdown":
                    shutdown()
                
        time.sleep(0.01)

if __name__ == "__main__":
    app = f_frontend.SyntheaApp()
    response_lock = threading.Lock()

    command_entity = f_CH.CommandHandler()
    # Start the chat cleaner thread
    threading.Thread(target=chat_cleaner, args=(app, response_lock,command_entity), daemon=True).start()
    
    # Run the main app logic
    asyncio.run(app.runner())  # Ensure `runner` gracefully exits by setting `app.running = False`

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
