from discord.ext import commands
import os
import discord

from lib.Variables import Variables
from lib.Logger import Logger
log = Logger(logfile = "CodingChallengeBot.log")

class CodingChallengeBot(commands.Bot):
    def __init__(self):
        super().__init__() # command_prefix = "!" --> doesnt work
        self.var = Variables(".env")

    async def on_ready(interaction):
        log.info(f"Discord version: v{discord.__version__}")
        log.info(f'Logged in as {interaction.user}')

    def load_extensions(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
                log.info(f"Loaded cogs.{filename[:-3]}")

if __name__ == "__main__":
    client = CodingChallengeBot()
    client.load_extensions()
    client.run(client.var.token) # run the bot with the token