import discord
import yaml
from discord.ext import commands

from buttons.applications.freelancerapplicationsubmit import FreelancerApplicationSubmit

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

class FreelancerApplicationDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='-------DESIGN-------'),
            discord.SelectOption(label='Illustrator'),
            discord.SelectOption(label='GFX Designer'),
            discord.SelectOption(label='Skin Designer'),
            discord.SelectOption(label='Pixel Arist'),
            discord.SelectOption(label='-------DEVELOPMENT-------'),
            discord.SelectOption(label='Bot Developer'),
            discord.SelectOption(label='Lua Scripter'),
            discord.SelectOption(label='Software Developer'),
            discord.SelectOption(label='Plugin Developer'),
            discord.SelectOption(label='Mod Developer'),
            discord.SelectOption(label='Datapack Developer'),
            discord.SelectOption(label='Minecraft Client Developer'),
            discord.SelectOption(label='-------WEB-------'),
            discord.SelectOption(label='Tebex Designer'),
            discord.SelectOption(label='Pterodactyl Designer'),
            discord.SelectOption(label='Web Developer'),
            discord.SelectOption(label='Web Designer'),
            discord.SelectOption(label='UIX Designer'),
            discord.SelectOption(label='-------SETUPS-------'),
            discord.SelectOption(label='Discord Setup'),
            discord.SelectOption(label='Minecraft Setup'),
            discord.SelectOption(label='Configurator'),
            discord.SelectOption(label='System Administrator'),
        ]

        super().__init__(placeholder="Choose all the roles you're applying for!", min_values=1, max_values=20, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.stored_values = self.values
        stored_roles = (', '.join(self.values))
        self.view.stored_roles = stored_roles
        roles = (' \n'.join(self.values))
        self.view.roles = roles
        embed=discord.Embed(title="Freelancer Applications", 
        description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*{roles}*

**Design**
Illustrator
GFX Designer
Skin Designer
Pixel Artist

**Development**
Bot Developer
Lua Scripter
Software Developer
Plugin Developer
Mod Developer
Datapack Developer
Minecraft Client Developer

**Web**
Tebex Designer
Pterodactyl Designer
Web Developer
Web Designer
UIX Designer

**Setups**
Discord Setup
Minecraft Setup
Configurator
System Administrator
""", 
        color=discord.Color.orange())
        await interaction.response.edit_message(embed=embed)

class FreelancerApplicationDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.stored_roles = None
        self.roles = None
        self.stored_values = None

        self.add_item(FreelancerApplicationDropdown())
        self.add_item(FreelancerApplicationSubmit())
        self.add_item(FreelancerApplicationNext())

class FreelancerApplicationDropdownTwo(discord.ui.Select):
    def __init__(self, stored_values, stored_roles, roles):
        self.stored_values = stored_values
        self.stored_roles = stored_roles
        self.roles = roles

        options = [
            discord.SelectOption(label='-------MC Builds-------'),
            discord.SelectOption(label='Builder'),
            discord.SelectOption(label='Terraformer'),
            discord.SelectOption(label='-------Video-------'),
            discord.SelectOption(label='Animator'),
            discord.SelectOption(label='Video Editor'),
            discord.SelectOption(label='Intro Creator'),
            discord.SelectOption(label='Trailer Creator'),
            discord.SelectOption(label='-------Writing-------'),
            discord.SelectOption(label='Writer'),
            discord.SelectOption(label='-------Game-------'),
            discord.SelectOption(label='Game Developer'),
            discord.SelectOption(label='Sound Engineer'),
            discord.SelectOption(label='Map Designer'),
            discord.SelectOption(label='3D Modeler'),
            discord.SelectOption(label='-------Music-------'),
            discord.SelectOption(label='Musician'),
            discord.SelectOption(label='Instrumentalist'),
        ]

        super().__init__(placeholder="Choose all the roles you're applying for!", min_values=1, max_values=13, options=options)

    async def callback(self, interaction: discord.Interaction):

        try:
            self.view.roles = (' \n'.join(self.stored_values)) + '\n' + (' \n'.join(self.values))
        except:
            self.view.roles = (' \n'.join(self.values))
        try:
            self.view.stored_values = self.stored_values + self.values
        except:
            self.view.stored_values = self.values
        try:
            self.view.stored_roles = self.stored_roles + ', ' + (', '.join(self.values))
        except:
            self.view.stored_roles = (', '.join(self.values))

        embed=discord.Embed(title="Freelancer Applications", 
        description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*{self.view.roles}*

**MC Builds**
Builder
Terraformer

**Video**
Animator
Video Editor
Intro Creator
Trailer Creator

**Writing**
Writer

**Game**
Game Developer
Sound Engineer
Map Designer
3D Modeler

**Music**
Musician
Instrumentalist
""", 
        color=discord.Color.orange())
        await interaction.response.edit_message(embed=embed)

class FreelancerApplicationDropdownViewTwo(discord.ui.View):
    def __init__(self, stored_values, stored_roles, roles):
        super().__init__()
        self.stored_values = stored_values
        self.stored_roles = stored_roles
        self.roles = roles

        self.stored_values2 = None
        self.stored_roles2 = None
        self.roles2 = None

        self.add_item(FreelancerApplicationDropdownTwo(stored_values, stored_roles, roles))
        self.add_item(FreelancerApplicationSubmit())
        self.add_item(FreelancerApplicationRestart())

class FreelancerApplicationNext(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Next Page', emoji='➡️')

    async def callback(self, interaction: discord.Interaction):
        stored_values = self.view.stored_values
        stored_roles = self.view.stored_roles
        roles = self.view.roles
        view = FreelancerApplicationDropdownViewTwo(stored_values, stored_roles, roles)
        if roles == None:
            roles = "N/A"
        

        embed=discord.Embed(title="Freelancer Applications", 
        description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*{roles}*

**MC Builds**
Builder
Terraformer

**Video**
Animator
Video Editor
Intro Creator
Trailer Creator

**Writing**
Writer

**Game**
Game Developer
Sound Engineer
Map Designer
3D Modeler

**Music**
Musician
Instrumentalist
""", 
        color=discord.Color.orange())
        await interaction.response.edit_message(embed=embed, view=view)

class FreelancerApplicationRestart(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Restart', emoji='🔁')

    async def callback(self, interaction: discord.Interaction):

        view = FreelancerApplicationDropdownView()

        embed=discord.Embed(title="Freelancer Applications", 
        description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*N/A*

**Design**
Illustrator
GFX Designer
Skin Designer
Pixel Artist

**Development**
Bot Developer
Lua Scripter
Software Developer
Plugin Developer
Mod Developer
Datapack Developer
Minecraft Client Developer

**Web**
Tebex Designer
Pterodactyl Designer
Web Developer
Web Designer
UIX Designer

**Setups**
Discord Setup
Minecraft Setup
Configurator
System Administrator
""", 
        color=discord.Color.orange())
        await interaction.response.edit_message(embed=embed, view=view)

class FreelancerApplicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(FreelancerApplicationCog(bot), guilds=[discord.Object(id=guild_id)])