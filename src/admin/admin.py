import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

class AdminCog(commands.GroupCog, name="admin"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="view", description="Shows you information about a freelancer!")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.describe(member="Who's profile do you want to view?")
    @app_commands.default_permissions(administrator=True)
    async def view(self, interaction: discord.Interaction, member: discord.Member):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (member.id, ))
        a = await cursor.fetchone()
        cursor2 = await db.execute('SELECT * from balance WHERE freelancer_id=?', (member.id, ))
        b = await cursor2.fetchone()
        if a is None:
            await interaction.response.send_message('That member does not have any information to view!', ephemeral=True)
        else:
            if a[1] == 'null':
                title = "N/A"
            else:
                title = a[1]
            if a[2] == 'null':
                description = "N/A"
            else:
                description = a[2]
            if a[3] == 'null':
                portfolio = "N/A"
            else:
                portfolio = a[3]
            if a[4] == 'null':
                paypal = "N/A"
            else:
                paypal = a[4]
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            embed.add_field(name="Title", value=f"**{title}**", inline=True)
            embed.add_field(name="Description", value=f"**{description}**", inline=True)
            embed.add_field(name="Portfolio", value=f"**{portfolio}**", inline=True)
            embed.add_field(name="PayPal", value=f"**{paypal}**", inline=True)
            embed.add_field(name="Balance", value=f"**${b[1]:.2f}**", inline=True)
            embed.set_author(name=f"{member.name}'s Profile", icon_url=member.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCog(bot), guilds=[discord.Object(id=guild_id)])