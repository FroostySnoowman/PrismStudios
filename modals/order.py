import discord
import aiosqlite
import yaml
import datetime as DT
from datetime import datetime

from buttons.freelancer.freelancersystem import FreelancerSystem
from buttons.commissions.claimcommissionticket import ClaimCommissionTicket
from buttons.tickets.ticketclose import TicketClose

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

commission_ticket_category_id = data["Channel_Categories"]["TICKET_CATEGORY_ID"]
freelancer_commission_channel_id = data["Channels"]["FREELANCER_COMMISSION_CHANNEL_ID"]
staff_claim_ticket_channel_id = data["Channels"]["CLAIM_TICKET_CHANNEL_ID"]
commission_manager_role_id = data["Roles"]["COMMISSION_MANAGER_ROLE_ID"]

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

class Order(discord.ui.Modal, title='Order Services'):
    def __init__(self, category):
        super().__init__(timeout=None)
        self.category = category
    
        if self.category == "Illustrator":
            self.role_id = illustrator_role_id
        if self.category == "GFX Designer":
            self.role_id = gfx_designer_role_id
        if self.category == "Skin Designer":
            self.role_id = skin_designer_role_id
        if self.category == "Pixel Artist":
            self.role_id = pixel_artist_role_id
        if self.category == "Bot Developer":
            self.role_id = bot_developer_role_id
        if self.category == "Lua Scripter":
            self.role_id = lua_scripter_role_id
        if self.category == "Software Developer":
            self.role_id = software_developer_role_id
        if self.category == "Plugin Developer":
            self.role_id = plugin_developer_role_id
        if self.category == "Mod Develooper":
            self.role_id = mod_developer_role_id
        if self.category == "Datapack Developer":
            self.role_id = datapack_developer_role_id
        if self.category == "Minecraft Client Developer":
            self.role_id = minecraft_client_developer_role_id
        if self.category == "Tebex Designer":
            self.role_id = tebex_designer_role_id
        if self.category == "Pterodactyl Designer":
            self.role_id = pterodactyl_designer_role_id
        if self.category == "Web Developer":
            self.role_id = web_developer_role_id
        if self.category == "Web Designer":
            self.role_id = web_designer_role_id
        if self.category == "UIX Designer":
            self.role_id = uix_designer_role_id
        if self.category == "Discord Setup":
            self.role_id = discord_setup_role_id
        if self.category == "Minecraft Setup":
            self.role_id = minecraft_setup_role_id
        if self.category == "Configurator":
            self.role_id = configurator_role_id
        if self.category == "System Administrator":
            self.role_id = system_administrator_role_id
        if self.category == "Builder":
            self.role_id = builder_role_id
        if self.category == "Terraformer":
            self.role_id = terraformer_role_id
        if self.category == "Animator":
            self.role_id = animator_role_id
        if self.category == "Video Editor":
            self.role_id = video_editor_role_id
        if self.category == "Intro Creator":
            self.role_id = intro_creator_role_id
        if self.category == "Trailer Creator":
            self.role_id = trailer_creator_role_id
        if self.category == "Writer":
            self.role_id = writer_role_id
        if self.category == "Game Developer":
            self.role_id = game_developer_role_id
        if self.category == "Sound Engineer":
            self.role_id = sound_engineer_role_id
        if self.category == "Map Designer":
            self.role_id = map_designer_role_id
        if self.category == "3D Modeler":
            self.role_id = modeler_role_id
        if self.category == "Musician":
            self.role_id = musician_role_id
        if self.category == "Instrumentalist":
            self.role_id = instrumentalist_role_id

    budget = discord.ui.TextInput(
        label='Budget',
        placeholder='What is your budget?',
        max_length=5,
    )

    deadline = discord.ui.TextInput(
        label='Deadline',
        placeholder='What is your deadline?',
        max_length=25,
    )

    description = discord.ui.TextInput(
        label='Project Description',
        style=discord.TextStyle.long,
        placeholder='What is your project description?',
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content='Creating...', embed=None, view=None)
        db = await aiosqlite.connect('database.db')

        category_channel = interaction.guild.get_channel(commission_ticket_category_id)
        ticket_channel = await category_channel.create_text_channel(
            f"order-{interaction.user.name}")
        await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                                         send_messages=False,
                                         read_messages=False)

        
        await ticket_channel.set_permissions(interaction.user,
                                         send_messages=True,
                                         read_messages=True,
                                         add_reactions=True,
                                         embed_links=True,
                                         attach_files=True,
                                         read_message_history=True,
                                         external_emojis=True,
                                         use_application_commands=True)

        commissions_channel = interaction.guild.get_channel(freelancer_commission_channel_id)

        embed = discord.Embed(title="New Order Commission!",
                            description=f"**__Budget__** \n{self.budget.value} \n\n**__Deadline__** \n{self.deadline.value} \n\n**__Project Description__** \n{self.description.value}",
                            color=discord.Color.orange())
        
        embed.set_footer(text="Mixelate", icon_url=interaction.guild.icon.url)
        embed.timestamp = datetime.now()

        role = interaction.guild.get_role(self.role_id)

        c = await commissions_channel.send(content=f'{role.mention}', embed=embed, view=FreelancerSystem())

        claim_channel = interaction.guild.get_channel(staff_claim_ticket_channel_id)
        commission_manager = interaction.guild.get_role(commission_manager_role_id)

        a = DT.datetime.now().timestamp()
        b = int(a)

        embed=discord.Embed( 
        description=f"""
**Commission <t:{b}:R>**
```
Commission Deadline: {self.deadline.value}
Commission Details: {self.description.value}
```
""",
        color=discord.Color.orange())

        view = ClaimCommissionTicket()

        d = await claim_channel.send(content=commission_manager.id, embed=embed, view=view)

        await db.execute('INSERT INTO commissions VALUES (?,?,?,?,?,?,?);', (ticket_channel.id, self.role_id, c.id, 'null', 'null', d.id, 'null'))

        x = f'{interaction.user.mention}'

        embed = discord.Embed(title="Order Information",
                            description=f"""
Our freelancers will begin sending you quotes for your project shortly. You will be notified when you receive a response!

**Some Tips While You Wait** ```
- If you have any issues during the commission process try pinging the commission manager! 

- Did you and the freelancer decide on a new price? The price can be updated any time before paying by clicking "Confirm" when prompted!```

**Details** ```
Budget: {self.budget.value}

Deadline: {self.deadline.value}

Project Description: {self.description.value}```
""",
                            color=discord.Color.orange())

        view = TicketClose()

        await ticket_channel.send(content=x, embed=embed, view=view)

        await interaction.edit_original_response(content=f'The ticket has been created at {ticket_channel.mention}.')

        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)