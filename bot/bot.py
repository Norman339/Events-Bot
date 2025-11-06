import os
import sys
import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables from the project root and override shell values
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.utils import Config
from bot.utils.database import db

class CyberBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # Enable privileged intents (must be enabled in Discord Developer Portal)
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=Config.DEFAULT_PREFIX,
            intents=intents,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for /sm_help"
            )
        )
        
        self.initial_extensions = [
            'bot.cogs.events',
            'bot.cogs.facts',
            'bot.cogs.help'
        ]
        
        # Track whether commands have been synced to avoid duplicate syncs
        self._synced = False
    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Bot is in {len(self.guilds)} server(s)')
        print('Available commands:')
        for command in self.tree.get_commands():
            print(f'  /{command.name} - {command.description}')
        print('------')
        print('Bot is ready! Slash commands may take a few minutes to appear in Discord.')
        
        # Sync application commands once when the bot becomes ready
        if not self._synced:
            synced = await self.tree.sync()
            print(f"Commands synced! Total: {len(synced)} commands")
            for cmd in synced:
                print(f'  - Synced: /{cmd.name}')
            self._synced = True
    
    async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command):
        print(f'Command used: /{command.name} by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')

async def main():
    # Verify configuration
    Config.verify_config()
    
    # Create bot instance
    bot = CyberBot()
    
    # Initialize database and load extensions before starting the bot
    await db.client.admin.command('ping')
    print("Connected to MongoDB!")
    for ext in bot.initial_extensions:
        try:
            await bot.load_extension(ext)
            print(f"Loaded extension: {ext}")
        except Exception as e:
            print(f"Failed to load extension {ext}: {e}")
    
    # Start the bot
    await bot.start(Config.TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
