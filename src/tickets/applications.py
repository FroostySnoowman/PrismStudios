import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

moderator_role_id = data["Roles"]["MODERATOR_ROLE_ID"]
lead_commission_manager_role_id = data["Roles"]["LEAD_COMMISSION_MANAGER_ROLE_ID"]
commission_manager_role_id = data["Roles"]["COMMISSION_MANAGER_ROLE_ID"]
lead_application_reviewer_role_id = data["Roles"]["LEAD_APPLICATION_REVIEWER_ROLE_ID"]
application_reviewer_role_id = data["Roles"]["APPLICATION_REVIEWER_ROLE_ID"]
freelancer_role_id = data["Roles"]["FREELANCER_ROLE_ID"]

illustrator_role_id = data["Roles"]["ILLUSTRATOR_ROLE_ID"]
gfx_designer_role_id = data["Roles"]["GFX_DESIGNER_ROLE_ID"]
skin_designer_role_id = data["Roles"]["SKIN_DESIGNER_ROLE_ID"]
pixel_artist_role_id = data["Roles"]["PIXEL_ARTIST_ROLE_ID"]
bot_developer_role_id = data["Roles"]["BOT_DEVELOPER_ROLE_ID"]
lua_scripter_role_id = data["Roles"]["LUA_SCRIPTER_ROLE_ID"]
software_developer_role_id = data["Roles"]["SOFTWARE_DEVELOPER_ROLE_ID"]
plugin_developer_role_id = data["Roles"]["PLUGIN_DEVELOPER_ROLE_ID"]
mod_developer_role_id = data["Roles"]["MOD_DEVELOPER_ROLE_ID"]
datapack_developer_role_id = data["Roles"]["DATAPACK_DEVELOPER_ROLE_ID"]
minecraft_client_developer_role_id = data["Roles"]["MINECRAFT_CLIENT_DEVELOPER_ROLE_ID"]
tebex_designer_role_id = data["Roles"]["TEBEX_DESIGNER_ROLE_ID"]
pterodactyl_designer_role_id = data["Roles"]["PTERODACTYL_DESIGNER_ROLE_ID"]
web_developer_role_id = data["Roles"]["WEB_DEVELOPER_ROLE_ID"]
web_designer_role_id = data["Roles"]["WEB_DESIGNER_ROLE_ID"]
uix_designer_role_id = data["Roles"]["UIX_DESIGNER_ROLE_ID"]
discord_setup_role_id = data["Roles"]["DISCORD_SETUP_ROLE_ID"]
minecraft_setup_role_id = data["Roles"]["MINECRAFT_SETUP_ROLE_ID"]
configurator_role_id = data["Roles"]["CONFIGURATOR_ROLE_ID"]
system_administrator_role_id = data["Roles"]["SYSTEM_ADMINISTRATOR_ROLE_ID"]
builder_role_id = data["Roles"]["BUILDER_ROLE_ID"]
terraformer_role_id = data["Roles"]["TERRAFORMER_ROLE_ID"]
animator_role_id = data["Roles"]["ANIMATOR_ROLE_ID"]
video_editor_role_id = data["Roles"]["VIDEO_EDITOR_ROLE_ID"]
intro_creator_role_id = data["Roles"]["INTRO_CREATOR_ROLE_ID"]
trailer_creator_role_id = data["Roles"]["TRAILER_CREATOR_ROLE_ID"]
writer_role_id = data["Roles"]["WRITER_ROLE_ID"]
game_developer_role_id = data["Roles"]["GAME_DEVELOPER_ROLE_ID"]
sound_engineer_role_id = data["Roles"]["SOUND_ENGINEER_ROLE_ID"]
map_designer_role_id = data["Roles"]["MAP_DESIGNER_ROLE_ID"]
modeler_role_id = data["Roles"]["MODELER_ROLE_ID"]
musician_role_id = data["Roles"]["MUSICIAN_ROLE_ID"]
instrumentalist_role_id = data["Roles"]["INSTRUMENTALIST_ROLE_ID"]

claim_ticket_channel_id = data["Channels"]["CLAIM_TICKET_CHANNEL_ID"]
freelancer_announcement_channel_id = data["Channels"]["FREELANCER_ANNOUNCEMENT_CHANNEL_ID"]
freelancer_commission_channel_id = data["Channels"]["FREELANCER_COMMISSION_CHANNEL_ID"]

class ApplicationManagerDropdown(discord.ui.Select):
    def __init__(self, roles):
        self.roles = roles

        options = [discord.SelectOption(label=x) for x in roles]

        super().__init__(placeholder="Choose all the you wish to give them!", min_values=1, max_values=len(roles), options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Accepting...", view=None, embed=None)
        e = await interaction.original_response()
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        ids = []
        try:
            channel = interaction.guild.get_channel(claim_ticket_channel_id)
            claim_message = channel.get_partial_message(a[3])
            await claim_message.delete()
        except:
            pass
        for roles in self.values:
            if roles == "Moderator":
                id = moderator_role_id
                ids.append(id)
            if roles == "Lead Commission Manager":
                id = lead_commission_manager_role_id
                ids.append(id)
            if roles == "Commission Manager":
                id = commission_manager_role_id
                ids.append(id)
            if roles == "Lead Application Reviewer":
                id = lead_application_reviewer_role_id
                ids.append(id)
            if roles == "Application Reviewer":
                id = application_reviewer_role_id
                ids.append(id)
            if roles == "Illustrator":
                id = illustrator_role_id
                ids.append(id)
            if roles == "GFX Designer":
                id = gfx_designer_role_id
                ids.append(id)
            if roles == "Skin Designer":
                id = skin_designer_role_id
                ids.append(id)
            if roles == "Pixel Artist":
                id = pixel_artist_role_id
                ids.append(id)
            if roles == "Bot Developer":
                id = bot_developer_role_id
                ids.append(id)
            if roles == "Lua Scripter":
                id = lua_scripter_role_id
                ids.append(id)
            if roles == "Software Developer":
                id = software_developer_role_id
                ids.append(id)
            if roles == "Plugin Developer":
                id = plugin_developer_role_id
                ids.append(id)
            if roles == "Mod Developer":
                id = mod_developer_role_id
                ids.append(id)
            if roles == "Datapack Developer":
                id = datapack_developer_role_id
                ids.append(id)
            if roles == "Minecraft Client Developer":
                id = minecraft_client_developer_role_id
                ids.append(id)
            if roles == "Tebex Designer":
                id = tebex_designer_role_id
                ids.append(id)
            if roles == "Pterodactyl Designer":
                id = pterodactyl_designer_role_id
                ids.append(id)
            if roles == "Web Developer":
                id = web_developer_role_id
                ids.append(id)
            if roles == "Web Designer":
                id = web_designer_role_id
                ids.append(id)
            if roles == "UIX Designer":
                id = uix_designer_role_id
                ids.append(id)
            if roles == "Discord Setup":
                id = discord_setup_role_id
                ids.append(id)
            if roles == "Minecraft Setup":
                id = minecraft_setup_role_id
                ids.append(id)
            if roles == "Configurator":
                id = configurator_role_id
                ids.append(id)
            if roles == "System Adminstrator":
                id = system_administrator_role_id
                ids.append(id)
            if roles == "Builder":
                id = builder_role_id
                ids.append(id)
            if roles == "Terraformer":
                id = terraformer_role_id
                ids.append(id)
            if roles == "Animator":
                id = animator_role_id
                ids.append(id)
            if roles == "Video Editor":
                id = video_editor_role_id
                ids.append(id)
            if roles == "Intro Creator":
                id = intro_creator_role_id
                ids.append(id)
            if roles == "Trailer Creator":
                id = trailer_creator_role_id
                ids.append(id)
            if roles == "Writer":
                id = writer_role_id
                ids.append(id)
            if roles == "Game Developer":
                id = game_developer_role_id
                ids.append(id)
            if roles == "Sound Engineer":
                id = sound_engineer_role_id
                ids.append(id)
            if roles == "Map Designer":
                id = map_designer_role_id
                ids.append(id)
            if roles == "3D Modeler":
                id = modeler_role_id
                ids.append(id)
            if roles == "Musician":
                id = musician_role_id
                ids.append(id)
            if roles == "Instrumentalist":
                id = instrumentalist_role_id
                ids.append(id)
            else:
                continue
        applicant = interaction.guild.get_member(a[0])
        for roles in ids:
            role = interaction.guild.get_role(roles)
            await applicant.add_roles(role)
        if "Lead Application Reviewer" in self.values:
            try:
                role = interaction.guild.get_role(application_reviewer_role_id)
                await applicant.add_roles(role)
            except:
                pass
        if "Lead Commission Manager" in self.values:
            try:
                role = interaction.guild.get_role(commission_manager_role_id)
                await applicant.add_roles(role)
            except:
                pass
        roles = (' \n'.join(self.values))
        r = roles.replace(", ", "\n")
        await db.execute('DELETE FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        await db.commit()
        await db.close()
        valid_things = ("Moderator", "Lead Commission Manager", "Commission Manager", "Lead Application Reviewer", "Application Reviewer")
        if any(thing in roles for thing in valid_things):
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
Welcome to the staff team! Please wait patiently until we give you more information about your position!
""", 
            color=discord.Color.orange())
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await e.edit(content='Accepted!', view=None, embed=None)
        else:
            try:
                freelancer = interaction.guild.get_role(freelancer_role_id)
                await applicant.add_roles(freelancer)
            except:
                pass
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
If you haven't already, make sure to setup your profile. Use the command </freelancer dashboard:1037174318527955045> and click Profile to set up your profile!

You will start recieving commissions in the <#{freelancer_commission_channel_id}> channel. Please be sure to check <#{freelancer_announcement_channel_id}> frequently for any new announcements!
""", 
            color=discord.Color.orange())
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await e.edit(content='Accepted!', view=None, embed=None)

class ApplicationManagerDropdownView(discord.ui.View):
    def __init__(self, roles):
        super().__init__()
        self.roles = roles

        self.add_item(ApplicationManagerDropdown(roles))

class ApplicationManager(discord.ui.View):
    def __init__(self, ids):
        super().__init__(timeout=None)
        self.ids = ids

    @discord.ui.button(emoji='✅', label='Yes', style=discord.ButtonStyle.grey, custom_id='application:1')
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Accepting...", view=None, embed=None)
        e = await interaction.original_response()
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        try:
            channel = interaction.guild.get_channel(claim_ticket_channel_id)
            claim_message = channel.get_partial_message(a[3])
            await claim_message.delete()
        except:
            pass
        r = a[2].replace(", ", "\n")
        applicant = interaction.guild.get_member(a[0])
        for roles in self.ids:
            role = interaction.guild.get_role(roles)
            try:
                await applicant.add_roles(role)
            except:
                pass
        if "Lead Application Reviewer" in a[2]:
            try:
                role = interaction.guild.get_role(application_reviewer_role_id)
                await applicant.add_roles(role)
            except:
                pass
        if "Lead Commission Manager" in a[2]:
            try:
                role = interaction.guild.get_role(commission_manager_role_id)
                await applicant.add_roles(role)
            except:
                pass
        await db.execute('DELETE FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        await db.commit()
        await db.close()
        valid_things = ("Moderator", "Lead Commission Manager", "Commission Manager", "Lead Application Reviewer", "Application Reviewer")
        if any(thing in a[2] for thing in valid_things):
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
Welcome to the staff team! Please wait patiently until we give you more information about your position!
""", 
            color=discord.Color.orange())
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await e.edit(content='Accepted!', view=None, embed=None)
        else:
            try:
                freelancer = interaction.guild.get_role(freelancer_role_id)
                await applicant.add_roles(freelancer)
            except:
                pass
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
If you haven't already, make sure to setup your profile. Use the command </freelancer dashboard:1037174318527955045> and click Profile to set up your profile!

You will start receiving commissions in the <#{freelancer_commission_channel_id}> channel. Please be sure to check <#{freelancer_announcement_channel_id}> frequently for any new announcements!
""", 
            color=discord.Color.orange())
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await e.edit(content='Accepted!', view=None, embed=None)

    @discord.ui.button(emoji='❌', label='No', style=discord.ButtonStyle.grey, custom_id='application:2')
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        roles = a[2].split(", ")
        view = ApplicationManagerDropdownView(roles)
        await interaction.response.edit_message(content='Select the roles you would like to give them in the dropdown!', embed=None, view=view)

class ApplicationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="application", description="Open the application manager view.")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def application(self, interaction: discord.Interaction):
        if "apply" in interaction.channel.name:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            if a is None:
                await interaction.response.send_message("This application has already been accepted! Please get them to create a new application if they wish to apply for more.", ephemeral=True)
            else:
                ids = []
                x = a[2].split(", ")
                for roles in x:
                    if roles == "Moderator":
                        id = moderator_role_id
                        ids.append(id)
                    if roles == "Lead Commission Manager":
                        id = lead_commission_manager_role_id
                        ids.append(id)
                    if roles == "Commission Manager":
                        id = commission_manager_role_id
                        ids.append(id)
                    if roles == "Lead Application Reviewer":
                        id = lead_application_reviewer_role_id
                        ids.append(id)
                    if roles == "Application Reviewer":
                        id = application_reviewer_role_id
                        ids.append(id)
                    if roles == "Illustrator":
                        id = illustrator_role_id
                        ids.append(id)
                    if roles == "GFX Designer":
                        id = gfx_designer_role_id
                        ids.append(id)
                    if roles == "Skin Designer":
                        id = skin_designer_role_id
                        ids.append(id)
                    if roles == "Pixel Artist":
                        id = pixel_artist_role_id
                        ids.append(id)
                    if roles == "Bot Developer":
                        id = bot_developer_role_id
                        ids.append(id)
                    if roles == "Lua Scripter":
                        id = lua_scripter_role_id
                        ids.append(id)
                    if roles == "Software Developer":
                        id = software_developer_role_id
                        ids.append(id)
                    if roles == "Plugin Developer":
                        id = plugin_developer_role_id
                        ids.append(id)
                    if roles == "Mod Developer":
                        id = mod_developer_role_id
                        ids.append(id)
                    if roles == "Datapack Developer":
                        id = datapack_developer_role_id
                        ids.append(id)
                    if roles == "Minecraft Client Developer":
                        id = minecraft_client_developer_role_id
                        ids.append(id)
                    if roles == "Tebex Designer":
                        id = tebex_designer_role_id
                        ids.append(id)
                    if roles == "Pterodactyl Designer":
                        id = pterodactyl_designer_role_id
                        ids.append(id)
                    if roles == "Web Developer":
                        id = web_developer_role_id
                        ids.append(id)
                    if roles == "Web Designer":
                        id = web_designer_role_id
                        ids.append(id)
                    if roles == "UIX Designer":
                        id = uix_designer_role_id
                        ids.append(id)
                    if roles == "Discord Setup":
                        id = discord_setup_role_id
                        ids.append(id)
                    if roles == "Minecraft Setup":
                        id = minecraft_setup_role_id
                        ids.append(id)
                    if roles == "Configurator":
                        id = configurator_role_id
                        ids.append(id)
                    if roles == "System Adminstrator":
                        id = system_administrator_role_id
                        ids.append(id)
                    if roles == "Builder":
                        id = builder_role_id
                        ids.append(id)
                    if roles == "Terraformer":
                        id = terraformer_role_id
                        ids.append(id)
                    if roles == "Animator":
                        id = animator_role_id
                        ids.append(id)
                    if roles == "Video Editor":
                        id = video_editor_role_id
                        ids.append(id)
                    if roles == "Intro Creator":
                        id = intro_creator_role_id
                        ids.append(id)
                    if roles == "Trailer Creator":
                        id = trailer_creator_role_id
                        ids.append(id)
                    if roles == "Writer":
                        id = writer_role_id
                        ids.append(id)
                    if roles == "Game Developer":
                        id = game_developer_role_id
                        ids.append(id)
                    if roles == "Sound Engineer":
                        id = sound_engineer_role_id
                        ids.append(id)
                    if roles == "Map Designer":
                        id = map_designer_role_id
                        ids.append(id)
                    if roles == "3D Modeler":
                        id = modeler_role_id
                        ids.append(id)
                    if roles == "Musician":
                        id = musician_role_id
                        ids.append(id)
                    if roles == "Instrumentalist":
                        id = instrumentalist_role_id
                        ids.append(id)
                    else:
                        continue
                r = a[2].replace(", ", "\n")
                view = ApplicationManager(ids)
                embed=discord.Embed(
                description=f"Would you like to give the applicant all of the roles they applied for? Please use the buttons below. \n \n**__Roles__**: \n{r}", 
                color=discord.Color.orange())
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message("This is not an application channel!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ApplicationsCog(bot), guilds=[discord.Object(id=guild_id)])