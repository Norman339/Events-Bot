import random
import discord
from discord.ext import commands
from discord import app_commands
from bot.utils import db

class Facts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sm_fact", description="Get a random Shellmates cybersecurity fact")
    async def cyber_fact(self, interaction: discord.Interaction):
        fact = await db.get_random_fact()
        if not fact:
            await interaction.response.send_message("No facts available!")
            return
            
        embed = discord.Embed(
            title="🔒 Did You Know?",
            description=fact,
            color=discord.Color.gold()
        )
        embed.set_footer(text="Stay secure!")
        
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        # Initialize default facts if none exist
        await db.initialize_default_facts()

async def setup(bot):
    await bot.add_cog(Facts(bot))
