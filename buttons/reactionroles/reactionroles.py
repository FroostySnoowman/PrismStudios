import discord
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

class ReactionRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='📣', label='Announcements Ping', style=discord.ButtonStyle.gray, custom_id='rr:1')
    async def announcements(self, interaction: discord.Interaction, button: discord.ui.Button):
        announcements = discord.utils.get(interaction.guild.roles, id=1047265460787363903)
        header = discord.utils.get(interaction.guild.roles, id=1047265485055594528)
        if announcements in interaction.user.roles:
            await interaction.user.remove_roles(announcements)
            await interaction.response.send_message("You have opt out of getting Announcement notification pings!", ephemeral=True)
        else:
            try:
                await interaction.user.add_roles(header)
            except:
                pass
            await interaction.user.add_roles(announcements)
            await interaction.response.send_message('You have opt into getting Announcement notification pings!', ephemeral=True)

    @discord.ui.button(emoji='💰', label='Giveaways Ping', style=discord.ButtonStyle.gray, custom_id='rr:2')
    async def giveaways(self, interaction: discord.Interaction, button: discord.ui.Button):
        giveaways = discord.utils.get(interaction.guild.roles, id=1044756018204262480)
        header = discord.utils.get(interaction.guild.roles, id=1047265485055594528)
        if giveaways in interaction.user.roles:
            await interaction.user.remove_roles(giveaways)
            await interaction.response.send_message("You have opt out of getting Giveaways notification pings!", ephemeral=True)
        else:
            try:
                await interaction.user.add_roles(header)
            except:
                pass
            await interaction.user.add_roles(giveaways)
            await interaction.response.send_message('You have opt into getting Giveaways notification pings!', ephemeral=True)

    @discord.ui.button(emoji='📈', label='Updates Ping', style=discord.ButtonStyle.gray, custom_id='rr:3')
    async def updates(self, interaction: discord.Interaction, button: discord.ui.Button):
        updates = discord.utils.get(interaction.guild.roles, id=1032082933353291877)
        header = discord.utils.get(interaction.guild.roles, id=1047265485055594528)
        if updates in interaction.user.roles:
            await interaction.user.remove_roles(updates)
            await interaction.response.send_message("You have opt out of getting Updates notification pings!", ephemeral=True)
        else:
            try:
                await interaction.user.add_roles(header)
            except:
                pass
            await interaction.user.add_roles(updates)
            await interaction.response.send_message('You have opt into getting Updates notification pings!', ephemeral=True)

class ReactionRolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(ReactionRoles())

async def setup(bot):
    await bot.add_cog(ReactionRolesCog(bot), guilds=[discord.Object(id=guild_id)])