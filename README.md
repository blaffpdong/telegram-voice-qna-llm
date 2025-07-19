# telegram-voice-qna-llm

**telegram-voice-qna-llm** is a Telegram bot that receives voice messages, transcribes them using OpenAI Whisper, and generates concise, professional answers with a local LLM (such as Mistral-7B). The bot supports multiple languages, works fully offline after downloading the models, and is designed for automating interviews or Q&A sessions.

**Features:**
- Accepts voice and audio messages in Telegram
- Converts audio to text (Whisper)
- Generates answers using a local LLM (Mistral-7B)
- Supports multiple languages
- Quick setup and launch on MacOS/Linux

![telegram-voice-qna-llm](/docs/preview.jpg)

## Architecture

The project consists of the following main files:
- `main.py`: Main entry point for the bot, handles incoming messages and orchestrates the workflow.
- `telegram_bot.py`: Contains the Telegram bot logic, including message handling and command processing.
- `audio_processor.py`: Handles audio file processing, including downloading and converting voice messages.
- `llm_processor.py`: Contains the logic for generating responses using the LLM.
- `speech_to_text.py`: Handles audio transcription using Whisper.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `.env`: Environment variables for configuration (e.g., Telegram bot token).
- `README.md`: Documentation for the project.

## Quick Start Guide MacOS

### 0. Update Prompt

Before running the bot, you can customize the system prompt in [llm_processor.py](/llm_processor.py:40) to tailor the bot's responses to your needs. The default prompt is designed for interview scenarios, but you can modify it to suit other contexts.

### 1. Install Dependencies

```bash
# 1. Install Homebrew (if not yet installed)
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Adding Homebrew to PATH (for Apple Silicon)
$ echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
$ source ~/.zshrc

# Install ffmpeg
$ brew install ffmpeg

# 2. Install Python dependencies:
$ pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```plaintext
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 3. Run the Application

```bash
$ python main.py
```

### 4. Models Download

- **Mistral-7B** model, will download automatically when you run the application for the first time. The model is approximately 7 GB in size, so ensure you have enough disk space.
- **Whisper model** will also be downloaded automatically when you run the application for the first time. The model size varies based on the selected model size (e.g., tiny, base, small, medium, large, turbo).

## Whisper (OpenAI)

The leading open-source solution, used in 90% of local ASR (Automatic Speech Recognition) projects.

**Key Features:**
- Automatically detects language, adds punctuation, and capitalizes text (even for complex structures).
- Supports 100+ languages.
- Works fully offline after installation.
- Multiple model sizes: from tiny (39 MB) for low-end PCs to large-v3 (10+ GB) for maximum accuracy.

## Mistral-7B

Mistral-7B is a powerful open-source LLM that can be run locally. It is designed for high performance and supports various tasks, including question answering and text generation.

## License

This project is licensed under the Apache License Version 2.0 License. See the [LICENSE](LICENSE) file for details.
