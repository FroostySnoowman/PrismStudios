import discord
import time
import yaml
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from buttons.reactionroles.reactionroles import ReactionRoles

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

launch_time = datetime.utcnow()

class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.add_view(ReactionRoles())

    @app_commands.command(name="roles", description="Sends the button roles panel!")
    async def roles(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Reaction Roles",
            description=
            f"Click the buttons below to add/remove roles!",
            color=discord.Color.orange())
        await interaction.channel.send(embed=embed, view=ReactionRoles())
        await interaction.response.send_message("Sent!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RolesCog(bot), guilds=[discord.Object(id=guild_id)])