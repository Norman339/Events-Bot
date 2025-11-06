import discord
from discord.ext import commands
from discord import app_commands

CHESS_GREEN = discord.Color.from_rgb(29, 185, 84)
CHESS_SYMBOLS = ["♟️", "♙", "♜", "♖", "♞", "♘", "♝", "♗", "♛", "♕", "♚", "♔"]
CHESS_BOARD_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Chess_board_opening_staunton.png/320px-Chess_board_opening_staunton.png"

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Help cog initialized")

    @app_commands.command(name="sm_help", description="Show all available Shellmates bot commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="♛ Shellmates Command Center ♛",
            description="*Navigate the chessboard of commands with strategic precision!*\n\nHere are all the available moves for the Shellmates bot:",
            color=CHESS_GREEN
        )
        
        # Events commands section
        embed.add_field(
            name="🎯 Event Management ",
            value=(
                "`/sm_events` - Display all upcoming events on the chessboard\n"
                "`/sm_addevent` - Place a new event on the board (♚ Admin only)\n"
                "`/sm_removeevent` - Remove an event from the board (♚ Admin only)\n"
                "`/sm_clearevents` - Clear all events from the board (♚ Admin only)\n"
                "`/sm_modifyevent` - Reposition an existing event (♚ Admin only)\n"
            ),
            inline=False
        )
        
        # Facts commands section
        embed.add_field(
            name="🛡️ Security facts ",
            value=(
                "`/sm_fact` - Receive a random cybersecurity insight from the chess masters\n"
                "`/sm_addfact` - Add new strategic knowledge (♚ Admin only)\n"
                "`/sm_removefact` - Retire outdated insights (♚ Admin only)\n"
                "`/sm_listfacts` - Review the complete knowledge vault (♚ Admin only)\n"
            ),
            inline=False
        )
        
        # Help command section
        embed.add_field(
            name="ℹ️  Assistance",
            value=(
                "`/sm_help` - Display this strategic command overview\n"
            ),
            inline=False
        )
        
        # Additional chess-themed information
        embed.add_field(
            name="♟️ Daily facts ",
            value="*Automated cybersecurity facts are shared daily across all servers!*",
            inline=False
        )
        
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Chess_klt45.svg/800px-Chess_klt45.svg.png")
        embed.set_footer(text="♜ Shellmates Chess Club • Make your moves wisely! ♜")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))

