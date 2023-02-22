import discord
import aiosqlite
import asyncio
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
payout_channel_id = data["Channels"]["PAYOUT_CHANNEL_ID"]

class FreelancerDashboard(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.response = None
        self.user = user

    async def on_timeout(self):
        try:
            for child in self.children:
                child.disabled = True
            await self.response.edit(content="This button has timed out... deleting in 15 seconds!", embed=None, view=self)
            await asyncio.sleep(15)
            await self.response.delete()
        except:
            return

    @discord.ui.button(emoji='💵', label='Wallet', style=discord.ButtonStyle.grey, custom_id='freelancer_dashboard:1')
    async def wallet(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from balance WHERE freelancer_id=?', (self.user.id, ))
        a = await cursor.fetchone()
        user = self.user
        view = FreelancerWallet(user)
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, 'null', 'null', 'null', 'null'))
            await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, 0))
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            embed.add_field(name="Wallet", value="**$0.00**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Balance", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
            out = await interaction.original_response()
            view.response = out
        else:
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            embed.add_field(name="Wallet", value=f"**${a[1]:.2f}**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Balance", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='🧑‍💻', label='Profile', style=discord.ButtonStyle.grey, custom_id='freelancer_dashboard:2')
    async def profile(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (self.user.id, ))
        a = await cursor.fetchone()
        user = self.user
        view = FreelancerProfile(user)
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, 'null', 'null', 'null', 'null'))
            await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, 0))
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            embed.add_field(name="Title", value=f"**N/A**", inline=True)
            embed.add_field(name="Description", value=f"**N/A**", inline=True)
            embed.add_field(name="Portfolio", value=f"**N/A**", inline=True)
            embed.add_field(name="PayPal", value=f"**N/A**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
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
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

class FreelancerWallet(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.response = None
        self.user = user

    async def on_timeout(self):
        try:
            for child in self.children:
                child.disabled = True
            await self.response.edit(content="This button has timed out... deleting in 15 seconds!", embed=None, view=self)
            await asyncio.sleep(15)
            await self.response.delete()
        except:
            return

    @discord.ui.button(emoji='🤑', label='Request Payout', style=discord.ButtonStyle.grey, custom_id='freelancer_wallet:1')
    async def payout(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        cursor2 = await db.execute('SELECT * FROM balance WHERE freelancer_id=?', (interaction.user.id, ))
        b = await cursor2.fetchone()
        pp = self.children
        dd = self
        user = self.user
        if a is None:
            await interaction.response.send_modal(RequestPayout(pp, dd, user))
        else:
            if b[1] > 0:
                if a[4] == 'null':
                    await interaction.response.send_modal(RequestPayout(pp, dd, user))
                else:
                    await db.execute('UPDATE balance SET amount=? WHERE freelancer_id=?', (0, interaction.user.id))
                    payout_channel = interaction.guild.get_channel(payout_channel_id)
                    embed = discord.Embed(
                        title="",
                        color=discord.Color.orange())
                    embed.add_field(name="PayPal", value=f"**{a[4]}**", inline=True)
                    embed.add_field(name="Amount", value=f"**${b[1]:.2f}**", inline=True)
                    await payout_channel.send(content=f"{interaction.user.mention} ({interaction.user.id}) has requested for a payout!", embed=embed, view=None)
                    await interaction.response.edit_message(content="You have successfully requested your payout! The money will be transferred to your payout shortly.", embed=None, view=None)
            else:
                await interaction.response.edit_message(content="You do not have enough funds to withdraw!", embed=None, view=None)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='👈', label='Back', style=discord.ButtonStyle.red, custom_id='freelancer_wallet:2')
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="",
            color=discord.Color.orange())
        embed.add_field(name="Wallet", value="View and request to withdraw your CookieServices balance.", inline=True)
        embed.add_field(name="Profile", value="View and edit your profile, configure account settings.", inline=True)
        embed.set_author(name=f"{interaction.user.name}'s Dashboard", icon_url=interaction.user.avatar.url)
        user = interaction.user
        view = FreelancerDashboard(user)
        await interaction.response.edit_message(embed=embed, view=view)
        out = await interaction.original_response()
        view.response = out

class RequestPayout(discord.ui.Modal, title='Requesting Your Payout!'):

    def __init__(self, pp, dd, user):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.user = user

    setpaypal = discord.ui.TextInput(
        label='Requesting Payout',
        placeholder='What is your PayPal email?',
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if "@" in self.setpaypal.value:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            cursor2 = await db.execute('SELECT * FROM balance WHERE freelancer_id=?', (interaction.user.id, ))
            b = await cursor2.fetchone()
            view = FreelancerDashboardBack(self.user)
            if a is None:
                await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, 'null' 'null', 'null', self.setpaypal.value))
                await db.execute('UPDATE balance SET amount=? WHERE freelancer_id=?', (0, interaction.user.id))
                embed = discord.Embed(
                    title="",
                    description=f"Your PayPal has been set to **{self.setpaypal.value}** and the request has been sent.",
                    color=discord.Color.orange())
                await interaction.response.edit_message(embed=embed, view=view)
                payout_channel = interaction.guild.get_channel(payout_channel_id)
                embed = discord.Embed(
                    title="",
                    color=discord.Color.orange())
                embed.add_field(name="PayPal", value=f"**{self.setpaypal.value}**", inline=True)
                embed.add_field(name="Amount", value=f"**${b[1]:.2f}**", inline=True)
                await payout_channel.send(content=f"{interaction.user.mention} ({interaction.user.id}) has requested for a payout!", embed=embed, view=None)
            else:
                await db.execute('UPDATE freelancer SET paypal=? WHERE freelancer_id=?', (self.setpaypal.value, interaction.user.id))
                await db.execute('UPDATE balance SET amount=? WHERE freelancer_id=?', (0, interaction.user.id))
                embed = discord.Embed(
                    title="",
                    description=f"Your PayPal has been set to **{self.setpaypal.value}** and the request has been sent.",
                    color=discord.Color.orange())
                await interaction.response.edit_message(embed=embed, view=view)
                payout_channel = interaction.guild.get_channel(payout_channel_id)
                embed = discord.Embed(
                    title="",
                    color=discord.Color.orange())
                embed.add_field(name="PayPal", value=f"**{self.setpaypal.value}**", inline=True)
                embed.add_field(name="Amount", value=f"**${b[1]:.2f}**", inline=True)
                await payout_channel.send(content=f"{interaction.user.mention} ({interaction.user.id}) has requested for a payout!", embed=embed, view=None)
            await db.commit()
            await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class FreelancerDashboardBack(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.response = None
        self.user = user

    async def on_timeout(self):
        try:
            for child in self.children:
                child.disabled = True
            await self.response.edit(content="This button has timed out... deleting in 15 seconds!", embed=None, view=self)
            await asyncio.sleep(15)
            await self.response.delete()
        except:
            return

    @discord.ui.button(emoji='👈', label='Back', style=discord.ButtonStyle.red, custom_id='freelancer_dashboard_back:1')
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="",
            color=discord.Color.orange())
        embed.add_field(name="Wallet", value="View and request to withdraw your CookieServices balance.", inline=True)
        embed.add_field(name="Profile", value="View and edit your profile, configure account settings.", inline=True)
        embed.set_author(name=f"{interaction.user.name}'s Dashboard", icon_url=interaction.user.avatar.url)
        user = interaction.user
        view = FreelancerDashboard(user)
        await interaction.response.edit_message(embed=embed, view=view)
        out = await interaction.original_response()
        view.response = out

class FreelancerProfile(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.response = None
        self.user = user

    async def on_timeout(self):
        try:
            for child in self.children:
                child.disabled = True
            await self.response.edit(content="This button has timed out... deleting in 15 seconds!", embed=None, view=self)
            await asyncio.sleep(15)
            await self.response.delete()
        except:
            return

    @discord.ui.button(emoji='🐬', label='Set Title', style=discord.ButtonStyle.grey, custom_id='freelancer_profile:1')
    async def title(self, interaction: discord.Interaction, button: discord.ui.Button):
        pp = self.children
        dd = self
        user = self.user
        await interaction.response.send_modal(SetTitle(pp, dd, user))

    @discord.ui.button(emoji='✏️', label='Set Description', style=discord.ButtonStyle.grey, custom_id='freelancer_profile:2')
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        pp = self.children
        dd = self
        user = self.user
        await interaction.response.send_modal(SetDescription(pp, dd, user))

    @discord.ui.button(emoji='📖', label='Set Portfolio', style=discord.ButtonStyle.grey, custom_id='freelancer_profile:3')
    async def portfolio(self, interaction: discord.Interaction, button: discord.ui.Button):
        pp = self.children
        dd = self
        user = self.user
        await interaction.response.send_modal(SetPortfolio(pp, dd, user))

    @discord.ui.button(emoji='💰', label='Set PayPal', style=discord.ButtonStyle.grey, custom_id='freelancer_profile:4')
    async def paypal(self, interaction: discord.Interaction, button: discord.ui.Button):
        pp = self.children
        dd = self
        user = self.user
        await interaction.response.send_modal(SetPayPal(pp, dd, user))

    @discord.ui.button(emoji='👈', label='Back', style=discord.ButtonStyle.red, custom_id='freelancer_profile:5', row=2)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="",
            color=discord.Color.orange())
        embed.add_field(name="Wallet", value="View and request to withdraw your CookieServices balance.", inline=True)
        embed.add_field(name="Profile", value="View and edit your profile, configure account settings.", inline=True)
        embed.set_author(name=f"{interaction.user.name}'s Dashboard", icon_url=interaction.user.avatar.url)
        user = interaction.user
        view = FreelancerDashboard(user)
        await interaction.response.edit_message(embed=embed, view=view)
        out = await interaction.original_response()
        view.response = out

class SetTitle(discord.ui.Modal, title='Set Your Title!'):

    def __init__(self, pp, dd, user):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.user = user

    settitle = discord.ui.TextInput(
        label='Set Title',
        placeholder='What is your title?',
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        view = FreelancerProfile(self.user)
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, self.settitle.value, 'null', 'null', 'null'))
            await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, 0))
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            if self.settitle.value == 'null':
                title = "N/A"
            else:
                title = self.settitle.value
            embed.add_field(name="Title", value=f"**{self.settitle.value}**", inline=True)
            embed.add_field(name="Description", value=f"**N/A**", inline=True)
            embed.add_field(name="Portfolio", value=f"**N/A**", inline=True)
            embed.add_field(name="PayPal", value="**N/A**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await db.execute('UPDATE freelancer SET title=? WHERE freelancer_id=?', (self.settitle.value, interaction.user.id))
            if self.settitle.value == 'null':
                title = "N/A"
            else:
                title = self.settitle.value
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
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class SetDescription(discord.ui.Modal, title='Set Your Description!'):

    def __init__(self, pp, dd, user):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.user = user

    setdescription = discord.ui.TextInput(
        label='Set Description',
        placeholder='What is your description?',
        max_length=150,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        view = FreelancerProfile(self.user)
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, 'null', self.setdescription.value, 'null', 'null'))
            await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, 0))
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            if self.setdescription.value == 'null':
                description = "N/A"
            else:
                description = self.setdescription.value
            embed.add_field(name="Title", value=f"**N/A**", inline=True)
            embed.add_field(name="Description", value=f"**{description}**", inline=True)
            embed.add_field(name="Portfolio", value=f"**N/A**", inline=True)
            embed.add_field(name="PayPal", value="**N/A**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await db.execute('UPDATE freelancer SET description=? WHERE freelancer_id=?', (self.setdescription.value, interaction.user.id))
            if a[1] == 'null':
                title = "N/A"
            else:
                title = a[1]
            if self.setdescription.value == 'null':
                description = "N/A"
            else:
                description = self.setdescription.value
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
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class SetPortfolio(discord.ui.Modal, title='Set Your Portfolio!'):

    def __init__(self, pp, dd, user):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.user = user

    setportfolio = discord.ui.TextInput(
        label='Set Portfolio',
        placeholder='What is your portfolio?',
        max_length=75,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        view = FreelancerProfile(self.user)
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, 'null', 'null', self.setportfolio.value, 'null'))
            await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, 0))
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            if self.setportfolio.value == 'null':
                portfolio = "N/A"
            else:
                portfolio = self.setportfolio.value
            embed.add_field(name="Title", value=f"**N/A**", inline=True)
            embed.add_field(name="Description", value=f"**N/A**", inline=True)
            embed.add_field(name="Portfolio", value=f"**{portfolio}**", inline=True)
            embed.add_field(name="PayPal", value=f"**N/A**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await db.execute('UPDATE freelancer SET portfolio=? WHERE freelancer_id=?', (self.setportfolio.value, interaction.user.id))
            if a[1] == 'null':
                title = "N/A"
            else:
                title = a[1]
            if a[2] == 'null':
                description = "N/A"
            else:
                description = a[2]
            if self.setportfolio.value == 'null':
                portfolio = "N/A"
            else:
                portfolio = self.setportfolio.value
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
            embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class SetPayPal(discord.ui.Modal, title='Set Your PayPal!'):

    def __init__(self, pp, dd, user):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.user = user

    setpaypal = discord.ui.TextInput(
        label='Set PayPal',
        placeholder='What is your paypal email?',
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction):
        valid_options = ('@', 'null')
        if any(thing in self.setpaypal.value for thing in valid_options):
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            view = FreelancerProfile(self.user)
            if a is None:
                await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, 'null', 'null', 'null', self.setpaypal.value))
                await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, 0))
                embed = discord.Embed(
                    title="",
                    color=discord.Color.orange())
                if self.setpaypal.value == 'null':
                    paypal = "N/A"
                else:
                    paypal = self.setpaypal.value
                embed.add_field(name="Title", value=f"**N/A**", inline=True)
                embed.add_field(name="Description", value=f"**N/A**", inline=True)
                embed.add_field(name="Portfolio", value=f"**{portfolio}**", inline=True)
                embed.add_field(name="PayPal", value=f"**{paypal}**")
                embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                await db.execute('UPDATE freelancer SET paypal=? WHERE freelancer_id=?', (self.setpaypal.value, interaction.user.id))
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
                if self.setpaypal.value == 'null':
                    paypal = "N/A"
                else:
                    paypal = self.setpaypal.value
                embed = discord.Embed(
                    title="",
                    color=discord.Color.orange())
                embed.add_field(name="Title", value=f"**{title}**", inline=True)
                embed.add_field(name="Description", value=f"**{description}**", inline=True)
                embed.add_field(name="Portfolio", value=f"**{portfolio}**", inline=True)
                embed.add_field(name="PayPal", value=f"**{paypal}**")
                embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=embed, view=view)
            await db.commit()
            await db.close()
        else:
            await interaction.response.send_message("You must provide a valid email!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class FreelancerCog(commands.GroupCog, name="freelancer"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="balance", description="Shows you how much money you have!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def balance(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from balance WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?);', (interaction.user.id, 'null', 'null', 'null', 'null'))
            await db.execute('INSERT INTO balance VALUES (?,?);', (interaction.user.id, 0))
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            embed.add_field(name="Wallet", value="**$0.00**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Balance", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            embed.add_field(name="Wallet", value=f"**${a[1]:.2f}**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Balance", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="dashboard", description="Opens the freelancer dashboard!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def dashboard(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="",
            color=discord.Color.orange())
        embed.add_field(name="Wallet", value="View and request to withdraw your CookieServices balance.", inline=True)
        embed.add_field(name="Profile", value="View and edit your profile, configure account settings.", inline=True)
        embed.set_author(name=f"{interaction.user.name}'s Dashboard", icon_url=interaction.user.avatar.url)
        user = interaction.user
        view = FreelancerDashboard(user)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        out = await interaction.original_response()
        view.response = out

class ViewCog(commands.GroupCog, name="view"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="freelancer", description="Shows you information about a freelancer!")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.default_permissions(administrator=True)
    async def view(self, interaction: discord.Interaction, member: discord.Member):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (member.id, ))
        a = await cursor.fetchone()
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
            embed = discord.Embed(
                title="",
                color=discord.Color.orange())
            embed.add_field(name="Title", value=f"**{title}**", inline=True)
            embed.add_field(name="Description", value=f"**{description}**", inline=True)
            embed.add_field(name="Portfolio", value=f"**{portfolio}**", inline=True)
            embed.set_author(name=f"{member.name}'s Profile", icon_url=member.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(FreelancerCog(bot), guilds=[discord.Object(id=guild_id)])
    await bot.add_cog(ViewCog(bot), guilds=[discord.Object(id=guild_id)])