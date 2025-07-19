# telegram_bot.py
# Examples for python-telegram-bot: 
# https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples

"""
Don't forget to enable inline mode with @BotFather

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging
from tempfile import NamedTemporaryFile
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from typing import Optional


class TelegramBot:
    def __init__(
        self, token: str, audio_processor, speech_to_text, llm_processor
    ) -> None:
        """Initialization of the bot, :param token: Bot token from @BotFather."""
        self.token = token
        self.application = None
        self.audio_processor = audio_processor
        self.speech_to_text = speech_to_text
        self.llm_processor = llm_processor

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a message when the command /start is issued."""
        await self.send_message(update=update, text="Start!")

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a message when the command /help is issued."""
        await self.send_message(update=update, text="Help!")

    async def ping_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a message when the command /ping is issued."""
        await self.send_message(update=update, text="Pong")

    async def send_message(
        self,
        update: Update,
        text: str,
        parse_mode: ParseMode = ParseMode.HTML,
        reply_to_message_id: Optional[int] = None,
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
    ) -> None:
        """Unified method for sending messages to chat

        :param update: Update object from Telegram API
        :param text: Message text
        """

        chat_id = update.effective_chat.id if update.effective_chat else None

        if not chat_id:
            logging.warning("Chat ID not found in update")
            return
        try:
            await self.application.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                reply_to_message_id=reply_to_message_id,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
            )
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

    async def handle_audio(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not update.message:
            return

        try:
            # Скачивание файла
            audio_file = await self._download_file(update)
            if not audio_file:
                await update.message.reply_text("× Failed to download audio")
                return

            # Convert to WAV
            wav_path = self.audio_processor.convert_to_wav(audio_file)
            # Delete the temporary source file immediately after conversion
            try:
                os.unlink(audio_file)
            except Exception as e:
                logging.error(f"Error deleting temporary file: {e}")

            if not wav_path:
                await update.message.reply_text("× Failed to convert audio")
                return

            # Show "typing" status
            await update.message.chat.send_action(action=ChatAction.TYPING)

            try:
                # Recognize speech
                transcribed = self.speech_to_text.transcribe(wav_path)
                text = transcribed["text"]
                language = transcribed["language"]
                # Send the result
                # await update.message.reply_text(f"🎤 Recognized text:\n\n{text}")

                # Generate a response using LLM
                await update.message.chat.send_action(action=ChatAction.RECORD_VIDEO_NOTE)
                llm_response = self.llm_processor.generate_response(text, language)
                await update.message.reply_text(f"{llm_response}")
            except Exception as e:
                logging.error(f"Error recognizing speech: {e}")
                await update.message.reply_text("× Failed to recognize speech")
            finally:
                # Delete the WAV file after processing
                try:
                    os.unlink(wav_path)
                except Exception as e:
                    logging.error(f"Error deleting WAV file: {e}")

        except Exception as e:
            logging.error(f"Error processing audio: {e}")
            await update.message.reply_text("⚠ An unexpected error occurred")

    async def _download_file(self, update: Update) -> Optional[str]:
        """Downloads the file and returns the path to it."""
        try:
            if update.message.voice:
                file = await update.message.voice.get_file()
            elif update.message.audio:
                file = await update.message.audio.get_file()
            else:
                return None

            with NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
                await file.download_to_drive(temp_file.name)
                return temp_file.name

        except Exception as e:
            logging.error(f"Error downloading file: {e}")
            return None

    def run(self) -> None:
        """Run the bot"""
        logging.info("Telegram Bot Launched!")

        # Create the Application and pass it your bot's token.
        self.application = Application.builder().token(self.token).build()

        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("ping", self.ping_command))

        # Audio handler
        self.application.add_handler(
            MessageHandler(filters.VOICE | filters.AUDIO, self.handle_audio)
        )

        # Run the bot until the user presses Ctrl-C
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
