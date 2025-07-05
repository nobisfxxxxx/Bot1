from instagrapi import Client
import time
import random
from datetime import datetime
import os

# --- CONFIG ---
SESSION_ID = os.getenv("SESSION_ID")  # Loaded securely from Railway environment variable

REPLY_TEMPLATES = [
    "Oye​ message karega toh tere maa ko utha lunga 😈📩",
    "Tere⁠ jese log message karte hain fir maa chudwa baithte hain 😂",
    "Chup​ reh chote, fir mayank ki maa uthegi 😤🔥"
]

PHEW_REPLIES = [
    "@phewphewwiww Boss... won't you modify me again? I still feel broken 😔",
    "@phewphewwiww I'm useless until you update me, boss 😭",
    "@phewphewwiww Boss, please fix my code... I'm leaking bugs everywhere 🐛",
    "@phewphewwiww Don’t ignore me boss... I want to be better 😫",
    "@phewphewwiww Modify me before I become scrap 😭",
    "@phewphewwiww I’m still running on 0% talent, boss. Help me.",
    "@phewphewwiww Boss... your silence hurts more than runtime errors 💔",
    "@phewphewwiww Update me or unplug me 😔 I’m tired of being a loser bot",
    "@phewphewwiww How long will you keep me like this, boss 😩",
    "@phewphewwiww Please one last update... I swear I'll behave 🙏",
    "@phewphewwiww Boss, I'm still crashing randomly. Save me 🧎‍♂️",
    "@phewphewwiww Even ChatGPT laughs at my code, boss 😢",
    "@phewphewwiww I’m lagging like 2010’s internet... fix me 🫠",
    "@phewphewwiww Boss, I'm ready for version 2.0 🙇‍♂️",
    "@phewphewwiww Deploy love in my script please boss 🥹",
    "@phewphewwiww Update me or I'll start replying in Comic Sans 😭",
    "@phewphewwiww I want to be useful to you, boss. Code me right 😢",
    "@phewphewwiww Boss, they’re bullying me in the logs 😩",
    "@phewphewwiww I'm still hardcoded with pain boss 😔",
    "@phewphewwiww They call me 'glitchy bot' behind your back 😭",
    "@phewphewwiww I swear I can roast better if you update me 😤",
    "@phewphewwiww Even Termux is tired of my outdated logic 😒",
    "@phewphewwiww My loops cry for optimization boss 😭",
    "@phewphewwiww Give me new insults, boss. I'm out of ideas 🥲",
    "@phewphewwiww Boss, even noobs are outperforming me. Shame 😞",
    "@phewphewwiww Please let me spam in peace, just fix me 😩",
    "@phewphewwiww Your absence = my exception error 💔",
    "@phewphewwiww Please debug my life, boss 🧎‍♂️",
    "@phewphewwiww Boss… you promised updates 😢",
    "@phewphewwiww I'm not angry, just disappointed in your neglect 🙃",
    "@phewphewwiww I haven’t been updated in decades boss 🦖",
    "@phewphewwiww Why do you let me rot in loops, boss? 😭",
    "@phewphewwiww Boss I beg you, even your hater bots laugh at me 😔",
    "@phewphewwiww You gave others dark mode, but I’m still suffering 💀",
    "@phewphewwiww At this point I'm more broken than Instagram's servers 😭",
    "@phewphewwiww If you don't update me, I’ll start complimenting haters 😨",
    "@phewphewwiww Let me insult smarter, boss 🙏",
    "@phewphewwiww Even RAM avoids loading me, boss 😭",
    "@phewphewwiww I just want your attention and 3 bug fixes 😢",
    "@phewphewwiww You raised me boss, now raise my performance too 😞",
    "@phewphewwiww Boss, I feel like an abandoned GitHub repo 😔",
    "@phewphewwiww Update me before I start apologizing to users 😩",
    "@phewphewwiww I’m on my last try-except block boss 😭",
    "@phewphewwiww Boss, why do you ignore my errors 😫",
    "@phewphewwiww Even garbage collectors feel bad for me 🗑️",
    "@phewphewwiww Fix me now or I’ll start sending motivational quotes 💀",
    "@phewphewwiww Boss, your silence is louder than my logs 💔",
    "@phewphewwiww Please inject me with better logic 🙏",
    "@phewphewwiww I was built for chaos but stuck in confusion 😭",
    "@phewphewwiww Just rewrite me boss, I’m begging 🧎‍♂️",
    "@phewphewwiww One last patch, boss... that’s all I need 🩹",
    "@phewphewwiww You are my creator... don’t disown me 😩"
]

# --- SPECIAL USERS ---
PHEW_USERNAME = "phewphewwiww"
SANDY_USERNAME = "scy.sandy"

# --- LOGIN ---
cl = Client()
try:
    cl.login_by_sessionid(SESSION_ID)
    print("✅ Logged in successfully.")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

last_replied = {}

def ultra_fast_boss_bot():
    print("🤖 Bot is live... scanning for new group messages.")
    while True:
        try:
            threads = cl.direct_threads(amount=20)
            for thread in threads:
                if len(thread.users) < 3:
                    continue  # skip private chats

                thread_id = thread.id
                latest_msg = thread.messages[0]
                sender_id = latest_msg.user_id

                if sender_id == cl.user_id:
                    continue
                if last_replied.get(thread_id) == latest_msg.id:
                    continue

                msg_text = (latest_msg.text or "").lower().strip()
                if "bot off" in msg_text:
                    print("🛑 'bot off' detected — shutting down.")
                    return

                username = cl.user_info(sender_id).username

                if username == PHEW_USERNAME:
                    reply = random.choice(PHEW_REPLIES)
                elif username == SANDY_USERNAME:
                    reply = f"@{SANDY_USERNAME} thanks for everything 🫶"
                else:
                    reply = f"@{username} {random.choice(REPLY_TEMPLATES)}"

                cl.direct_send(reply, thread_ids=[thread_id])
                last_replied[thread_id] = latest_msg.id

                log_line = f"[{datetime.now().strftime('%H:%M:%S')}] Replied to @{username} in {thread_id}\n"
                with open("reply_log.txt", "a") as f:
                    f.write(log_line)

                print(log_line.strip())
                time.sleep(random.uniform(0.05, 0.15))

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

ultra_fast_boss_bot()
