@echo off
rem RUN.bat: Batch script to set environment variables and start the bot.
rem Sets Telegram and OpenAI tokens and runs the main Python script.

rem Set environment variables for Telegram and OpenAI API tokens.
set TOKEN=WRITE_YOUR_TOKEN_HERE 
set OPEN_AI_TOKEN=WRITE_YOUR_TOKEN_HERE

rem Execute the main Python script to run the bot.
python Bot.py

rem Pause the command prompt to view any output messages.
pause
