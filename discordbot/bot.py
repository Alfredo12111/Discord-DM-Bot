import discord
from discord.ext import commands
from discord import app_commands

# Bot setup
intents = discord.Intents.default()
intents.members = True  # Required to fetch members
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name="dm", description="DM everyone in the server")
async def dm_everyone(interaction: discord.Interaction, message: str):
    guild = interaction.guild
    member = guild.get_member(interaction.user.id)  # Get the member object

    if not member or not member.guild_permissions.administrator:
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
        return
    
    await interaction.response.send_message("Sending DMs...", ephemeral=True)
    for member in guild.members:
        if not member.bot:
            try:
                await member.send(message)
            except discord.Forbidden:
                print(f"Could not DM {member}")
    print("DMs sent!")

# Run the bot
bot.run("Token Here")
