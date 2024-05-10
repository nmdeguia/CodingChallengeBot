import discord
#from discord import app_commands
from discord.ext import commands
from discord.enums import ChannelType
from discord import option

import os
import dotenv

from lib.WebTools import WebTools
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
    @commands.slash_command(name = "dbg_problem")
    @commands.is_owner()
    async def dbg_problem(self, interaction):
        number = self.__get_problem_number()
        log.info(f"Problem {number} requested by {interaction.user.name}")
        await self.__post_problem(interaction, number)
        await self.__post_guidelines(interaction)
        await self.__create_post_discussion_thread(interaction, number)

    @commands.slash_command(name = "problem")
    @commands.slash_command(description = "Request a new problem (1 per day only)")
    async def problem(self, interaction):
        number = self.__get_problem_number()
        log.info(f"Problem {number} requested by {interaction.user.name}")
        if self.__is_new_day_today():
            await self.__post_problem(interaction, number)
            await self.__post_guidelines(interaction)
            await self.__create_post_discussion_thread(interaction, number)
            self.__inc_problem_number()
            self.var.update("DATE", str(log.datestamp()))
            self.var.reload()
        else:
            await interaction.respond(f"Problem {number} already posted for today.\n"\
                "**/current_problem** to show current problem\n"\
                "**/new_problem** to fetch new problem")
        
    @commands.slash_command(name = "new_problem")
    @commands.slash_command(description = "Force request a new problem")
    async def new_problem(self, interaction):
        number = self.__get_problem_number(force_next=True)
        log.info(f"Problem {number} requested by {interaction.user.name} (new)")
        await self.__post_problem(interaction, number)
        await self.__post_guidelines(interaction)
        await self.__create_post_discussion_thread(interaction, number)
        self.__inc_problem_number()
        
    @commands.slash_command(name = "show_problem")
    @commands.slash_command(description = "Show problem (does not increment current daily problem)")
    @option(name = "number", required = True)
    async def show_problem(self, interaction, number: int):
        log.info(f"Problem {number} requested by {interaction.user.name} (get)")
        await self.__post_problem(interaction, number)
        
    @commands.slash_command(name = "current_problem")
    @commands.slash_command(description = "Show current problem (does not increment current daily problem)")
    async def current_problem(self, interaction):
        number = self.__get_problem_number()
        log.info(f"Problem {number} requested by {interaction.user.name}")
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
            
    def __fetch_problem_ss(self, number):
        web_link = f"{self.var.problem_source}={number}"
        save_path = f"{self.var.problem_images}/problem_{number}.png"
        utils = WebTools()
        utils.screenshot_by_id(web_link, save_path, element_id="content")
        log.info(f"Saved image: {save_path}")
    
    # Check if current problem is already posted
    def __is_new_day_today(self):
        self.var.reload()
        # self.var.date is the last date posted for a new problem
        if log.datestamp() != str(self.var.date):
            return True
        else:
            return False
                        
    async def __post_problem(self, interaction, number):
        try:
            await interaction.respond(
                f"**Problem {number}**: <{self.var.problem_source}={number}>",
                file=discord.File(f"{self.var.problem_images}/problem_{number}.png"))
        except:
            await interaction.response.defer(ephemeral=False)
            self.__fetch_problem_ss(number)
            await interaction.respond(
                f"**Problem {number}**: <{self.var.problem_source}={number}>",
                file=discord.File(f"{self.var.problem_images}/problem_{number}.png"))
        log.info(f"Problem {number} posted")
        
    async def __post_guidelines(self, interaction):        
        await interaction.send(
            "To submit your answers, use the command **/submit**. "\
            "You can resubmit an answer with the same command. "\
            "A post discussion thread will be created where you "\
            "can post your algorithms, codes, and discussions.")
        
    async def __post_command_help(self, interaction):
        await interaction.send(
            "Commands:\n\n"\
            "**/problem**, **/new_problem**, **/show_problem** -- fetch problems\n"\
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