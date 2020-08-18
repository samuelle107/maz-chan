import discord
import os
import json
from discord.ext import commands
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

CUSTOM_COMMAND_LIST = dict()


# create CUSTOM_COMMANDS_FILE_PATH variable in .env file
def load_commands() -> str:
    global CUSTOM_COMMAND_LIST
    with open(os.getenv("CUSTOM_COMMANDS_FILE_PATH"), "r") as f:
        CUSTOM_COMMAND_LIST = json.load(f)
    return CUSTOM_COMMAND_LIST


def save_command(command: str, text: str):
    global CUSTOM_COMMAND_LIST
    CUSTOM_COMMAND_LIST[command] = text
    with open(os.getenv("CUSTOM_COMMANDS_FILE_PATH"), "w") as f:
        json.dump(CUSTOM_COMMAND_LIST, f)


def remove_command(command: str) -> str:
    global CUSTOM_COMMAND_LIST
    del CUSTOM_COMMAND_LIST[command]
    with open(os.getenv("CUSTOM_COMMANDS_FILE_PATH"), "w") as f:
        json.dump(CUSTOM_COMMAND_LIST, f)
    return command
