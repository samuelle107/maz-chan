import asyncio
# import create_command
import datetime
import discord
import os
import logging
import mysql.connector
from discord.ext import commands
from dotenv import load_dotenv
from subreddit_scrapper import get_scraped_submissions
from db_helper import get_all, get_all_conditional, insert, remove, does_exist

logging.getLogger().setLevel(logging.INFO)

load_dotenv()

# Secret variable. Do not push to github
# Either ask me for the token or make your own bot
# this will go in .env
# DISCORD_BOT_TOKEN=xxxx
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
# These values are found by right clicking on the channel and then clicking copy ID
WELCOME_CHANNEL_ID = 744054264640569355
BOT_COMMANDS_CHANNEL_ID = 744057858886336552
BOT_TESTING_CHANNEL_ID = 744065526023847957
GENERAL_CHAT_CHANNEL_ID = 744030856196390994
RULES_CHANNEL_ID = 744047107866099813
MECH_MARKET_CHANNEL_ID = 746622430927257721

client = commands.Bot(command_prefix='!')

con_info = dict(
    user=os.getenv("MYSQL_USERNAME"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    database=os.getenv("MYSQL_DB"),
    charset="utf8",
    use_unicode=True
)

def query_keywords() -> list:
    con = mysql.connector.connect(**con_info)
    results = get_all(con, "keywords")
    con.close()
    return list(result[0] for result in results)

def query_users_by_keywords(keyword: str) -> list:
    con = mysql.connector.connect(**con_info)
    results = get_all_conditional(con, "keywords_users", ["keyword_id"], [keyword])
    con.close()
    return list(result[1] for result in results)

@client.event
async def on_ready():
    bot_testing_channel = client.get_channel(BOT_TESTING_CHANNEL_ID)
    mechmarket_channel = client.get_channel(MECH_MARKET_CHANNEL_ID)

    logging.info(f'{str(datetime.datetime.now())}: Bot is ready')
    await bot_testing_channel.send("MAZ Chan is ready!")

    while True:
        con = mysql.connector.connect(**con_info)

        keywords = query_keywords()

        logging.info(f'{str(datetime.datetime.now())}: Checking for new submissions: ')
        submissions = get_scraped_submissions("MechMarket")

        for submission in submissions:
            post_does_exist = does_exist(con, "mechmarket_posts", "post_id", submission.id)

            if not post_does_exist:
                logging.info(f'{str(datetime.datetime.now())}: Found new submission: {submission.title[:100]}')
                insert(con, "mechmarket_posts", ["post_id", "title"], [submission.id, submission.title[:100]])

                matching_keywords = list(filter(lambda keyword: keyword.lower() in submission.title.lower(), keywords))
                mentions = []

                for matching_keyword in matching_keywords:
                    users = query_users_by_keywords(matching_keyword)
                    for uid in users:
                        mentions.append(client.get_user(uid).mention)

                await mechmarket_channel.send(f'```{submission.title}```\n {", ".join(mentions)} \n\n{submission.url}\n\n')

        logging.info(f'{str(datetime.datetime.now())}: Finished scraping')
        con.close()
        await asyncio.sleep(60)


# Called when a new member joins
# Will add them to a refugee role, send a gif, and message
@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    url = "https://imgur.com/ANEL8c3"
    role = discord.utils.get(member.guild.roles, name="Refugee")

    await member.add_roles(role)
    await channel.send(url)
    await channel.send(
        f'Irasshaimase, {member.mention} \n\nRead the rules at <#{RULES_CHANNEL_ID}>'
    )


# # called when any message is sent
# # this event is used to check if custom command is used
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content[0] == "~" and message.content[
#             1:] in create_command.CUSTOM_COMMAND_LIST.keys():
#         await message.channel.send(
#             create_command.CUSTOM_COMMAND_LIST[message.content[1:]])


# Used to paste copy pasta
# !egghead
@client.command()
async def egghead(ctx):
    await ctx.send(
        "https://media.discordapp.net/attachments/668640100367990793/714849219231613029/unknown.png"
    )


# Used to paste copy pasta
# !prawn
@client.command()
async def prawn(ctx):
    await ctx.send("ANOTHA PRAWN ON THE BAWBIE")


@client.command()
async def test(ctx):
    await ctx.send("hello")

    
# Used to clone a message to a different channel
# !cl <number of messages ago> <#channel>
@client.command()
async def cl(ctx, *args):
    messages_ago = int(args[0]) + 1
    target_channel_id = int("".join([(s) for s in args[1] if s.isdigit()]))

    channel = client.get_channel(target_channel_id)
    messages = await ctx.history(limit=messages_ago).flatten()
    message = f"{messages[-1].author.mention} said: {messages[-1].attachments[0].url if len(messages[-1].attachments) > 0 else messages[-1].content}"

    await channel.send(message)

# Used to clone a message by id
# !clid id <#channel>
@client.command()
async def clid(ctx, *args):
    id = int(args[0])
    target_channel_id = int("".join([(s) for s in args[1] if s.isdigit()]))
    channel = client.get_channel(target_channel_id)
    message_data = await ctx.channel.fetch_message(id)

    message = f"{message_data.author.mention} said: {message_data.attachments[0].url if len(message_data.attachments) > 0 else message_data.content}"
    await channel.send(message)


@client.command()
async def gugl(ctx, *args):
    base_url = "https://www.google.com/search?"
    query = f"q={'+'.join(args)}"
    await ctx.send(base_url + query)

@client.command()
async def add_keyword(ctx, *arg):
    keyword = " ".join(arg)

    con = mysql.connector.connect(**con_info)
    insert(con, "keywords", ["keyword_id"], [keyword])
    insert(con, "users", ["user_id"], [ctx.message.author.id])
    keywords_users_id = insert(con, "keywords_users", ["user_id", "keyword_id"], [ctx.message.author.id, keyword])
    con.close()

    if keywords_users_id != -1:
        await ctx.send(f"Successfully added: {keyword}")
    else:
        await ctx.send(f"Failled to add: {keyword}")


@client.command()
async def remove_keyword(ctx, *arg):
    keyword = " ".join(arg)

    con = mysql.connector.connect(**con_info)
    num_removed = remove(con, "keywords_users", ["user_id", "keyword_id"], [ctx.message.author.id, keyword])
    con.close()

    if num_removed != 0:
        await ctx.send(f"Sucessfully deleted: {keyword}")
    else:
        await ctx.send(f"Failed to delete: {keyword}")

@client.command()
async def get_keywords(ctx):
    con = mysql.connector.connect(**con_info)
    results = get_all_conditional(con, "keywords_users", ['user_id'], [ctx.message.author.id])

    await ctx.send(f"Your keywords are: {', '.join(list(result[2] for result in results))}")
    con.close()


# create a new custom command
@client.command()
async def ncc(ctx, *args):
    command_name = args[0]
    if command_name in create_command.CUSTOM_COMMAND_LIST.keys():
        await ctx.send(
            f"`{command_name}` already exists. Are you sure you want to continue (y/n)"
        )
        msg = await client.wait_for(
            'message',
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            and m.content in ['y', 'n'])
        if msg.content == 'n':
            await ctx.send("**Aborting...**")
            return
    await ctx.send(
        f"please enter the text the command `{command_name}` should display when it is called"
    )
    msg = await client.wait_for(
        'message',
        check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    create_command.save_command(command_name, msg.content)


# list all custom commands
@client.command()
async def lcc(ctx):
    formatted_string = ""
    for k, v in create_command.CUSTOM_COMMAND_LIST:
        formatted_string += f"`{k}`: `{v}`\n"
    await ctx.send(formatted_string)


# remove a custom command
@client.command()
async def rcc(ctx, *args):
    command_name = args[0][1:]
    print(command_name)
    if command_name in create_command.CUSTOM_COMMAND_LIST.keys():
        create_command.remove_command(command_name)
        await ctx.send(f"Successfully deleted command `{command_name}`")
    else:
        await ctx.send(f"No such command `{command_name}`")

client.run(DISCORD_BOT_TOKEN)

# print(query_users_by_keywords("9009"))
