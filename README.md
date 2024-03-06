# Telegram AI Chatbot

This project is a Telegram bot that leverages the OpenAI's GPT-3 model to conduct conversations in a human-like manner. It's capable of understanding user inputs and generating appropriate responses. The bot also features a state management system to handle complex user interactions.

## Project Structure

The Telegram bot project has the following directory and file structure:

```plaintext
telegram-bot/
├── handlers/             # Handlers for different bot commands and conversation states
│   ├── __init__.py       # Initializes the handlers package
│   ├── ai.py             # AI functionalities, including conversations powered by GPT-3
│   ├── buttons.py        # Keyboard button layouts for user interaction
│   ├── responses.py      # Response handling for user inputs
│   └── other.py          # Additional functionalities
├── Bot.py                # Main bot script that sets up and runs the bot
├── DATABASE.db           # Database for storing conversation logs and other data
├── RUN.bat               # Batch script to set tokens and run the bot
└── connection.py         # Bot's connection setup and dispatcher configuration
```

### Bot.py

`Bot.py` is the main script that initializes the bot, sets up conversation states, and starts polling for messages. It utilizes the dispatcher from `aiogram` to manage the flow of the conversation based on user input.

### DATABASE.db

A SQLite database file that holds logs, user interactions, and bot responses. This allows the bot to learn from past interactions and improve the conversation experience.

### RUN.bat

A batch script for Windows that sets the necessary environment variables, such as your Telegram Bot Token and OpenAI API Key, and runs the bot. You need to replace placeholder texts with your actual credentials.

### connection.py

Configures the bot with the Telegram API token, initializes logging, and sets up the dispatcher and storage mechanisms.

### Handlers Module

This module contains various scripts that define the bot's behavior:

- `ai.py`: Handles the integration with OpenAI's GPT-3 for generating conversation replies.
- `buttons.py`: Manages the construction of custom keyboard layouts for user interaction.
- `responses.py`: Manages the bot's responses to user messages, including storing new interactions in the database for learning purposes.
- `other.py`: A placeholder for any additional features you want to implement in the future.

## Installation and Usage

Before running the bot, make sure you have Python installed and the required libraries are set up.

### Prerequisites

- Python 3.x
- `aiogram` library
- `openai` library
- Additional libraries as needed

### Setup

1. Clone the repository to your local machine.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Set your Telegram Bot Token and OpenAI API Key in `RUN.bat`.
4. Execute `RUN.bat` to start the bot on Windows.

## Features

- **AI-Powered Conversations**: Engage with users in natural language, powered by OpenAI's GPT-3.
- **State Management**: Track conversation states to provide context-aware responses.
- **Interactive Buttons**: Use custom keyboard layouts for streamlined user interactions.
- **Learning Capability**: Store and retrieve user interactions to improve response accuracy over time.
- **Scalability**: Easily expand the bot's capabilities by adding new handlers in the `handlers` module.

## Contributing

Your contributions are welcome! If you have ideas for improvements or new features, feel free to fork the repository, implement your changes, and submit a pull request.

## License

This project is open-sourced under the MIT License. See the LICENSE file in the repository for more details.
