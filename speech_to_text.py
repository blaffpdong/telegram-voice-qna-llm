# speech_to_text.py
# https://pypi.org/project/openai-whisper/

import logging
import whisper
import os
import warnings

class SpeechToText:
    def __init__(self, model_size="turbo", device="cpu"):
        """
        Initialization of the transcriber.
        :param model_size: model size (tiny, base, small, medium, large, turbo)
        :param device: computing device (auto, cpu, cuda)
        """
        self.model_size = model_size
        self.device = device
        self.model = None

        # Ignore warnings related to FP16
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
        warnings.filterwarnings("ignore", category=UserWarning, module="whisper")

    def load_model(self):
        """Loads the Whisper model (automatically called during transcription)"""
        if self.model is None:
            self.model = whisper.load_model(name=self.model_size, device=self.device)

    def transcribe(self, audio_path, language=None, initial_prompt=None):
        """
        Transcribes an audio file to text
        :param audio_path: path to the WAV file
        :param language: language of the audio (ru, en, etc.), None for auto-detection
        :param initial_prompt: prompt to improve recognition
        :return: recognized text with punctuation
        """
        # Check if file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        with open(audio_path, "rb") as f:
            duration = len(f.read()) / (16_000 * 1)  # Approximate duration estimate
            if duration > 60:  # If longer than 1 minute
                logging.warning(f"Long audio: {duration:.1f} sec")

        # Auto-load model on first call
        self.load_model()

        # Perform transcription
        result = self.model.transcribe(
            audio=audio_path,
            language=language,
            initial_prompt=initial_prompt,
            task="transcribe",
            verbose=False,
        )

        return result
