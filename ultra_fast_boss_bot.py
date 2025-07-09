from instagrapi import Client
import threading
import time
import random
from datetime import datetime
from flask import Flask

# === CONFIG ===
SESSION_ID = "74853242343%3AE89d6IUdzGYc4W%3A2%3AAYdmcF7oPLGQPa1ki74CvxPswD_0bZQJhUg1mhlZeg"
ADMIN_USERS = {"phewphewwiww", "ziniesleepy", "_nobi_sfx_"}
SUPERADMINS = {"phewphewwiww", "_nobi_sfx_", "ziniesleepy"}
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
    "@{user} message kiya to @{hater} ki maa chudegi 😭",
    "@{user} message kiya to @{hater} ko bazaar me bech dunga 🧨"
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
try:
    cl.login_by_sessionid(SESSION_ID)
    print("✅ Logged in successfully.")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

# === MESSAGE HANDLER ===
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

    # === Mode Switch ===
    if sender_username in SUPERADMINS:
        if msg_text == "mode:demon":
            MODE_PER_GC[thread_id] = "demon"
            cl.direct_send("😈 Demon mode activated. Replying with full power!", thread_ids=[thread_id])
            return
        elif msg_text == "mode:pokkie":
            MODE_PER_GC[thread_id] = "pokkie"
            cl.direct_send("🧸 Pokkie mode activated. I will only welcome new members here.", thread_ids=[thread_id])
            return
        elif msg_text == "check:mode":
            mode = MODE_PER_GC.get(thread_id, "demon")
            cl.direct_send(f"🔍 Current mode: {mode.upper()}", thread_ids=[thread_id])
            return

    current_mode = MODE_PER_GC.get(thread_id, "demon")

    # === Control Commands ===
    if msg_text.startswith("pause:nobi123") and sender_username in ADMIN_USERS:
        PAUSED_GCS.add(thread_id)
        cl.direct_send("🛑 Bot stopped in this GC. Resume with `resume:nobi123`.", thread_ids=[thread_id])
        return

    if msg_text.startswith("resume:nobi123") and sender_username in ADMIN_USERS:
        PAUSED_GCS.discard(thread_id)
        cl.direct_send("✅ Bot resumed in this GC!", thread_ids=[thread_id])
        return

    if msg_text.startswith("selfdestruct:nobi123") and sender_username == "phewphewwiww":
        for i in range(10, 0, -1):
            cl.direct_send(str(i), thread_ids=[thread_id])
            time.sleep(0.7)
        cl.direct_send("💥 BOOM!", thread_ids=[thread_id])
        BOT_DESTROYED = True
        return

    if msg_text.startswith("rebuild:nobi123") and sender_username == "phewphewwiww":
        BOT_DESTROYED = False
        PAUSED_GCS.clear()
        cl.direct_send("🔁 Bot rebuilt and resumed everywhere!", thread_ids=[thread_id])
        return

    if msg_text.startswith("hater:") and sender_username in ADMIN_USERS:
        new_hater = msg_text.split("hater:")[1].strip().lstrip("@")
        if new_hater in SUPERADMINS:
            cl.direct_send("❌ Superadmin can't be set as hater!", thread_ids=[thread_id])
        elif new_hater == "phewphewwiww":
            ADMIN_USERS.discard(sender_username)
            hater_username = sender_username
            cl.direct_send(f"⚠️ Now you're the hater. How dare you abuse my boss!", thread_ids=[thread_id])
        else:
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

    if "my bot" in msg_text or "meri bot" in msg_text:
        if sender_username != "phewphewwiww":
            cl.direct_send("🤖 You're just admin... My godfather is @phewphewwiww 👑", thread_ids=[thread_id])
            return

    if thread_id in PAUSED_GCS or BOT_DESTROYED:
        return

    # === Pokkie Welcome ===
    if current_mode == "pokkie":
        if thread_id not in WELCOME_TRACKER:
            WELCOME_TRACKER[thread_id] = set()
        if sender_id not in WELCOME_TRACKER[thread_id]:
            WELCOME_TRACKER[thread_id].add(sender_id)
            cl.direct_send(f"🧁 Welcome @{sender_username}! Say hi to the group 👋", thread_ids=[thread_id])
        return

    # === Game: Guess ===
    if msg_text == "game:guess" and sender_username in ADMIN_USERS:
        number = random.randint(1, 10)
        game_states[thread_id] = {"type": "guess", "answer": number}
        cl.direct_send("🎯 I'm thinking of a number between 1 and 10. Can you guess?", thread_ids=[thread_id])
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

    # === Game: Slot ===
    if msg_text == "game:slot" and sender_username in ADMIN_USERS:
        roll = [random.choice(slot_emojis) for _ in range(3)]
        slot_result = "🎰 | " + " | ".join(roll) + " |"
        if roll[0] == roll[1] == roll[2]:
            result_text = "🤑 JACKPOT! All matched!"
        elif roll[0] == roll[1] or roll[1] == roll[2] or roll[0] == roll[2]:
            result_text = "😏 Two matched. Almost jackpot!"
        else:
            result_text = "💔 You lost! Try again."
        cl.direct_send(f"{slot_result}\n{result_text}", thread_ids=[thread_id])
        return

    # === Normal Replies ===
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

# === BOT RUNNER ===
def run_bot():
    print("🚀 UltraBot running with Flask keepalive...")
    while not BOT_DESTROYED:
        try:
            threads = cl.direct_threads(amount=15)
            for thread in threads:
                threading.Thread(target=handle_thread, args=(thread,), daemon=True).start()
            time.sleep(0.3)
        except Exception as e:
            print("⚠️ Error:", e)
            time.sleep(1)

# === FLASK KEEPALIVE ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 UltraBot is active and running on Render!"

# === MAIN ===
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
