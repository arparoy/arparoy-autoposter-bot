import discord
from discord.ext import commands, tasks
import os
import itertools
import logging

# ================= CONFIG =================
CHANNEL_ID = 1454248846208139324
LINKS_FILE = "links.txt"
POST_INTERVAL_MINUTES = 1
STATUS_INTERVAL_MINUTES = 2  # Separate interval for status rotation
GUILD_ID = 1313110086910218331
AUTO_ROLE_ID = 1427593128264601682
# =========================================

# -------- LOGGING SETUP --------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# -------- INTENTS --------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # REQUIRED for on_member_join

bot = commands.Bot(command_prefix="!", intents=intents)

link_index = 0

# -------- ACTIVITY ROTATION -------- 
activities = itertools.cycle([
    discord.Streaming(
        name="Arpa Roy Onlyfans Collections",
        url="https://twitch.tv/arparoy"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Arpa Roy Screaming"
    ),
    discord.Activity(
        type=discord.ActivityType.watching,
        name="Arpa Roy Pussy"
    ),
    discord.Activity(
        type=discord.ActivityType.playing,
        name="Arpa Roy Boobs"
    ),
    discord.Activity(
        type=discord.ActivityType.competing,
        name="Arpa Roy Moaning"
    ),
    discord.Game(name="Discord Bot Simulator"),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Arpa Roy Ass Fucking"
    ),
    discord.Activity(
        type=discord.ActivityType.watching,
        name="Arpa Roy Fucking Pussy"
    ),
    discord.Activity(
        type=discord.ActivityType.playing,
        name="Arpa Roy Pussy & Boobs"
    ),
    discord.Streaming(
        name="Arpa Roy Nudes",
        url="https://arparoy-website.vercel.app"
    )
])

# -------- LOAD LINKS --------
def load_links():
    """Load links from the links file"""
    if not os.path.exists(LINKS_FILE):
        logger.warning(f"{LINKS_FILE} not found. Creating empty file.")
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write("")
        return []
    
    try:
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(links)} links from {LINKS_FILE}")
            return links
    except Exception as e:
        logger.error(f"Error loading links: {e}")
        return []

# -------- EVENTS --------
@bot.event
async def on_ready():
    logger.info(f"Bot online: {bot.user.name} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} server(s)")

    if not post_links.is_running():
        post_links.start()
        logger.info("Started link posting task")

    if not rotate_status.is_running():
        rotate_status.start()
        logger.info("Started status rotation task")

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Error in {event}: {args} {kwargs}")

@bot.event
async def on_member_join(member: discord.Member):
    # Ensure it's the correct server
    if member.guild.id != GUILD_ID:
        return

    role = member.guild.get_role(AUTO_ROLE_ID)
    if not role:
        logger.error("Auto role not found")
        return

    try:
        await member.add_roles(role, reason="Auto role on join")
        logger.info(f"Gave role '{role.name}' to {member.name}")
    except discord.Forbidden:
        logger.error("Missing permissions to assign roles")
    except Exception as e:
        logger.error(f"Error assigning role: {e}")

# -------- LINK POSTER --------
@tasks.loop(minutes=POST_INTERVAL_MINUTES)
async def post_links():
    """Post links from the file to the specified channel"""
    global link_index

    links = load_links()
    if not links:
        logger.warning("No links to post")
        return

    if link_index >= len(links):
        link_index = 0
        logger.info("Restarting link rotation")

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        logger.error(f"Channel {CHANNEL_ID} not found")
        return

    try:
        await channel.send(links[link_index])
        logger.info(f"Posted link {link_index + 1}/{len(links)}: {links[link_index][:50]}...")
        link_index += 1
    except discord.errors.Forbidden:
        logger.error("Missing permissions to send messages in the channel")
    except Exception as e:
        logger.error(f"Error posting link: {e}")

@post_links.before_loop
async def before_post_links():
    await bot.wait_until_ready()

@post_links.error
async def post_links_error(error):
    logger.error(f"Error in post_links task: {error}")

# -------- STATUS ROTATION --------
@tasks.loop(minutes=STATUS_INTERVAL_MINUTES)
async def rotate_status():
    """Rotate bot's activity status"""
    try:
        activity = next(activities)
        await bot.change_presence(activity=activity)
        logger.info(f"Changed status to: {activity.name}")
    except Exception as e:
        logger.error(f"Error rotating status: {e}")

@rotate_status.before_loop
async def before_rotate_status():
    await bot.wait_until_ready()

@rotate_status.error
async def rotate_status_error(error):
    logger.error(f"Error in rotate_status task: {error}")

# -------- RUN BOT --------
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN environment variable is not set")
    
    logger.info("Starting bot...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
