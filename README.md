# MAZ Chan
### Background
What is the MAZ? The MAZ is not a place. It is not a thing. It is a common goal that people seek. It is the idea of freedom. MAZ Chan is used to help us achieve that goal.
### Serious Description
MAZ Chan is a discord bot for a server. It is built and maintained by members of that server.

## Setting Up
### Prerequisites
- git
- python3
- pip3
### Installation
1. Run `git clone https://github.com/samuelle107/maz-chan.git` at wherever you want to clone it.
2. Make a .env file at the root of the repository.
3. Add the content `DISCORD_BOT_TOKEN=xxx` to line 1. xxx is the bot token. Either ask me for it or make your own bot. Note, if you make your own bot, you need to change the channel IDs in `bot.py`. Add `MYSQL_USERNAME`, `MYSQL_PASSWORD`, `MYSQL_HOST`, and `MYSQL_DB` environment variables as well to the `.env` file. 
4. Run `pip3 install -r requirements.txt` to get all of the packages.
5. Run `python3 bot.py` to start the bot.

## Deployment
To deploy the code, you need access to push to my Heroku repository. Contact me for more information.
