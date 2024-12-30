import os
from audio_extract import extract_audio
import datetime


class AudioExtractor:
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.source_folder = os.path.join(os.getcwd(), "source_videos")
        self.output_folder = os.path.join(os.getcwd(), f"extracted_audio_{self.timestamp}")
        os.makedirs(self.output_folder, exist_ok=True)
    
    def extract_all_audio(self):
        for file in os.listdir(f"{self.source_folder}"):
            if file.endswith('.mp4'):
                filename = os.path.splitext(file)[0].rstrip()
                extract_audio(input_path=f"./{self.source_folder}/{file}",
                              output_path=f"./{self.output_folder}/{filename}.mp3",
                              overwrite=True)

AudioExtractor().extract_all_audio()