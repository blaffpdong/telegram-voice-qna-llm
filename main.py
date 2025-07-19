# main.py
import os
import logging
from dotenv import load_dotenv

# Module imports
from telegram_bot import TelegramBot
from audio_processor import AudioProcessor
from speech_to_text import SpeechToText
from llm_processor import LLMProcessor

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

load_dotenv()

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found! Check the .env file.")

    # Initialize services with configuration
    audio_processor = AudioProcessor(output_dir="converted_audio")

    speech_to_text = SpeechToText(
        model_size="small", device="cpu"  # if "cuda" если есть GPU
    )

    llm_processor = LLMProcessor()

    # Create bot with dependencies
    bot = TelegramBot(
        token=token,
        audio_processor=audio_processor,
        speech_to_text=speech_to_text,
        llm_processor=llm_processor,
    )

    # Run the bot - all processing logic is inside the bot
    bot.run()


if __name__ == "__main__":
    main()
