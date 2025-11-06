import discord
from discord.ext import commands
from discord import app_commands
from bot.utils import db

CHESS_GREEN = discord.Color.from_rgb(29, 185, 84)
CHESS_SYMBOLS = ["♟️", "♙", "♜", "♖", "♞", "♘", "♝", "♗", "♛", "♕", "♚", "♔"]
CHESS_BOARD_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Chess_board_opening_staunton.png/320px-Chess_board_opening_staunton.png"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sm_events", description="List all upcoming Shellmates events")
    async def list_events(self, interaction: discord.Interaction):
        """Display the chessboard of upcoming events"""
        events = await db.get_events()
        if not events:
            embed = discord.Embed(
                title="♚ Empty events board ♚",
                description="*The board is clear... No events are scheduled yet.*\n\nUse `/sm_addevent` to plan the first event!",
                color=CHESS_GREEN
            )
            embed.set_thumbnail(url=CHESS_BOARD_URL)
            embed.set_footer(text="♟️ The pieces await your command ♟️")
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="♛ events board: Upcoming Shellmates Events ♛",
            description="*Strategic planning ahead! Schedule your participation wisely.*\n\u200b",
            color=CHESS_GREEN
        )
        embed.set_thumbnail(url=CHESS_BOARD_URL)
        embed.set_footer(text="♜ Check your schedule and join the events! ♜")
        
        toggle_index = 0
        for event in events:
            symbol = CHESS_SYMBOLS[toggle_index % len(CHESS_SYMBOLS)]
            toggle_index += 1
            
            field_value = (
                f"🏁 **Event Date:** {event['date']}\n"
                f"📜 **Event Description:** {event['description']}\n"
                f"⬆️ **Position:** {toggle_index} on the event list"
            )
            
            embed.add_field(
                name=f"{symbol} Event Title: {event['title']}",  # Changed this line
                value=field_value,
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sm_addevent", description="Add a new Shellmates event (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        title="Title of the event",
        day="Day of the event (1-31)",
        month="Month of the event (1-12)", 
        year="Year of the event (2024 or later)",
        description="Description of the event"
    )
    async def add_event(self, interaction: discord.Interaction, title: str, day: int, month: int, year: int, description: str):
        """Place a new event on the chessboard"""
        # Validate date inputs
        if day < 1 or day > 31:
            embed = discord.Embed(
                title="❌ Invalid Day ❌",
                description="*Day must be between 1 and 31!*\n\nPlease enter a valid day.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Check your date format ♜")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if month < 1 or month > 12:
            embed = discord.Embed(
                title="❌ Invalid Month ❌",
                description="*Month must be between 1 and 12!*\n\nPlease enter a valid month.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Check your date format ♜")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if year < 2025:
            embed = discord.Embed(
                title="❌ Invalid Year ❌",
                description="*Year must be 2024 or later!*\n\nPlease enter a valid year.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Check your date format ♜")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Additional validation for day-month combinations
        if month in [4, 6, 9, 11] and day > 30:  # Months with 30 days
            embed = discord.Embed(
                title="❌ Invalid Date ❌",
                description=f"*Month {month} only has 30 days!*\n\nPlease enter a valid day.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Check your date format ♜")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if month == 2:  # February
            # Simple leap year check
            is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            max_feb_days = 29 if is_leap_year else 28
            
            if day > max_feb_days:
                embed = discord.Embed(
                    title="❌ Invalid Date ❌",
                    description=f"*February {year} only has {max_feb_days} days!*\n\nPlease enter a valid day.",
                    color=discord.Color.red()
                )
                embed.set_footer(text="♜ Check your date format ♜")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        # Format the date as DD/MM/YYYY
        formatted_date = f"{day:02d}/{month:02d}/{year}"
        
        event_data = {
            'title': title,
            'date': formatted_date,  # Now using the formatted date
            'description': description,
            'created_by': interaction.user.id,
            'created_at': interaction.created_at.isoformat()
        }
        await db.add_event(event_data)
        
        embed = discord.Embed(
            title=f"🎯♞ New Event Added: {title} ♞🎯",
            description="*A new event appears on the chessboard!*",
            color=CHESS_GREEN
        )
        embed.add_field(name="📅 Event Date", value=f"🗓️ {formatted_date}", inline=True)
        embed.add_field(name="📋 Event Details", value=f"📝 {description}", inline=True)
        embed.add_field(name="👑 Organizer", value=f"🎖️ {interaction.user.display_name}", inline=True)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Chess_klt45.svg/800px-Chess_klt45.svg.png")
        embed.set_footer(text="♛ Prepare for the event! ♛")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sm_removeevent", description="Remove a Shellmates event (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(title="Title of the event to remove")
    async def remove_event(self, interaction: discord.Interaction, title: str):
        """Remove an event from the sevents board"""
        removed = await db.remove_event(title)
        if removed:
            embed = discord.Embed(
                title="♟️ Event Removed ♟️",
                description=f"*The event **'{title}'** has been removed from the board.*",
                color=CHESS_GREEN
            )
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Chess_piece_-_White_king.jpg/320px-Chess_piece_-_White_king.jpg")
            embed.set_footer(text="♚ The board evolves with each move ♚")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Event Not Found ❌",
                description=f"*No event found with the title: **{title}***\n\nCheck the event name and try again.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Verify the event title ♜")
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sm_clearevents", description="Clear all Shellmates events (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear_events(self, interaction: discord.Interaction):
        """Clear all events from the chessboard"""
        await db.clear_events()
        embed = discord.Embed(
            title="♛ Board Cleared ♛",
            description="*All events have been cleared from the board...*\n\nThe chessboard now awaits new event planning.",
            color=CHESS_GREEN
        )
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Chess_board.svg/320px-Chess_board.svg.png")
        embed.set_footer(text="♞ A fresh start for new events ♞")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="sm_modifyevent", 
        description="Modify an existing Shellmates event (Admin only)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        title="Title of the event you want to modify",
        new_title="New title for the event (leave empty to keep current)",
        new_date="New date for the event (leave empty to keep current)", 
        new_description="New description for the event (leave empty to keep current)"
    )
    async def modify_event(self, interaction: discord.Interaction, title: str, 
                         new_title: str = None, new_date: str = None, new_description: str = None):
        """Modify an event on the chessboard"""
        # Check if at least one field is being modified
        if new_title is None and new_date is None and new_description is None:
            embed = discord.Embed(
                title="❌ Modification Error ❌",
                description="*You must adjust at least one aspect of the event!*\n\nModify the title, date, or description to make your changes.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♝ A true planner always adapts ♝")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Call the database function to modify the event
        updated_event = await db.modify_event(
            title,
            new_title=new_title,
            new_date=new_date, 
            new_description=new_description
        )
        
        if updated_event:
            embed = discord.Embed(
                title=f"♚ Event Updated: {updated_event['title']} ♚",
                description="*Your event has been successfully modified!*",
                color=CHESS_GREEN
            )
            
            # Show what was changed
            changes = []
            if new_title is not None:
                changes.append(f"**🏷️ Event Title:** {title} → {new_title}")
            if new_date is not None:
                changes.append(f"**⏰ Event Date:** Schedule adjusted")
            if new_description is not None:
                changes.append(f"**📋 Event Details:** Description updated")
            
            if changes:
                embed.add_field(
                    name="📊 Modifications Made",
                    value="\n".join(changes),
                    inline=False
                )
            
            embed.add_field(name="🗓️ Current Date", value=f"📅 {updated_event['date']}", inline=True)
            embed.add_field(name="📜 Current Description", value=f"📝 {updated_event['description']}", inline=True)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Chess_kdl45.svg/800px-Chess_kdl45.svg.png")
            embed.set_footer(text="♛ Adaptability is the mark of a great organizer ♛")
            
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Event Not Found ❌",
                description=f"*No event found with the name: **{title}***\n\nCheck the event list and try again.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Verify the event name ♜")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @add_event.error
    @remove_event.error
    @modify_event.error
    @clear_events.error
    async def event_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Error handler for event commands with chess theme"""
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Access Denied 🚫",
                description="*You lack the permissions to manage events!*\n\nOnly administrators may organize these events.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♚ Admin privileges required ♚")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="💥 Operation Failed 💥",
                description=f"*An unexpected error occurred:*\n\n`{str(error)}`",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Try again later ♜")
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup the Events Command Center"""
    await bot.add_cog(Events(bot))

