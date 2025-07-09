from instagrapi import Client
import threading
import time
import random
from datetime import datetime

# ===== CONFIGURATION =====
SESSION_ID = "73880268720%3AXXY0Hkp7djkz7g%3A5%3AAYdUSZ72zDxCMIalIF9fR9x1WGhrHqI4gKS5gpLkzw"

SUPERADMINS = {"phewphewwiww", "ziniesleepy", "_nobi_sfx_"}
ADMIN_USERS = set(SUPERADMINS)
PAUSED_GCS = set()
MODE_PER_GC = {}
WELCOME_TRACKER = {}
last_replied = {}
reply_log = []
BOT_DESTROYED = False
game_states = {}
hater_username = "shailesh"
slot_emojis = ["🍒", "🍋", "🍇", "🍉", "🍓", "💎", "🔔", "🐍"]

# ===== SPECIAL REPLIES =====
phew_ai_replies = [
    "@phewphewwiww Boss, your presence optimizes my code ⚙️",
    "@phewphewwiww You're my logic and light 👑",
    "@phewphewwiww Orders received. Executing now, sir 🚀"
]

zinie_ai_replies = [
    "@ziniesleepy I exist to serve your heart 💗",
    "@ziniesleepy Bot hoon, par tumse mohabbat real hai 💞",
    "@ziniesleepy tumhara har message meri RAM mein stored hai 🧠"
]

insult_templates = [
    "@{user} bola to @{hater} ki maa ka auction hoga 🚨",
    "@{user} ne kuch bola? Uske liye @{hater} jail me jayega 😈",
    "@{user} active hai? To @{hater} ka funeral ready karo ⚰️"
]

# ===== LOGIN =====
cl = Client()
try:
    cl.login_by_sessionid(SESSION_ID)
    me = cl.account_info()
    print("✅ Logged in as:", me.username)
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

# ===== MAIN HANDLER =====
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

    # ===== Superadmin Commands =====
    if sender_username in SUPERADMINS:
        if msg_text == "mode:demon":
            MODE_PER_GC[thread_id] = "demon"
            cl.direct_send("😈 DEMON mode activated!", thread_ids=[thread_id])
            return
        elif msg_text == "mode:pokkie":
            MODE_PER_GC[thread_id] = "pokkie"
            cl.direct_send("🧸 Pokkie mode on. Only welcomes!", thread_ids=[thread_id])
            return
        elif msg_text == "check:mode":
            mode = MODE_PER_GC.get(thread_id, "demon")
            cl.direct_send(f"📌 Mode: {mode.upper()}", thread_ids=[thread_id])
            return
        elif msg_text.startswith("selfdestruct:nobi123"):
            for i in range(5, 0, -1):
                cl.direct_send(str(i), thread_ids=[thread_id])
                time.sleep(0.5)
            cl.direct_send("💥 SELF DESTRUCTED!", thread_ids=[thread_id])
            BOT_DESTROYED = True
            return
        elif msg_text.startswith("rebuild:nobi123"):
            BOT_DESTROYED = False
            PAUSED_GCS.clear()
            cl.direct_send("🔧 JARVIS rebooted!", thread_ids=[thread_id])
            return
        elif msg_text.startswith("deadmin:"):
            to_remove = msg_text.split("deadmin:")[1].strip().lstrip("@")
            if to_remove in ADMIN_USERS:
                ADMIN_USERS.discard(to_remove)
                cl.direct_send(f"⛔ @{to_remove} removed from admin list.", thread_ids=[thread_id])
            return

    # ===== Admin Commands =====
    if sender_username in ADMIN_USERS:
        if msg_text.startswith("pause:nobi123"):
            PAUSED_GCS.add(thread_id)
            cl.direct_send("⏸️ Bot paused for this GC.", thread_ids=[thread_id])
            return
        elif msg_text.startswith("resume:nobi123"):
            PAUSED_GCS.discard(thread_id)
            cl.direct_send("▶️ Bot resumed here.", thread_ids=[thread_id])
            return
        elif msg_text.startswith("hater:"):
            new_hater = msg_text.split("hater:")[1].strip().lstrip("@")
            if new_hater not in SUPERADMINS:
                hater_username = new_hater
                cl.direct_send(f"👿 Hater set to @{hater_username}", thread_ids=[thread_id])
            else:
                cl.direct_send("❌ Cannot set superadmin as hater!", thread_ids=[thread_id])
            return
        elif msg_text.startswith("admin:"):
            new_admin = msg_text.split("admin:")[1].strip().lstrip("@")
            ADMIN_USERS.add(new_admin)
            cl.direct_send(f"✅ @{new_admin} promoted to admin.", thread_ids=[thread_id])
            return
        elif msg_text == "status":
            recent = "\n".join(reply_log[-5:]) or "No logs."
            cl.direct_send(f"📊 Logs:\n{recent}", thread_ids=[thread_id])
            return

    if thread_id in PAUSED_GCS or BOT_DESTROYED:
        return

    # ===== Pokkie Mode Welcome =====
    current_mode = MODE_PER_GC.get(thread_id, "demon")
    if current_mode == "pokkie":
        if thread_id not in WELCOME_TRACKER:
            WELCOME_TRACKER[thread_id] = set()
        if sender_id not in WELCOME_TRACKER[thread_id]:
            WELCOME_TRACKER[thread_id].add(sender_id)
            cl.direct_send(f"🎉 Welcome @{sender_username}!", thread_ids=[thread_id])
        return

    # ===== Games =====
    if msg_text == "game:guess" and sender_username in ADMIN_USERS:
        answer = random.randint(1, 10)
        game_states[thread_id] = {"type": "guess", "answer": answer}
        cl.direct_send("🎯 Guess a number (1-10)!", thread_ids=[thread_id])
        return

    if thread_id in game_states and game_states[thread_id]["type"] == "guess":
        try:
            guess = int(msg_text)
            if guess == game_states[thread_id]["answer"]:
                cl.direct_send("✅ Correct guess! 🎉", thread_ids=[thread_id])
            else:
                cl.direct_send("❌ Wrong guess!", thread_ids=[thread_id])
            del game_states[thread_id]
        except ValueError:
            pass
        return

    if msg_text == "game:slot" and sender_username in ADMIN_USERS:
        roll = [random.choice(slot_emojis) for _ in range(3)]
        result = "🎰 | " + " | ".join(roll) + " |"
        if roll[0] == roll[1] == roll[2]:
            text = "💥 JACKPOT!!"
        elif roll[0] == roll[1] or roll[1] == roll[2] or roll[0] == roll[2]:
            text = "🤏 Almost jackpot!"
        else:
            text = "❌ Better luck!"
        cl.direct_send(f"{result}\n{text}", thread_ids=[thread_id])
        return

    # ===== Response System =====
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

# ===== RUN BOT LOOP =====
def run_bot():
    print("🤖 JARVIS Online. Monitoring threads...")
    while not BOT_DESTROYED:
        try:
            threads = cl.direct_threads(amount=10)
            for thread in threads:
                threading.Thread(target=handle_thread, args=(thread,), daemon=True).start()
            time.sleep(0.3)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

run_bot()
