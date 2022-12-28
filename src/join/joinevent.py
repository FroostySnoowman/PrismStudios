import discord
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

member_divider_role_id = data["Roles"]["MEMBER_DIVIDER_ROLE_ID"]
announcements_ping_role_id = data["Roles"]["ANNOUNCEMENTS_PING_ROLE_ID"]
giveaways_ping_role_id = data["Roles"]["GIVEAWAYS_PING_ROLE_ID"]
updates_ping_role_id = data["Roles"]["UPDATES_PING_ROLE_ID"]

class JoinEventCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member: discord.Member):
        guild = self.bot.get_guild(guild_id)
        try:
            member_divider = guild.get_role(member_divider_role_id)
            announcements_ping = guild.get_role(announcements_ping_role_id)
            giveaways_ping = guild.get_role(giveaways_ping_role_id)
            updates_ping = guild.get_role(updates_ping_role_id)
            await member.add_roles(member_divider)
            await member.add_roles(announcements_ping)
            await member.add_roles(giveaways_ping)
            await member.add_roles(updates_ping)
        except:
            pass

async def setup(bot):
    await bot.add_cog(JoinEventCog(bot))