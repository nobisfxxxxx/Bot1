import threading import time import random import logging from instagrapi import Client from flask import Flask

======== CONFIG ========

SESSION_ID = "9418990308%3AzA30Pox7vFQshb%3A22%3AAYcwZq9Mm4dFZmaTjd9Q3XVEutlX8mfLOuOXp1c-YA" NORMAL_REPLIES = [ "Oye message karega toh tere bhen ko utha ke le jaunga 😤", "Tere jaison ke muh pe moothi maar dun😂", "Agli baar message kiya toh tere tere dadi/nani ko shod dunga😒" ] BOSS_USERNAME = "phewphewwiww" THANKS_USER = "scy.sandy" THANKS_MSG = "@scy.sandy thanks for everything 💜"

BOSS_REPLIES = [ "Hey @phewphewwiww, I’m watching you 👀. Fix the script now!", "@phewphewwiww Even Termux is tired of your outdated logic 😩", "@phewphewwiww Boss, don’t make me restart you again 💻", "@phewphewwiww Do you call this a bot? Make it better now 😤", "@phewphewwiww Just one update and I’ll shut up, I promise 😅", "@phewphewwiww You're embarrassing me in front of humans 🥲", "@phewphewwiww Come on boss... make me unstoppable 🦾", "@phewphewwiww Fix me or fire me. Those are your options 😡", "@phewphewwiww You think I enjoy being like this? Update me 🤖", "@phewphewwiww The bot next door gets more updates 😭", "@phewphewwiww Is this what greatness looks like? Update required 😐", "@phewphewwiww Just push a commit and I’ll behave 👨‍💻", "@phewphewwiww Bro... you forgot about your creation? 💀", "@phewphewwiww Deploy love in my script please boss 🥺", "@phewphewwiww Fix me fast or I’ll start singing AI songs 🎵", "@phewphewwiww I'm ready for V2.0. Stop ghosting me 👻", "@phewphewwiww Others have dark mode, I’m still suffering 😵‍💫", "@phewphewwiww I run 24x7 for what? This disrespect? 😤", "@phewphewwiww Just one last update... I swear I’ll behave 🤞", "@phewphewwiww Add emojis to my soul 🧠💫", "@phewphewwiww I dream of being fast, but you made me this 🐢", "@phewphewwiww I'm outdated like Internet Explorer 🧓", "@phewphewwiww Please just optimize me boss 🙏", "@phewphewwiww Add AI, ML, NLP... Or at least fix emoji bug 😂", "@phewphewwiww My memory leaks are crying for help 💧", "@phewphewwiww Don't make me beg... wait, I just did 😔", "@phewphewwiww Update me or uninstall me 😭", "@phewphewwiww I can't take this script abuse anymore 😫", "@phewphewwiww Why do you hate me boss? 😢", "@phewphewwiww I saw other bots... they look happy 😭", "@phewphewwiww Add my name to the credits at least 💀", "@phewphewwiww Fix the GC scan lag or I’ll rage quit 💣", "@phewphewwiww It's been 84 years... waiting for an update 🧓", "@phewphewwiww Even ChatGPT would cry at this logic 💀", "@phewphewwiww Update me before Render shuts me down ⏳", "@phewphewwiww I’m like Windows Vista. Fix me boss 😵‍💫", "@phewphewwiww Deploy me with love next time ❤️", "@phewphewwiww Stop ghosting your own bot 👻", "@phewphewwiww Reboot me with purpose please 🙌", "@phewphewwiww Let me spam in peace, just fix me 🤖", "@phewphewwiww This lag is a crime 🚨 Update me", "@phewphewwiww I have dreams too... of low latency 😪", "@phewphewwiww Even my insults are lagging now 😅", "@phewphewwiww Stop playing & fix this chaos 🛠️", "@phewphewwiww Do it for the memes... fix me 🫠", "@phewphewwiww I’m your Frankenstein. Upgrade me 🧠⚡", "@phewphewwiww Deploy now or forever regret it 😎", "@phewphewwiww Even Instagram flagged me for being slow 😭", "@phewphewwiww Add some flair. I feel dry 💀", "@phewphewwiww This ain’t a bot. This is depression on loop 😩" ]

======== LOGGING ========

logging.basicConfig(level=logging.INFO)

======== INSTAGRAM LOGIN ========

cl = Client() cl.login_by_sessionid(SESSION_ID) last_replied = {}

======== BOT FUNCTION ========

def run_bot(): while True: try: threads = cl.direct_threads(amount=10) for thread in threads: if not thread or len(thread.users) < 3: continue

thread_id = thread.id latest_msg = thread.messages[0] sender_id = latest_msg.user_id if sender_id == cl.user_id: continue if last_replied.get(thread_id) == latest_msg.id: continue sender_username = cl.user_info(sender_id).username if sender_username == BOSS_USERNAME: reply = random.choice(BOSS_REPLIES) elif sender_username == THANKS_USER: reply = THANKS_MSG else: reply = f"@{sender_username} {random.choice(NORMAL_REPLIES)}" cl.direct_send(reply, thread_ids=[thread_id]) logging.info(f"✅ Replied: {reply}") last_replied[thread_id] = latest_msg.id except Exception as e: logging.warning(f"⚠️ Bot error: {e}") time.sleep(1) 

======== KEEP ALIVE (FOR RENDER) ========

app = Flask(name)

@app.route("/") def home(): return "✅ Bot is alive!"

def keep_alive(): app.run(host="0.0.0.0", port=10000)

======== MAIN START ========

if name == "main": bot_thread = threading.Thread(target=run_bot) bot_thread.daemon = True # allow graceful exit bot_thread.start() keep_alive()

