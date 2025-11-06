import random
import discord
from discord.ext import commands, tasks
from discord import app_commands
from bot.utils import db

CHESS_GREEN = discord.Color.from_rgb(29, 185, 84)
CHESS_SYMBOLS = ["♟️", "♙", "♜", "♖", "♞", "♘", "♝", "♗", "♛", "♕", "♚", "♔"]
CHESS_BOARD_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Chess_board_opening_staunton.png/320px-Chess_board_opening_staunton.png"

class Facts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_fact.start()

    # ------------------------------
    # Command: Get Random Fact
    # ------------------------------
    @app_commands.command(name="sm_fact", description="Get a random Shellmates cybersecurity fact!")
    async def cyberfact(self, interaction: discord.Interaction):
        """Display a strategic cybersecurity fact"""
        fact = await db.get_random_fact()
        if not fact:
            embed = discord.Embed(
                title="♟️ No Facts Available",
                description="*The knowledge vault is currently empty...*",
                color=CHESS_GREEN
            )
            embed.set_thumbnail(url=CHESS_BOARD_URL)
            embed.set_footer(text="♜ Use /sm_addfact to share your wisdom ♜")
            await interaction.response.send_message(embed=embed)
            return

        symbol = random.choice(CHESS_SYMBOLS)
        embed = discord.Embed(
            title=f"{symbol} Security Fact {symbol}",
            description=f"```\n{fact}\n```",
            color=CHESS_GREEN
        )
        embed.set_thumbnail(url=CHESS_BOARD_URL)
        embed.set_footer(text="♛ Knowledge is your strongest defense ♛")

        await interaction.response.send_message(embed=embed)

    # ------------------------------
    # Command: Add New Fact (Admin)
    # ------------------------------
    @app_commands.command(name="sm_addfact", description="[Admin] Add a new cybersecurity fact")
    @app_commands.describe(fact="The cybersecurity fact to add")
    @app_commands.checks.has_permissions(administrator=True)
    async def addfact(self, interaction: discord.Interaction, fact: str):
        """Add a new piece of strategic knowledge to the vault"""
        await db.add_fact(fact)
        
        embed = discord.Embed(
            title=f"✅♞ New Security Fact Added ♞✅",
            description="*Your wisdom has been recorded in the knowledge vault!*",
            color=CHESS_GREEN
        )
        embed.add_field(
            name="📜 Security Fact", 
            value=f"```{fact}```", 
            inline=False
        )
        embed.add_field(
            name="👑 Added By", 
            value=f"🎖️ {interaction.user.display_name}", 
            inline=True
        )
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Chess_klt45.svg/800px-Chess_klt45.svg.png")
        embed.set_footer(text="♛ Your move strengthens our defenses ♛")
        
        await interaction.response.send_message(embed=embed)

    # ------------------------------
    # Command: Remove Fact (Admin)
    # ------------------------------
    @app_commands.command(name="sm_removefact", description="[Admin] Remove a cybersecurity fact")
    @app_commands.describe(fact="The exact text of the fact to remove")
    @app_commands.checks.has_permissions(administrator=True)
    async def removefact(self, interaction: discord.Interaction, fact: str):
        """Remove outdated knowledge from the vault"""
        success = await db.remove_fact(fact)
        
        if success:
            embed = discord.Embed(
                title="♟️ Fact Retired ♟️",
                description=f"*The following fact has been removed from our playbook:*",
                color=CHESS_GREEN
            )
            embed.add_field(
                name="📜 Retired Fact",
                value=f"```{fact}```",
                inline=False
            )
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Chess_piece_-_White_king.jpg/320px-Chess_piece_-_White_king.jpg")
            embed.set_footer(text=f"♜ Retired by {interaction.user.display_name} ♜")
        else:
            embed = discord.Embed(
                title="❌ Strategic Error ❌",
                description="*This fact was not found in our knowledge base.*\n\nCheck your notation and try again.",
                color=discord.Color.red()
            )
            embed.set_footer(text="♝ Verify the exact wording ♝")
        
        await interaction.response.send_message(embed=embed)

    # ------------------------------
    # Command: List All Facts (Admin)
    # ------------------------------
    @app_commands.command(name="sm_listfacts", description="[Admin] View all cybersecurity facts in the database")
    @app_commands.checks.has_permissions(administrator=True)
    async def listfacts(self, interaction: discord.Interaction):
        """Review the complete knowledge base"""
        facts = await db.get_all_facts()
        
        if not facts:
            embed = discord.Embed(
                title="♟️ Empty Knowledge Vault ♟️",
                description="*No facts are currently recorded.*\n\nUse `/sm_addfact` to begin building our defenses!",
                color=CHESS_GREEN
            )
            embed.set_footer(text="♜ The vault awaits your wisdom ♜")
            await interaction.response.send_message(embed=embed)
            return
        
        # Show first page
        description = ""
        for i, fact in enumerate(facts, start=1):
            symbol = CHESS_SYMBOLS[(i-1) % len(CHESS_SYMBOLS)]
            description += f"{symbol} **{i}.** {fact}\n\n"
        
        embed = discord.Embed(
            title="♛ Security Facts Collection ♛",
            description=description,
            color=CHESS_GREEN
        )
        embed.set_thumbnail(url=CHESS_BOARD_URL)
        embed.set_footer(
            text=f"Total Facts: {len(facts)} • Knowledge Base"
        )
        
        await interaction.response.send_message(embed=embed)

    # ------------------------------
    # Daily Fact Automation (24 hours)
    # ------------------------------
    @tasks.loop(hours=24)
    async def daily_fact(self):
        """Automatically send a daily cybersecurity fact"""
        # You can specify a channel ID here, or get it from a config
        # For now, I'll send to the first text channel of each guild the bot is in
        for guild in self.bot.guilds:
            # Find a suitable channel to send the fact
            channel = None
            for text_channel in guild.text_channels:
                if text_channel.permissions_for(guild.me).send_messages:
                    channel = text_channel
                    break
            
            if channel:
                fact = await db.get_random_fact()
                if fact:
                    symbol = random.choice(CHESS_SYMBOLS)
                    embed = discord.Embed(
                        title=f"{symbol} Daily Security Fact {symbol}",
                        description=f"```\n{fact}\n```",
                        color=CHESS_GREEN
                    )
                    embed.set_thumbnail(url=CHESS_BOARD_URL)
                    embed.set_footer(
                        text=f"♛ Daily Security Update • {discord.utils.utcnow().strftime('%B %d, %Y')} ♛"
                    )

                    try:
                        await channel.send(embed=embed)
                    except:
                        continue  # If we can't send in one channel, try others

    @daily_fact.before_loop
    async def before_daily_fact(self):
        """Wait until the bot is ready before starting the daily fact loop"""
        await self.bot.wait_until_ready()

    def cog_unload(self):
        """Cancel the daily fact task when the cog is unloaded"""
        self.daily_fact.cancel()

    # ------------------------------
    # Unified Error Handler
    # ------------------------------
    @addfact.error
    @removefact.error
    @listfacts.error
    async def fact_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Error handler for fact commands with chess theme"""
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Royal Decree Required 🚫",
                description="*Only administrators may modify the knowledge base!*",
                color=discord.Color.red()
            )
            embed.set_footer(text="♚ Administrator privileges needed ♚")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="💥 Operation Failed 💥",
                description=f"*An unexpected error occurred:*\n\n`{str(error)}`",
                color=discord.Color.red()
            )
            embed.set_footer(text="♜ Try again later ♜")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        """Initialize default facts when the bot starts"""
        await db.initialize_default_facts()

async def setup(bot):
    """Setup the Facts Command Center"""
    await bot.add_cog(Facts(bot))
