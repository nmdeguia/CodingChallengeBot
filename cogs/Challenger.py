import discord
#from discord import app_commands
from discord.ext import commands
from discord.enums import ChannelType
from discord import option

import os
import dotenv

from lib.Variables import Variables
from lib.Logger import Logger
log = Logger(logfile = "app.log", shared = True, identifier = __name__[5:])

class Challenger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.var = Variables(".env")
        
    """
    App slash commands wrappers, these will appear on the discord
    when the user starts a message with '/'. Keep functions simple,
    and call subroutines to do the work instead.
    """
    @commands.slash_command(name = "problem")
    async def problem(self, interaction):
        number = self.__get_problem_number()
        log.info(f"Problem {number} requested by {interaction.user.name}")
        if self.__is_new_day_today():
            await self.__post_problem(interaction, number)
            await self.__post_guidelines(interaction)
            await self.__create_post_discussion_thread(interaction, number)
            self.__inc_problem_number()
        else:
            await interaction.respond(f"Problem {number} already posted for today.\n"\
                "**/current_problem** to show current problem\n"\
                "**/new_problem** to fetch new problem")
        
    @commands.is_owner()
    @commands.slash_command(name = "new_problem")
    async def new_problem(self, interaction):
        number = self.__get_problem_number(force_next=True)
        log.info(f"New problem {number} requested by {interaction.user.name}")
        await self.__post_problem(interaction, number)
        await self.__post_guidelines(interaction)
        await self.__create_post_discussion_thread(interaction, number)
        self.__inc_problem_number()
        
    @commands.slash_command(name = "get_problem")
    @option(name = "number", required = True)
    async def get_problem(self, interaction, number: int):
        log.info(f"Get problem {number} requested by {interaction.user.name}")
        await self.__post_problem(interaction, number)
        
    @commands.slash_command(name = "current_problem")
    async def current_problem(self, interaction):
        number = self.__get_problem_number()
        log.info(f"Current problem {number} requested by {interaction.user.name}")
        await self.__post_problem(interaction, number)
                
    """
    Private methods to be used within the class only, this serves as the
    engine for the commands in the cog defined above.
    """
    def __get_problem_number(self, force_next = False):
        self.var.reload()
        if force_next == True or self.__is_new_day_today():
            return int(self.var.problem_number) + 1
        else:
            return int(self.var.problem_number)
        
    def __inc_problem_number(self): 
        self.var.update("PROBLEM_NUMBER", str(self.var.problem_number + 1))
        self.var.reload()
        log.info(f"Problem number updated {self.var.problem_number - 1} "\
            f"-> {self.var.problem_number}")
    
    # Check if current problem is already posted
    def __is_new_day_today(self):
        self.var.reload()
        # self.var.date is the last date posted for a new problem
        if log.datestamp() != str(self.var.date):
            self.var.update("DATE", str(log.datestamp()))
            self.var.reload()
            return True
        else:
            return False
            
    async def __post_problem(self, interaction, number):
        try:
            await interaction.respond(
                f"**Problem {number}**: <{self.var.problem_source}={number}>",
                file=discord.File(f"{self.var.problem_images}/problem_{number}.png"))
        except:
            log.warning(f"No image found: {self.var.problem_images}/problem_{number}.png")
            await interaction.respond(
                f"**Problem {number}**: <{self.var.problem_source}={number}>")
        log.info(f"Problem {number} posted")
        
    async def __post_guidelines(self, interaction):        
        await interaction.respond(
            "To submit your answers, use the command **/submit** or **/submission_box**. "\
            "A post discussion thread will be created where you "\
            "can post your algorithms, codes, and discussions.")
        
    async def __post_command_help(self, interaction):
        await interaction.respond(
            "Commands:\n\n"\
            "**/problem**, **/new_problem**, **/get_problem** -- fetch problems\n"\
            "**/submit**, **/submission_box** -- submit answers\n"\
            "**/scoreboard**, **/global_scoreboard**, **/personal_stats**\n")
            
    # Currently the documentation says only public threads are available
    # for unboosted servers. Creation of private threads will only be allowed
    # once the server is boosted to at least level 2. Alternative would be to 
    # just create a text channel and delete it afterwards, albeit a little messy.
    async def __create_post_discussion_thread(self, interaction, number):
        channel = interaction.channel        
        await channel.create_thread(
            name=f"Problem {number} Post Discussion",
            type=ChannelType.public_thread) # 🧠・
        
def setup(bot):
    bot.add_cog(Challenger(bot))