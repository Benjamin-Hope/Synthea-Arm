import edge_tts
import pygame
import asyncio
import os


class TTS:
    def __init__(self):
        self.text = ""
        self.voice = "en-IE-EmilyNeural"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(script_dir, '..', 'audio')
        # Create the directory if it doesn't exist
        os.makedirs(audio_dir, exist_ok=True)
        self.output_file = os.path.join(audio_dir, "voice.mp3")
        self.communicate = None

    def set_text(self, text):
        self.text = text
        self.communicate = edge_tts.Communicate(
            self.text, self.voice)
        # print(f"Text set to: {self.text}")
        asyncio.run(self.speak())

    async def save(self, output_file):
        # print(f"Saving to file: {output_file}")
        await self.communicate.save(output_file)
        # print(f"File saved: {output_file}")

    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    async def speak(self):
        await self.save(self.output_file)
        self.play()

    def speak_text(self, text):
        self.set_text(text)


# Example

# tts = TTS()
# tts.speak_text("That is very funny sir")
