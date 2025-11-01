import discord
from discord.ext import commands
from discord import app_commands
from bot.utils import db

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sm_events", description="List all upcoming Shellmates events")
    async def list_events(self, interaction: discord.Interaction):
        events = await db.get_events()
        if not events:
            await interaction.response.send_message("No upcoming events scheduled!")
            return
        
        embed = discord.Embed(
            title="📅 Upcoming Shellmates Events",
            color=discord.Color.green()
        )
        
        for event in events:
            embed.add_field(
                name=event['title'],
                value=f"📅 {event['date']}\n📝 {event['description']}\n\n",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sm_addevent", description="Add a new Shellmates event (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_event(
        self,
        interaction: discord.Interaction,
        title: str,
        date: str,
        description: str
    ):
        event_data = {
            'title': title,
            'date': date,
            'description': description,
            'created_by': interaction.user.id,
            'created_at': interaction.created_at.isoformat()
        }
        
        await db.add_event(event_data)
        
        embed = discord.Embed(
            title="✅ Event Added",
            description=f"**{title}** has been added to the events list!",
            color=discord.Color.green()
        )
        embed.add_field(name="Date", value=date, inline=False)
        embed.add_field(name="Description", value=description, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sm_removeevent", description="Remove a Shellmates event (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_event(self, interaction: discord.Interaction, title: str):
        removed = await db.remove_event(title)
        if removed:
            await interaction.response.send_message(f"✅ Event '{title}' has been removed!")
        else:
            await interaction.response.send_message(f"❌ No event found with the title: {title}")

    @add_event.error
    @remove_event.error
    async def event_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ You don't have permission to use this command!", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ An error occurred: {str(error)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Events(bot))
