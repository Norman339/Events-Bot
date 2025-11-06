import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Help cog initialized")

    @app_commands.command(name="sm_help", description="Show all available Shellmates bot commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛡️ Shellmates Bot - Command List",
            description="Here are all the available commands for the Shellmates bot:",
            color=discord.Color.blue()
        )
        
        # Events commands
        embed.add_field(
            name="📅 Event Commands",
            value=(
                "`/sm_events` - List all upcoming Shellmates events\n"
                "`/sm_addevent` - Add a new event (Admin only)\n"
                "`/sm_modifyevent` - Modify an existing event (Admin only)\n"
                "`/sm_removeevent` - Remove an event (Admin only)\n"
                "`/sm_clearevents` - Clear all events (Admin only)\n"
            ),
            inline=False
        )
        
        # Facts commands
        embed.add_field(
            name="🔒 Cybersecurity Commands",
            value=(
                "`/sm_fact` - Get a random cybersecurity fact\n"
                "`/sm_addfact` - Add a new fact (Admin only)\n"
                "`/sm_removefact` - Remove a fact (Admin only)\n"
                "`/sm_listfacts` - List all facts (Admin only)\n"
            ),
            inline=False
        )
        
        # Help command
        embed.add_field(
            name="ℹ️ Information",
            value=(
                "`/sm_help` - Show this help message\n"
            ),
            inline=False
        )
        
        embed.set_footer(text="Shellmates Cybersecurity Club | MongoDB-backed • Stay secure! 🔐")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
