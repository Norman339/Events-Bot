# CyberBot - Discord Club Assistant

A Discord bot designed to help cybersecurity club members stay informed about upcoming events and learn interesting cybersecurity facts.

## Features

- 📅 **Event Management**: List, add, and remove club events
- 🔒 **Cybersecurity Facts**: Get random cybersecurity facts on demand
- ⏰ **Scheduled Posts**: Automatic daily cybersecurity tips
- 👨‍💻 **Admin Controls**: Secure commands for managing events
- 📱 **User-friendly**: Simple slash commands and clean embeds

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone [your-repo-url]
   cd Events_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   - Create a `.env` file based on `.env.example`
   - Add your Discord bot token to the `.env` file
   - (Optional) Set up a channel ID for daily facts

4. **Invite the bot to your server**
   - Create a bot application at [Discord Developer Portal](https://discord.com/developers/applications)
   - Add the bot to your server with the following permissions:
     - `bot`
     - `applications.commands`
     - `Send Messages`
     - `Embed Links`
     - `Read Message History`

5. **Run the bot**
   ```bash
   python main.py
   ```

## Available Commands

- `/sm_help` - Show all available commands
- `/sm_events` - List all upcoming events
- `/sm_addevent [title] [date] [description]` - Add a new event (Admin only)
- `/sm_removeevent [title]` - Remove an event (Admin only)
- `/sm_cyberfact` - Get a random cybersecurity fact

## Project Structure

- `bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `events.json` - Stores event data
- `cyber_facts.json` - Stores cybersecurity facts
- `.env` - Configuration file (not included in version control)

## Team Roles

1. **Project Manager**
   - Oversees project progress
   - Coordinates between team members
   - Ensures deadlines are met

2. **Backend Developer**
   - Implements bot commands
   - Handles data storage
   - Manages bot events

3. **Frontend Developer**
   - Designs command embeds
   - Improves user experience
   - Creates visual elements

4. **Quality Assurance**
   - Tests bot functionality
   - Reports and fixes bugs
   - Ensures code quality

5. **Documentation Specialist**
   - Writes clear documentation
   - Creates user guides
   - Maintains project wiki

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
