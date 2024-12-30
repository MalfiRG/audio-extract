import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from audio_extract import extract_audio
import datetime


class AudioExtractor:
    def __init__(self):
        """
        Initializes the AudioExtractor class.

        This constructor sets up the necessary directories for source videos and output audio files,
        and initializes a thread pool executor for concurrent audio extraction tasks.

        Attributes:
            timestamp (str): A timestamp string used to uniquely identify the output folder.
            source_folder (str): The path to the directory containing source video files.
            output_folder (str): The path to the directory where extracted audio files will be saved.
            executor (ThreadPoolExecutor): A thread pool executor for running audio extraction tasks concurrently.
        """
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.source_folder = os.path.join(os.getcwd(), "source_videos")
        self.output_folder = os.path.join(os.getcwd(), f"extracted_audio_{self.timestamp}")
        os.makedirs(self.output_folder, exist_ok=True)
        self.executor = ThreadPoolExecutor()

    def extract_audio_task(self, input_path, output_path):
        """
        Extracts audio from a video file and saves it to the specified output path.

        Args:
            input_path (str): The file path of the source video from which audio will be extracted.
            output_path (str): The file path where the extracted audio will be saved.

        Returns:
            None
        """
        extract_audio(input_path, output_path, overwrite=True)

    def extract_all_audio(self):
        """
        Extracts audio from all video files in the source directory concurrently.

        This function iterates over all files in the source directory, identifies video files
        with a '.mp4' extension, and submits concurrent audio extraction tasks for each file.
        The extracted audio is saved in the output directory with the same base filename and an '.mp3' extension.

        Returns:
            None
        """
        futures = []
        for file in os.listdir(self.source_folder):
            if file.endswith('.mp4'):
                filename = os.path.splitext(file)[0].rstrip()
                input_path = os.path.join(self.source_folder, file)
                output_path = os.path.join(self.output_folder, f"{filename}.mp3")
                futures.append(self.executor.submit(self.extract_audio_task, input_path, output_path))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

    def run(self):
        """
        Executes the audio extraction process.

        This function initiates the concurrent extraction of audio from all video files
        located in the source directory by submitting tasks to the thread pool executor.

        Returns:
            None
        """
        self.extract_all_audio()


AudioExtractor().run()