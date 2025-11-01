import os
import sys
import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.utils import Config
from bot.utils.database import db

class CyberBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # Disable privileged intents if not enabled in Discord Developer Portal
        intents.message_content = False
        intents.members = False
        
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
    
    async def setup_hook(self):
        # Initialize database connection
        if db.use_mongodb:
            await db.client.admin.command('ping')
            print("Connected to MongoDB!")
        else:
            print("Using JSON file storage")
        
        # Load all extensions
        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
                print(f"Loaded extension: {ext}")
            except Exception as e:
                print(f"Failed to load extension {ext}: {e}")
        
        # Sync application commands (don't clear them!)
        synced = await self.tree.sync()
        print(f"Commands synced! Total: {len(synced)} commands")
        for cmd in synced:
            print(f"  - Synced: /{cmd.name}")
    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Bot is in {len(self.guilds)} server(s)')
        print('Available commands:')
        for command in self.tree.get_commands():
            print(f'  /{command.name} - {command.description}')
        print('------')
        print('Bot is ready! Slash commands may take a few minutes to appear in Discord.')
    
    async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command):
        print(f'Command used: /{command.name} by {interaction.user} in {interaction.guild.name if interaction.guild else "DM"}')

async def main():
    # Verify configuration
    Config.verify_config()
    
    # Create bot instance
    bot = CyberBot()
    
    # Start the bot
    await bot.start(Config.TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
