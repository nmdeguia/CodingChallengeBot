import discord

class Submission:
    def __init__(self,
                 problem_number = None,
                 answer = None,
                 language = None,
                 total_lines = None,
                 total_runtime = None):
        self.problem_number = problem_number
        self.answer = answer
        self.language = language
        self.total_lines = total_lines
        self.total_runtime = total_runtime
    
class SubmissionBox(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Problem number"))
        self.add_item(discord.ui.InputText(label="Answer"))
        self.add_item(discord.ui.InputText(label="Language used"))
        self.add_item(discord.ui.InputText(label="Total lines"))
        self.add_item(discord.ui.InputText(label="Total runtime (s)"))
        self.submission = Submission()
        
    async def callback(self, interaction: discord.Interaction):
        self.submission.problem_number = value=self.children[0].value
        self.submission.answer = value=self.children[1].value
        self.submission.language = value=self.children[2].value
        self.submission.total_lines = value=self.children[3].value
        self.submission.total_runtime = value=self.children[4].value
      
        embed = discord.Embed(title=f"Submission recorded")
        embed.add_field(name="Problem", value=self.children[0].value)
        embed.add_field(name="Language", value=self.children[2].value)
        embed.add_field(name="Total lines", value=self.children[3].value)
        embed.add_field(name="Total runtime (s)", value=self.children[4].value)
        await interaction.response.send_message(embeds=[embed])