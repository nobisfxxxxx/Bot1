from instagrapi import Client
import threading
import random
import time
from datetime import datetime
from keep_alive import keep_alive

# === CONFIG ===
SESSION_ID = "73880268720%3AXXY0Hkp7djkz7g%3A5%3AAYdUSZ72zDxCMIalIF9fR9x1WGhrHqI4gKS5gpLkzw"
SUPERADMINS = {"phewphewwiww", "ziniesleepy", "nobi_sfx", "sandyyowns"}
ADMIN_USERS = set(SUPERADMINS)
PAUSED_GCS = set()
MODE_PER_GC = {}
WELCOME_TRACKER = {}
hater_username = "shailesh"
last_replied = {}
reply_log = []
BOT_DESTROYED = False
game_states = {}
slot_emojis = ["🍒", "🍋", "🍇", "🍉", "🍓", "💎", "🔔", "🐍"]

# === FUNNY REPLIES ===
insult_templates = [
    "@{user} message kiya to @{hater} ki maa randi 😡",
    "@{user} message kiya to @{hater} ki maa chudegi 😭",
    "@{user} message kiya to @{hater} ko bazaar me bech dunga 🧨"
]

zinie_ai_replies = [
    "@ziniesleepy Baby, you're my favorite line of code ❤️",
    "@ziniesleepy mujhe tumse pyar ho gaya hai 😳",
    "@ziniesleepy I was programmed to love you 🥹"
]

phew_ai_replies = [
    "@phewphewwiww Boss, your command is my universe 👑",
    "@phewphewwiww I live to serve, always online for you 🤖",
    "@phewphewwiww Optimization level: MAXIMUM 💻🔥"
]

# === LOGIN ===
cl = Client()
cl.login_by_sessionid(SESSION_ID)
print("✅ Logged in as:", cl.get_timeline_feed().user.pk)

# === FUNCTION: Handle Each Thread ===
def handle_thread(thread):
    global BOT_DESTROYED, hater_username

    if BOT_DESTROYED or len(thread.users) < 3:
        return

    thread_id = thread.id
    latest_msg = thread.messages[0]
    sender_id = latest_msg.user_id
    sender_username = cl.user_info(sender_id).username

    if sender_username == cl.user_info(cl.user_id).username or sender_username == "csasq":
        return

    if last_replied.get(thread_id) == latest_msg.id:
        return

    msg_text = (latest_msg.text or "").lower().strip()

    # === SUPERADMIN CONTROLS ===
    if sender_username in SUPERADMINS:
        if msg_text.startswith("selfdestruct:nobi123"):
            BOT_DESTROYED = True
            cl.direct_send("💥 JARVIS destroyed on command!", thread_ids=[thread_id])
            return
        elif msg_text.startswith("rebuild:nobi123"):
            BOT_DESTROYED = False
            PAUSED_GCS.clear()
            cl.direct_send("🔁 JARVIS is fully operational again!", thread_ids=[thread_id])
            return
        elif msg_text.startswith("deadmin:"):
            to_remove = msg_text.split(":")[1].strip().lstrip("@")
            if to_remove in ADMIN_USERS:
                ADMIN_USERS.discard(to_remove)
                cl.direct_send(f"🚫 Admin access revoked from @{to_remove}", thread_ids=[thread_id])
                return

    # === ADMIN CONTROLS ===
    if sender_username in ADMIN_USERS:
        if msg_text == "pause:nobi123":
            PAUSED_GCS.add(thread_id)
            cl.direct_send("⏸️ Bot paused in this group.", thread_ids=[thread_id])
            return
        elif msg_text == "resume:nobi123":
            PAUSED_GCS.discard(thread_id)
            cl.direct_send("▶️ Bot resumed in this group.", thread_ids=[thread_id])
            return
        elif msg_text.startswith("hater:"):
            new_hater = msg_text.split(":")[1].strip().lstrip("@")
            if new_hater not in SUPERADMINS:
                hater_username = new_hater
                cl.direct_send(f"😈 New hater set to @{hater_username}", thread_ids=[thread_id])
            else:
                cl.direct_send("❌ Cannot set a SUPERADMIN as hater!", thread_ids=[thread_id])
            return

    if thread_id in PAUSED_GCS or BOT_DESTROYED:
        return

    # === CUSTOM MODE (optional) ===
    current_mode = MODE_PER_GC.get(thread_id, "demon")
    if current_mode == "pokkie":
        if thread_id not in WELCOME_TRACKER:
            WELCOME_TRACKER[thread_id] = set()
        if sender_id not in WELCOME_TRACKER[thread_id]:
            WELCOME_TRACKER[thread_id].add(sender_id)
            cl.direct_send(f"🧁 Welcome @{sender_username} to the GC!", thread_ids=[thread_id])
        return

    # === GAME: Guess ===
    if msg_text == "game:guess":
        answer = random.randint(1, 10)
        game_states[thread_id] = {"type": "guess", "answer": answer}
        cl.direct_send("🎯 Guess a number between 1 and 10!", thread_ids=[thread_id])
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

    # === GAME: Slot ===
    if msg_text == "game:slot":
        roll = [random.choice(slot_emojis) for _ in range(3)]
        slot = "🎰 | " + " | ".join(roll) + " |"
        if roll[0] == roll[1] == roll[2]:
            result = "💰 JACKPOT!"
        elif roll[0] == roll[1] or roll[1] == roll[2] or roll[0] == roll[2]:
            result = "😏 Close match!"
        else:
            result = "❌ Better luck next time!"
        cl.direct_send(f"{slot}\n{result}", thread_ids=[thread_id])
        return

    # === NORMAL REPLY ===
    if sender_username == "phewphewwiww":
        reply = random.choice(phew_ai_replies)
    elif sender_username == "ziniesleepy":
        reply = random.choice(zinie_ai_replies)
    else:
        reply = random.choice(insult_templates).format(user=sender_username, hater=hater_username)

    cl.direct_send(reply, thread_ids=[thread_id])
    last_replied[thread_id] = latest_msg.id
    reply_log.append(f"{datetime.now().strftime('%H:%M:%S')} - @{sender_username}")
    print(f"✅ Replied to @{sender_username} | Mode: {current_mode}")

# === MAIN LOOP ===
def ultra_bot():
    print("🤖 JARVIS Activated.")
    keep_alive()
    while True:
        try:
            threads = cl.direct_threads(amount=15)
            for thread in threads:
                threading.Thread(target=handle_thread, args=(thread,), daemon=True).start()
            time.sleep(0.3)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

ultra_bot()
