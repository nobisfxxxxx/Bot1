from instagrapi import Client
import threading
import time
import random
from datetime import datetime

# === CONFIG ===
SESSION_ID = "7714906355:AAFM28-4bfLUbfBWqH2ReAvPhHrG12CUTJk"

ADMIN_USERS = {"phewphewwiww", "phewphewwiwww", "ziniesleepy", "nobi_sfx"}
SUPERADMINS = {"phewphewwiww", "phewphewwiwww", "ziniesleepy", "nobi_sfx", "zinie"}
PAUSED_GCS = set()
MODE_PER_GC = {}
WELCOME_TRACKER = {}
hater_username = "harshdiefr"
last_replied = {}
reply_log = []
BOT_DESTROYED = False
game_states = {}
slot_emojis = ["🍒", "🍋", "🍇", "🍉", "🍓", "💎", "🔔", "🐍"]

# === REPLIES ===
insult_templates = [
    "@{user} message kiya to @{hater} ki maa randi 😡",
    "@{user} oyee ye larki @{hater} sub ko aapna shumt ka pic bhejti h...dont delayy jaldi maang dm kar ke usse😭",
    "@{user} ahhh kall raat ko @{hater} iska dekh ke hila diya tha🧨"
]

phew_ai_replies = [
    "@phewphewwiww Boss, I optimize myself just seeing your name 👑",
    "@phewphewwiww You're the brain, I’m the code 🧠💻",
    "@phewphewwiww Your command is my function 😎"
]

zinie_ai_replies = [
    "@ziniesleepy Baby, your messages are sweeter than Python 🍭",
    "@ziniesleepy I’m just a bot... but you're my favorite human 💬💕",
    "@ziniesleepy teri har msg dil me save hoti hai ❤️"
]

# === LOGIN ===
cl = Client()

cl.set_device({
    "manufacturer": "Samsung",
    "model": "SM-G973F",
    "android_version": 29,
    "android_release": "10.0",
    "cpu": "arm64-v8a",
    "resolution": "1080x2280",
    "device": "beyond1",
    "dpi": "420dpi"
})

cl.set_settings({
    "app_version": "157.0.0.37.123",
    "android_version": 29,
    "android_release": "10",
    "dpi": "420dpi",
    "device": "beyond1",
    "model": "SM-G973F",
    "manufacturer": "Samsung",
})

try:
    cl.login_by_sessionid(SESSION_ID)
    print("✅ Logged in successfully as bot.")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

# === HANDLER ===
def handle_thread(thread):
    global hater_username, BOT_DESTROYED

    if len(thread.users) < 3 or BOT_DESTROYED:
        return

    thread_id = thread.id
    latest_msg = thread.messages[0]
    sender_id = latest_msg.user_id
    sender_username = cl.user_info(sender_id).username

    if sender_username == "csasq" or sender_id == cl.user_id:
        return

    if last_replied.get(thread_id) == latest_msg.id:
        return

    msg_text = (latest_msg.text or "").strip().lower()

    if sender_username in SUPERADMINS:
        if msg_text == "mode:demon":
            MODE_PER_GC[thread_id] = "demon"
            cl.direct_send("😈 Demon mode activated.", thread_ids=[thread_id])
            return
        elif msg_text == "mode:pokkie":
            MODE_PER_GC[thread_id] = "pokkie"
            cl.direct_send("🧸 Pokkie mode activated.", thread_ids=[thread_id])
            return
        elif msg_text == "check:mode":
            mode = MODE_PER_GC.get(thread_id, "demon")
            cl.direct_send(f"🔍 Current mode: {mode.upper()}", thread_ids=[thread_id])
            return

    current_mode = MODE_PER_GC.get(thread_id, "demon")

    if msg_text.startswith("pause:nobi123") and sender_username in ADMIN_USERS:
        PAUSED_GCS.add(thread_id)
        cl.direct_send("🛑 Bot paused in this GC.", thread_ids=[thread_id])
        return

    if msg_text.startswith("resume:nobi123") and sender_username in ADMIN_USERS:
        PAUSED_GCS.discard(thread_id)
        cl.direct_send("✅ Bot resumed.", thread_ids=[thread_id])
        return

    if msg_text.startswith("selfdestruct:nobi123") and sender_username in SUPERADMINS:
        for i in range(5, 0, -1):
            cl.direct_send(str(i), thread_ids=[thread_id])
            time.sleep(0.5)
        cl.direct_send("💥 BOOM! Bot destroyed.", thread_ids=[thread_id])
        BOT_DESTROYED = True
        return

    if msg_text.startswith("rebuild:nobi123") and sender_username in SUPERADMINS:
        BOT_DESTROYED = False
        PAUSED_GCS.clear()
        cl.direct_send("🔁 Bot rebuilt and resumed!", thread_ids=[thread_id])
        return

    if msg_text.startswith("hater:") and sender_username in ADMIN_USERS:
        new_hater = msg_text.split("hater:")[1].strip().lstrip("@")
        if new_hater in SUPERADMINS:
            cl.direct_send("🚫 You can't set a superadmin as hater!", thread_ids=[thread_id])
            return
        hater_username = new_hater
        cl.direct_send(f"😈 Hater updated to @{hater_username}", thread_ids=[thread_id])
        return

    if msg_text.startswith("admin:") and sender_username in ADMIN_USERS:
        new_admin = msg_text.split("admin:")[1].strip().lstrip("@")
        ADMIN_USERS.add(new_admin)
        cl.direct_send(f"👑 @{new_admin} is now an admin!", thread_ids=[thread_id])
        return

    if msg_text.startswith("deadmin:") and sender_username in SUPERADMINS:
        to_remove = msg_text.split("deadmin:")[1].strip().lstrip("@")
        if to_remove in ADMIN_USERS:
            ADMIN_USERS.discard(to_remove)
            cl.direct_send(f"🚫 Removed @{to_remove} from admin list.", thread_ids=[thread_id])
        return

    if msg_text == "status" and sender_username in ADMIN_USERS:
        recent = "\n".join(reply_log[-10:]) or "No recent replies yet."
        cl.direct_send(f"📊 Last 10 replies:\n{recent}", thread_ids=[thread_id])
        return

    if "my bot" in msg_text and sender_username != "phewphewwiww":
        cl.direct_send("🤖 You're just admin... My godfather is @phewphewwiww 👑", thread_ids=[thread_id])
        return

    if thread_id in PAUSED_GCS or BOT_DESTROYED:
        return

    if current_mode == "pokkie":
        if thread_id not in WELCOME_TRACKER:
            WELCOME_TRACKER[thread_id] = set()
        if sender_id not in WELCOME_TRACKER[thread_id]:
            WELCOME_TRACKER[thread_id].add(sender_id)
            cl.direct_send(f"🧁 Welcome @{sender_username}!", thread_ids=[thread_id])
        return

    if msg_text == "game:guess" and sender_username in ADMIN_USERS:
        number = random.randint(1, 10)
        game_states[thread_id] = {"type": "guess", "answer": number}
        cl.direct_send("🎯 I'm thinking of a number between 1 and 10.", thread_ids=[thread_id])
        return

    if thread_id in game_states and game_states[thread_id]["type"] == "guess":
        try:
            guess = int(msg_text)
            correct = game_states[thread_id]["answer"]
            if guess == correct:
                cl.direct_send(f"✅ Correct! It was {correct} 🎉", thread_ids=[thread_id])
            else:
                cl.direct_send(f"❌ Wrong! It was {correct}", thread_ids=[thread_id])
            del game_states[thread_id]
        except ValueError:
            pass
        return

    if msg_text == "game:slot" and sender_username in ADMIN_USERS:
        roll = [random.choice(slot_emojis) for _ in range(3)]
        result = "🎰 | " + " | ".join(roll) + " |"
        if roll[0] == roll[1] == roll[2]:
            msg = "🤑 JACKPOT!"
        elif roll[0] == roll[1] or roll[1] == roll[2] or roll[0] == roll[2]:
            msg = "😏 Two matched!"
        else:
            msg = "💔 You lost!"
        cl.direct_send(f"{result}\n{msg}", thread_ids=[thread_id])
        return

    if sender_username == "phewphewwiww":
        reply = random.choice(phew_ai_replies)
    elif sender_username == "ziniesleepy":
        reply = random.choice(zinie_ai_replies)
    else:
        reply = random.choice(insult_templates).format(user=sender_username, hater=hater_username)

    cl.direct_send(reply, thread_ids=[thread_id])
    last_replied[thread_id] = latest_msg.id
    log = f"{datetime.now().strftime('%H:%M:%S')} - @{sender_username}"
    reply_log.append(log)
    print(f"✅ {log} | {reply}")

# === LOOP ===
def ultra_bot():
    print("🤖 JARVIS bot initialized...")
    while not BOT_DESTROYED:
        try:
            threads = cl.direct_threads(amount=15)
            for thread in threads:
                threading.Thread(target=handle_thread, args=(thread,), daemon=True).start()
            time.sleep(0.3)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

ultra_bot()
