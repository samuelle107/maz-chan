import create_command
import datetime
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Secret variable. Do not push to github
# Either ask me for the token or make your own bot
# this will go in .env
# DISCORD_BOT_TOKEN=xxxx
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
# These values are found by right clicking on the channel and then clicking copy ID
WELCOME_CHANNEL_ID =  744054264640569355
BOT_COMMANDS_CHANNEL_ID =  744057858886336552
BOT_TESTING_CHANNEL_ID =  744065526023847957
GENERAL_CHAT_CHANNEL_ID = 744030856196390994
RULES_CHANNEL_ID =  744047107866099813

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    channel = client.get_channel(BOT_TESTING_CHANNEL_ID)
    await channel.send("MAZ Chan is ready!")


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


# Called when message is sent
@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == client.user:
        return

    if message.content[0] == "~" and message.content[1:] in create_command.CUSTOM_COMMAND_LIST.keys():
        print(create_command.CUSTOM_COMMAND_LIST)
        await message.channel.send(
            create_command.CUSTOM_COMMAND_LIST[message.content[1:]])


@client.command()
async def new_command(ctx, *args):
    print(f"got command {args[0]}")
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


@client.command()
async def list_custom_commands(ctx):
    formatted_string = ""
    for k, v in create_command.CUSTOM_COMMAND_LIST:
        formatted_string += f"`{k}`: `{v}`\n"
    await ctx.send(formatted_string)

@client.command()
async def remove_command(ctx, *args):
    command_name = args[0][1:]
    print(command_name)
    if command_name in create_command.CUSTOM_COMMAND_LIST.keys():
        create_command.remove_command(command_name)
        await ctx.send(f"Successfully deleted command `{command_name}`")
    else:
        await ctx.send(f"No such command `{command_name}`")


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


# Used to clone a message to a different channel
# !clone <number of messages ago> <#channel>
@client.command()
async def clone(ctx, *args):
    messages_ago = int(args[0]) + 1
    target_channel_id = int("".join([(s) for s in args[1] if s.isdigit()]))

    channel = client.get_channel(target_channel_id)
    messages = await ctx.history(limit=messages_ago).flatten()
    message = f"{messages[-1].author.mention} said: {messages[-1].attachments[0].url if len(messages[-1].attachments) > 0 else messages[-1].content}"

    await channel.send(message)


@client.command()
async def gugl(ctx, *args):
    base_url = "https://www.google.com/search?"
    query = f"q={'+'.join(args)}"
    await ctx.send(base_url + query)


create_command.load_commands()
client.run(DISCORD_BOT_TOKEN)
