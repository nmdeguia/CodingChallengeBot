import discord
from discord.ext import commands
from discord import option

import os
import dotenv

from lib.Variables import Variables
from lib.Submission import Submission
from lib.Submission import SubmissionBox
from lib.Logger import Logger
log = Logger(logfile = "app.log", shared = True, identifier = __name__[5:])

class Scoreboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.var = Variables(".env")

    """
    App slash commands wrappers, these will appear on the discord
    when the user starts a message with '/'. Keep functions simple,
    and call subroutines to do the work instead.
    """
    @commands.slash_command(name = "submission_box")
    async def submission_box(self, interaction):
        player_id = f"({interaction.guild.id}){interaction.user.name}"
        submission_modal = SubmissionBox(title="Submit Problem Solution")
        await interaction.send_modal(submission_modal)
        await submission_modal.wait()
        submission = submission_modal.submission
        timestamp_raw, timestamp = log.timestamp_raw()
        log.info(f"({player_id}) Submitted at {log.timestamp()}")
        log.info(f"({player_id}) Problem number: {submission.problem_number}")
        log.info(f"({player_id}) Language: {submission.language}")
        log.info(f"({player_id}) Total lines: {submission.total_lines}")
        log.info(f"({player_id}) Total runtime: {submission.total_runtime}")
        is_correct = self.__check_player_answer(submission.problem_number, submission.answer)
        if is_correct == True:
            await interaction.respond("Answer is correct. Submission recorded.")
            log.info(f"({player_id}) Answer correct")
            self.__record_player_submission(
                player = player_id, 
                submission = submission, 
                timestamp_raw = timestamp_raw, 
                timestamp = timestamp)
        else:
            await interaction.respond("Answer is incorrect. Please try again.")
            log.info(f"({player_id}) Answer incorrect")
            
    # Submit command but using options only, submit_modal uses full modal dialogue box
    @commands.slash_command(name = "submit")
    @option("problem", required=True)
    @option("answer", required=True)
    @option("language", required=True)
    @option("total_lines", required=True)
    @option("total_runtime", required=True)
    async def submit(self, 
                     interaction,
                     problem: int,
                     answer: str,
                     language: str,
                     total_lines: int,
                     total_runtime: float):
        player_id = f"({interaction.guild.id}){interaction.user.name}"
        timestamp_raw, timestamp = log.timestamp_raw()
        submission = Submission(problem, answer, language, total_lines, total_runtime)
        log.info(f"({player_id}) Submitted at {log.timestamp()}")
        log.info(f"({player_id}) Problem number: {problem}")
        log.info(f"({player_id}) Language: {language}")
        log.info(f"({player_id}) Total lines: {total_lines}")
        log.info(f"({player_id}) Total runtime: {total_runtime}")
        is_correct = self.__check_player_answer(submission.problem_number, submission.answer)
        if is_correct == True:
            await interaction.respond("Answer is correct. Submission recorded.")
            log.info(f"({player_id}) Answer correct")
            self.__record_player_submission(
                player = player_id, 
                submission = submission, 
                timestamp_raw = timestamp_raw, 
                timestamp = timestamp)
        else:
            await interaction.respond("Answer is incorrect. Please try again.")
            log.info(f"({player_id}) Answer incorrect")
            
    @commands.slash_command(name = "scoreboard")
    async def scoreboard(self, interaction):
        log.info(f"Scoreboard requested by: {interaction.user.name}")
        await interaction.respond("Command is currently in development.")
        
    @commands.slash_command(name = "global_scoreboard")
    async def global_scoreboard(self, interaction):
        log.info(f"Global scoreboard requested by: {interaction.user.name}")
        await interaction.respond("Command is currently in development.")

    @commands.slash_command(name = "personal_stats")
    async def personal_stats(self, interaction):
        log.info(f"Personal stats requested by: {interaction.user.name}")
        await interaction.respond("Command is currently in development.")
        
    """
    Private methods to be used within the class only, this serves as the
    engine for the commands in the cog defined above.
    """
    def __check_player_answer(self, problem_number, answer):
        answer_key = self.__load_answer_key(self.var.problem_anskey)
        correct_answer = answer_key[f"Problem {problem_number}"]
        return True if correct_answer == answer else False
            
    def __load_answer_key(self, path):
        answer_key = dict()
        try:
            with open(self.var.problem_anskey, "r") as file:
                lines = file.readlines()
                for line in lines:
                    answer_key.update({line.split(".")[0].strip():line.split(".")[1].strip()})
        except:
            log.error(f"No answer key found: {self.var.problem_anskey}")    
        return answer_key
        
    def __record_player_submission(self, player, submission, timestamp_raw, timestamp):
        with open(f"{self.var.players}/{player}", "a") as file:
            file.write(f"{submission.problem_number},")
            file.write(f"{submission.answer},")
            file.write(f"{submission.language},")
            file.write(f"{submission.total_lines},")
            file.write(f"{submission.total_runtime},")
            file.write(f"{timestamp_raw},")
            file.write(f"{timestamp}\n")
        log.info(f"({player}) Result recorded")
        
    def __fetch_player_stats(self, path): pass
    
    def __fetch_player_leaderboard(self, server, path):
        # Implement leaderboard stats here
        pass

def setup(bot):
    bot.add_cog(Scoreboard(bot))