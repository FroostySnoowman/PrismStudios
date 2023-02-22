import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
review_channel_id = data["Channels"]["REVIEW_CHANNEL_ID"]
commission_manager_role_id = data["Roles"]["COMMISSION_MANAGER_ROLE_ID"]

class ReviewOne(discord.ui.Modal, title='Review Freelancer'):

    review = discord.ui.TextInput(
        label='Review',
        placeholder='What is your review for the freelancer?',
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        freelancer = interaction.client.get_user(a[2])
        review_channel = interaction.guild.get_channel(review_channel_id)
        embed=discord.Embed(title=f"1 ⭐ Review For {freelancer}", 
        description=f"{self.review.value}", 
        color=discord.Color.orange())
        await review_channel.send(embed=embed)
        await interaction.response.send_message("Submitted!", ephemeral=True)
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewTwo(discord.ui.Modal, title='Review Freelancer'):

    review = discord.ui.TextInput(
        label='Review',
        placeholder='What is your review for the freelancer?',
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        freelancer = interaction.client.get_user(a[2])
        review_channel = interaction.guild.get_channel(review_channel_id)
        embed=discord.Embed(title=f"2 ⭐ Review For {freelancer}", 
        description=f"{self.review.value}", 
        color=discord.Color.orange())
        await review_channel.send(embed=embed)
        await interaction.response.send_message("Submitted!", ephemeral=True)
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewThree(discord.ui.Modal, title='Review Freelancer'):

    review = discord.ui.TextInput(
        label='Review',
        placeholder='What is your review for the freelancer?',
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        freelancer = interaction.client.get_user(a[2])
        review_channel = interaction.guild.get_channel(review_channel_id)
        embed=discord.Embed(title=f"3 ⭐ Review For {freelancer}", 
        description=f"{self.review.value}", 
        color=discord.Color.orange())
        await review_channel.send(embed=embed)
        await interaction.response.send_message("Submitted!", ephemeral=True)
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewFour(discord.ui.Modal, title='Review Freelancer'):

    review = discord.ui.TextInput(
        label='Review',
        placeholder='What is your review for the freelancer?',
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        freelancer = interaction.client.get_user(a[2])
        review_channel = interaction.guild.get_channel(review_channel_id)
        embed=discord.Embed(title=f"4 ⭐ Review For {freelancer}", 
        description=f"{self.review.value}", 
        color=discord.Color.orange())
        await review_channel.send(embed=embed)
        await interaction.response.send_message("Submitted!", ephemeral=True)
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewFive(discord.ui.Modal, title='Review Freelancer'):

    review = discord.ui.TextInput(
        label='Review',
        placeholder='What is your review for the freelancer?',
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        freelancer = interaction.client.get_user(a[2])
        review_channel = interaction.guild.get_channel(review_channel_id)
        embed=discord.Embed(title=f"5 ⭐ Review For {freelancer}", 
        description=f"{self.review.value}", 
        color=discord.Color.orange())
        await review_channel.send(embed=embed)
        await interaction.response.send_message("Submitted!", ephemeral=True)
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='⭐', label='1', style=discord.ButtonStyle.grey, custom_id='review:1')
    async def reviewone(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_modal(ReviewOne())

    @discord.ui.button(emoji='⭐', label='2', style=discord.ButtonStyle.grey, custom_id='review:2')
    async def reviewtwo(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_modal(ReviewTwo())

    @discord.ui.button(emoji='⭐', label='3', style=discord.ButtonStyle.grey, custom_id='review:3')
    async def reviewthree(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_modal(ReviewThree())

    @discord.ui.button(emoji='⭐', label='4', style=discord.ButtonStyle.grey, custom_id='review:4')
    async def reviewfour(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_modal(ReviewFour())

    @discord.ui.button(emoji='⭐', label='5', style=discord.ButtonStyle.grey, custom_id='review:5')
    async def reviewfive(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_modal(ReviewFive())


class CommissionsCog(commands.GroupCog, name="commission"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        self.bot.add_view(ReviewSystem())

    @app_commands.command(name="complete", description="Completes the commission!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def complete(self, interaction: discord.Interaction):
        commission_manager = discord.utils.get(interaction.guild.roles, id=commission_manager_role_id)
        if commission_manager in interaction.user.roles:
            if "order" in interaction.channel.name:
                db = await aiosqlite.connect('database.db')
                cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
                a = await cursor.fetchone()
                if a[2] != 'null':
                    if a[3] != 'null':
                        if a[6] != 'null':
                            cursor = await db.execute('SELECT * from balance')
                            b = await cursor.fetchone()
                            if b is None:
                                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                                y = msg[0].mentions[0]
                                amount = (90*a[4])/100
                                amount = int(amount)
                                await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, amount))
                                await db.execute('UPDATE commissions SET amount=? WHERE channel_id=?', ('null', interaction.channel.id))
                                embed = discord.Embed(title="Commission Complete",
                                    description=f"""
This commission has been marked as complete! **${a[3]:.2f}** has been added to the <@{a[2]}>'s balance.

If there was an error in this, please contact a staff member immediately.
""",
                                    color=discord.Color.orange())
                                view = ReviewSystem()
                                await interaction.response.send_message(content=f'{y.mention} <@{a[2]}>', embed=embed, view=view)
                            else:
                                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                                y = msg[0].mentions[0]
                                amount = (90*a[4])/100
                                amount = int(amount)
                                await db.execute('UPDATE balance SET amount=amount + ? WHERE freelancer_id=?', (amount, a[2]))
                                await db.execute('UPDATE commissions SET amount=? WHERE channel_id=?', ('null', interaction.channel.id))
                                embed = discord.Embed(title="Commission Complete",
                                    description=f"""
This commission has been marked as complete! **${a[3]:.2f}** has been added to the <@{a[2]}>'s balance.

If there was an error in this, please contact a staff member immediately.
""",
                                    color=discord.Color.orange())
                                view = ReviewSystem()
                                await interaction.response.send_message(content=f'{y.mention} <@{a[2]}>', embed=embed, view=view)
                        else:
                            await interaction.response.send_message("This commission does not have a commission manager set!", ephemeral=True)
                    else:
                        await interaction.response.send_message("This commission does not have a price set!", ephemeral=True)
                else:
                    await interaction.response.send_message("This commission does not have a freelancer set!", ephemeral=True)
                await db.commit()
                await db.close()
            else:
                await interaction.response.send_message("This isn't a commission channel!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You don't have the {commission_manager.mention} role!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CommissionsCog(bot), guilds=[discord.Object(id=guild_id)])