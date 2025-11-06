# 🚀 Quick Start Guide - CyberBot (MongoDB)

Run the bot with MongoDB (Atlas or local). JSON files are no longer used.

## 1) Install Dependencies
```bash
pip install -r requirements.txt
```

## 2) Configure `.env`
Create a `.env` file in the project root with:
```
DISCORD_TOKEN=your_bot_token_here
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
```
For local MongoDB:
```
MONGODB_URI=mongodb://localhost:27017
```

## 3) Start the Bot
```bash
python main.py
```

## 4) Test Commands in Discord
Once your bot is online, try these commands:

**Event Commands:**
```
/sm_events                    # List all events
/sm_addevent "CTF Contest" "2024-12-25" "Annual hacking competition"  # Add event
/sm_modifyevent               # Edit an event (admin)
/sm_clearevents               # Clear all events (admin)
```

**Fact Commands:**
```
/sm_fact                      # Get a random cybersecurity fact
/sm_addfact                   # Add a fact (admin)
/sm_removefact                # Remove a fact (admin)
/sm_listfacts                 # List all facts (admin)
/sm_help                      # Show all commands
```

## Storage Details
- Storage: MongoDB database specified via `MONGODB_URI`
- JSON files are not used anymore

## Troubleshooting
- Bot not starting: Check `DISCORD_TOKEN` and `MONGODB_URI` in `.env`
- MongoDB errors: Verify `MONGODB_URI`, credentials, and network connectivity
- Missing modules: `pip install -r requirements.txt`