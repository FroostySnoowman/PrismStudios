import discord
import asyncio
import aiosqlite
import yaml
from discord.ext.commands import CommandNotFound
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

token = data["General"]["TOKEN"]
guild_id = data["General"]["GUILD_ID"]

intents = discord.Intents.all()
intents.message_content = True

initial_extensions = ['src.admin.admin',
                      'src.freelancer.freelancer',
                      'src.join.joinevent',
                      'src.paypal.pay',
                      'src.tickets.applications',
                      'src.tickets.commissions',
                      'src.tickets.tickets',
                      'src.utils.reactionroles',
                      'src.utils.utils']

class TicketBotView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Test', style=discord.ButtonStyle.green, custom_id='test:1')
    async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Testing the system...', ephemeral=True)

watching = discord.Activity(name='PrismStudios', type=discord.ActivityType.watching)
class TicketBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('-'), owner_id=503641822141349888, intents=intents, activity=watching, status=discord.Status.online)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(TicketBotView())
            self.persistent_views_added = True

        print(f'Signed in as {self.user}')

        await self.tree.sync(guild=discord.Object(id=guild_id))
        await self.tree.sync()

    async def setup_hook(self):
        for extension in initial_extensions:
            await self.load_extension(extension)

client = TicketBot()
client.remove_command('help')

@client.command()
@commands.is_owner()
async def delete(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE quotes;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def delete2(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE commissions;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def delete3(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE questions;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def delete4(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE balance;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def delete5(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE freelancer;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def delete6(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE applications;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def delete7(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE invoices;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE quotes (
        commissions_channel INTEGER,
        member_id INTEGER,
        quote_message_id INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def sqlite2(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE commissions (
        channel_id INTEGER,
        role_id INTEGER,
        freelancer_message_id INTEGER,
        freelancer_id INTEGER,
        amount INTEGER,
        claim_id INTEGER,
        commission_manager_id INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def sqlite3(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE questions (
        commissions_channel INTEGER,
        member_id INTEGER,
        question_message_id
    )""")
    await cursor.close()
    await db.commit()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def sqlite4(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE balance (
        freelancer_id INTEGER,
        amount INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def sqlite5(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE freelancer (
        freelancer_id INTEGER,
        title STRING,
        description STRING,
        portfolio STRING,
        paypal STRING
    )""")
    await cursor.close()
    await db.commit()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def sqlite6(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE applications (
        applicant_id INTEGER,
        channel_id INTEGER,
        roles STRING,
        claim_id INTEGER,
        application_reviewer INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def sqlite7(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE invoices (
        method STRING,
        message_id INTEGER,
        pay_message_id INTEGER,
        invoice_id STRING,
        subtotal INTEGER,
        fees INTEGER,
        total INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

#\\\\\\\\\\\\Error Handler////////////
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

client.run(token)