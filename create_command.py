import discord
import os
import json
import mysql.connector
from discord.ext import commands
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

con = mysql.connector.connect(user=os.getenv("MYSQL_USERNAME"),
                              password=os.getenv("MYSQL_PASSWORD"),
                              host=os.getenv("MYSQL_HOST"),
                              database=os.getenv("MYSQL_DB"),
                              charset="utf8",
                              use_unicode=True)
CUSTOM_COMMAND_LIST = dict()


def load_commands() -> str:
    global CUSTOM_COMMAND_LIST
    cur = con.cursor()
    sql = "SELECT (command, command_text) FROM custom_commands"
    cur.execute(sql)
    custom_commands = cur.fetchall()
    for (command, command_text) in custom_commands:
        CUSTOM_COMMAND_LIST[command] = command_text
    cur.close()
    return CUSTOM_COMMAND_LIST


def save_command(command: str, text: str):
    global CUSTOM_COMMAND_LIST
    CUSTOM_COMMAND_LIST[command] = text
    cur = con.cursor()
    sql = f"INSERT INTO custom_commands (command, command_text) VALUES ({command}, {text})"
    cur.execute(sql)
    cur.close()


def remove_command(command: str) -> str:
    global CUSTOM_COMMAND_LIST
    del CUSTOM_COMMAND_LIST[command]
    cur = con.cursor()
    sql = f"DELETE FROM custom_commands WHERE command = '{command}'"
    cur.execute(sql)
    cur.close()
    return command
