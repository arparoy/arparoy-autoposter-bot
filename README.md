
# ArpaRoy AutoPoster 🤖

ArpaRoy AutoPoster is a Discord bot built with **discord.py** that automatically posts links to a channel, rotates bot status activities, and assigns roles to new members.

## ✨ Features
- 🔁 Automatic link posting from `links.txt`
- ⏱️ Configurable posting interval
- 🎭 Rotating bot activity/status
- 👤 Auto-role assignment on member join
- 📝 Simple logging for monitoring

## 🧰 Tech Stack
- Python 3.10+
- discord.py
- asyncio tasks

## ⚙️ Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your bot token:
```
export DISCORD_TOKEN=your_token_here
```

3. Configure IDs in bot.py:
```
Channel ID

Guild ID

Role ID

```

4. Run the bot:
```
python bot.py
```


📌 Notes

Ensure the bot has Message, Member, and Role permissions.

links.txt should contain one link per line.

