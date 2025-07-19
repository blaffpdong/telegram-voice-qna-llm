# audio_processor.py

import logging
from pathlib import Path
from typing import Optional
from pydub import AudioSegment


class AudioProcessor:
    def __init__(self, output_dir: str = "converted_audio"):
        """
        Initialization of the audio processor.

        :param output_dir: Directory for saving WAV files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def convert_to_wav(self, input_path: str) -> Optional[str]:
        try:
            audio = AudioSegment.from_file(input_path)

            # Set optimal parameters for Whisper:
            # - Mono sound (1 channel)
            # - Sample rate 16kHz
            # - Bit depth 16 bit
            audio = audio.set_channels(1).set_frame_rate(16_000)

            wav_path = self.output_dir / f"{Path(input_path).stem}.wav"
            audio.export(
                wav_path,
                format="wav",
                codec="pcm_s16le",  # 16-bit little-endian
                bitrate="16k",
            )
            return str(wav_path)
        except Exception as e:
            logging.error(f"[AudioProcessor] Conversion error: {e}")
            return None
