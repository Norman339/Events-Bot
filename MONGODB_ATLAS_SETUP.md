# 🌐 MongoDB Atlas Setup Guide (Cloud Database)

## ✅ Why MongoDB Atlas?
- **No installation required** - Everything runs in the cloud
- **Free tier available** - Perfect for small projects
- **Always online** - Your data is accessible 24/7
- **Automatic backups** - Your data is safe
- **Global access** - Connect from anywhere

---

## 🚀 Step-by-Step Setup

### Step 1: Create Account
1. **Visit:** https://www.mongodb.com/atlas
2. **Click:** "Try Free"
3. **Sign up** with email or Google account
4. **Verify email** if required

### Step 2: Create Your Free Cluster
1. **After login, click:** "Build a Cluster"
2. **Choose:** "Shared" (free tier)
3. **Select cloud provider:** (AWS, Google Cloud, or Azure)
4. **Choose region:** Pick one close to you
5. **Click:** "Create Cluster" (wait ~5 minutes)

### Step 3: Configure Database Access
1. **In left sidebar, click:** "Database Access"
2. **Click:** "Add New Database User"
3. **Enter credentials:**
   ```
   Username: your_bot_user
   Password: your_secure_password
   ```
4. **Set privileges:** "Read and write to any database"
5. **Click:** "Add User"

### Step 4: Configure Network Access
1. **In left sidebar, click:** "Network Access"
2. **Click:** "Add IP Address"
3. **Click:** "Allow Access from Anywhere"
4. **Enter:** `0.0.0.0/0`
5. **Click:** "Confirm"

### Step 5: Get Your Connection String
1. **In left sidebar, click:** "Clusters"
2. **Click:** "Connect" button on your cluster
3. **Choose:** "Connect your application"
4. **Select driver:** "Python"
5. **Copy connection string** (will look like this):
   ```
   mongodb+srv://your_bot_user:your_password@cluster0.xxxxx.mongodb.net/
   ```

---

## 🔧 Configure Your Bot

### 1. Create `.env` file:
```env
DISCORD_TOKEN=your_discord_bot_token_here
MONGODB_URI=mongodb+srv://your_bot_user:your_password@cluster0.xxxxx.mongodb.net/
DEFAULT_PREFIX=!
```

### 2. Enable MongoDB in your bot:
**Edit:** `bot/utils/database.py` line 178
```python
db = Database(use_mongodb=True)  # Change from False to True
```

### 3. Test your connection:
```bash
python test_db.py
```

---

## 📊 Your Atlas Dashboard
After setup, you'll see:
- **Cluster name** (e.g., "Cluster0")
- **Connection string** (for your .env file)
- **Database users** (who can access your data)
- **Network access** (who can connect)
- **Storage usage** (how much free space you've used)

---

## 🎯 Next Steps
1. **Create your Atlas account** (5 minutes)
2. **Set up your cluster** (5 minutes)
3. **Configure bot** (2 minutes)
4. **Test connection** (1 minute)
5. **Start your bot!**

---

## 💡 Pro Tips
- **Free tier limits:** 512MB storage, shared CPU
- **Backup:** Automatic daily backups on free tier
- **Monitoring:** Check usage in Atlas dashboard
- **Security:** Always use strong passwords
- **Best practice:** Create separate database users for different applications

---

## 🆘 Need Help?
- **MongoDB Documentation:** https://docs.mongodb.com/
- **Atlas Support:** https://support.mongodb.com/
- **Community Forums:** https://community.mongodb.com/

**Ready to start?** Click here: https://www.mongodb.com/atlas