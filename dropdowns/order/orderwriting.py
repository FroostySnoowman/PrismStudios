import discord
import yaml
from discord.ext import commands

from modals.order import Order

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

class OrderWritingDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Writer'),
        ]

        super().__init__(placeholder="Select an option!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        await interaction.response.send_modal(Order(category))

class OrderWritingDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(OrderWritingDropdown())

class OrderWritingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(OrderWritingCog(bot), guilds=[discord.Object(id=guild_id)])