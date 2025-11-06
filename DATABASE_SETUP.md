# 🗄️ Database Setup Guide (MongoDB Only)

The bot now uses MongoDB exclusively for data storage. JSON files are no longer used.

## Quick Start (MongoDB Atlas or Local)

### 1) Configure `.env`
Create or update `.env` in the project root with:
```
DISCORD_TOKEN=your_bot_token_here
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
```
For local MongoDB, use:
```
MONGODB_URI=mongodb://localhost:27017
```

### 2) Verify DB connectivity
```bash
python test_db.py
```
You should see a successful MongoDB ping and CRUD operations.

### 3) Start the bot
```bash
python main.py
```

---

## MongoDB Setup Details

### Option A: Local MongoDB
1. **Install MongoDB**:
   - Windows: Download from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Linux: `sudo apt install mongodb`
   - Mac: `brew install mongodb-community`

2. **Start MongoDB**:
   ```bash
   # Windows
   net start MongoDB
   
   # Linux/Mac
   sudo systemctl start mongod
   ```

3. **Configure the bot**:
   Add to `.env`:
   ```
   DISCORD_TOKEN=your_bot_token_here
   MONGODB_URI=mongodb://localhost:27017
   ```

### Option B: MongoDB Atlas (Cloud)
1. **Create account** at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. **Create free cluster**
3. **Get connection string** (starts with `mongodb+srv://`)
4. **Configure .env file**:
   ```
   DISCORD_TOKEN=your_bot_token_here
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
   ```

---

## 🔧 Testing Commands

Once your bot is running, test these commands:

### Event Commands:
```
/sm_events          - List all events
/sm_addevent "Workshop" "2024-12-15" "Cybersecurity basics"  - Add event
/sm_removeevent "Workshop"  - Remove event
/sm_modifyevent "Workshop" new_description="Updated description"
```

### Fact Commands:
```
/sm_fact            - Get a random cybersecurity fact
/sm_addfact         - Add a new fact (Admin only)
/sm_removefact      - Remove a fact (Admin only)
/sm_listfacts       - List all facts (Admin only)
```

---

## 📊 Database Status Check

Run the test script to verify everything works:
```bash
python test_db.py
```

You should see output like:
```
🚀 Starting Database Test...
==================================================
✅ Connected to MongoDB (ping successful)
📊 Storage Method: MongoDB
...
✅ Database test completed successfully!
```

---

## 🛠️ Troubleshooting

### MongoDB Issues:
- **Connection failed**: Verify MongoDB is running and accessible
- **Authentication failed**: Check username/password in connection string
- **Network issues**: Ensure firewall allows MongoDB connections

### General Issues:
- **Module not found**: Run `pip install -r requirements.txt`
 - **Bot won't start**: Check Discord token and `MONGODB_URI` in `.env`