import datetime
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
WELCOME_CHANNEL_ID = os.environ['WELCOME_CHANNEL_ID']
BOT_COMMANDS_CHANNEL_ID = os.environ['BOT_COMMANDS_CHANNEL_ID']
BOT_TESTING_CHANNEL_ID = os.environ['BOT_TESTING_CHANNEL_ID']
GENERAL_CHAT_CHANNEL_ID = os.environ['GENERAL_CHAT_CHANNEL_ID']
RULES_CHANNEL_ID = os.environ['RULES_CHANNEL_ID']

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    channel = client.get_channel(int(BOT_TESTING_CHANNEL_ID))
    await channel.send("MAZ Chan is ready!")

@client.event
async def on_member_join(member):
    channel = client.get_channel(int(WELCOME_CHANNEL_ID))
    url = "https://imgur.com/ANEL8c3"
    role = discord.utils.get(member.guild.roles, name="Refugee")

    await member.add_roles(role)
    await channel.send(url)
    await channel.send(f'Irasshaimase, {member.mention} \n\nRead the rules at <#{int(RULES_CHANNEL_ID)}>')

@client.command()
async def flame(ctx, member : discord.Member):
    channel = client.get_channel(int(GENERAL_CHAT_CHANNEL_ID))
    await channel.send(f"What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, {member.mention}.")

@client.command()
async def idiot(ctx, member : discord.Member):
    channel = client.get_channel(int(GENERAL_CHAT_CHANNEL_ID))
    await channel.send(f"You idiot, You absolute bafoon, You’ve made yourself a laughingstock, You uneducated monkey, Your stupidity is mindblowing to me, I cant believe you just made that statement, You absolute moron, You have acted like a total fool, a total clown, HONK HONK, Yeah thats you, {member.mention}")

@client.command()
async def egghead(ctx):
    await ctx.send("https://media.discordapp.net/attachments/668640100367990793/714849219231613029/unknown.png")

@client.command()
async def prawn(ctx):
    await ctx.send("ANOTHA PRAWN ON THE BAWBIE")

@client.command()
async def shutup(ctx, member : discord.Member):
    channel = client.get_channel(int(GENERAL_CHAT_CHANNEL_ID))
    await channel.send(f"I know you have something to say, and I know you are eager to say it, So I'll get straight to the point: Shut the fuck up Nobody wants to hear it, nobody will ever want to hear it, nobody cares! And the fact you thought someone might care is honestly baffling to me. I've actually polled the entire world: Here's a composite of the faces of everybody who wants you to shut the fuck up, It seems as if this is a composite of every human being on the planet, Interesting. Now for a composite of the faces that, want you to keep talking: Interesting it seems as if nothing has happened. Here's a world map, now here's the text \"shut the fuck up\", that's what you should do. But you know what? Maybe I am being a little too harsh here, I actually do have on good authority thanks to my polling data That there is at least one person that actually wants to hear you speak, its a little child in Mozambique and he- Ah, oh, he's dead? Sorry man, I guess nobody wants to hear you talk anymore, please, shut the fuck up, {member.mention}")

@client.command()
async def clone(ctx, *args):
    messages_ago = int(args[0]) + 1
    target_channel_id = args[1]
    target_channel_id = "".join([(s) for s in target_channel_id if s.isdigit()])

    channel = client.get_channel(int(target_channel_id))
    messages = await ctx.history(limit=messages_ago).flatten()

    await channel.send(f"{messages[-1].author.mention} said: {messages[-1].attachments[0].url if len(messages[-1].attachments) > 0 else messages[-1].content}")

client.run(DISCORD_BOT_TOKEN)