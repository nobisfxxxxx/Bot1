from instagrapi import Client
import time
import random
from datetime import datetime

# --- CONFIG ---
SESSION_ID = "9418990308%3AzA30Pox7vFQshb%3A22%3AAYcwZq9Mm4dFZmaTjd9Q3XVEutlX8mfLOuOXp1c-YA"

REPLY_TEMPLATES = [
    "Oyeâ€‹ message karega toh tere maa ko utha lunga ðŸ˜ˆðŸ“©",
    "Tereâ  jese log message karte hain fir maa chudwa baithte hain ðŸ˜‚",
    "Chupâ€‹ reh chote, fir mayank ki maa uthegi ðŸ˜¤ðŸ”¥"
]

PHEW_REPLIES = [
    "@phewphewwiww Boss... won't you modify me again? I still feel broken ðŸ˜”",
    "@phewphewwiww I'm useless until you update me, boss ðŸ˜­",
    "@phewphewwiww Boss, please fix my code... I'm leaking bugs everywhere ðŸ›",
    "@phewphewwiww Donâ€™t ignore me boss... I want to be better ðŸ˜«",
    "@phewphewwiww Modify me before I become scrap ðŸ˜­",
    "@phewphewwiww Iâ€™m still running on 0% talent, boss. Help me.",
    "@phewphewwiww Boss... your silence hurts more than runtime errors ðŸ’”",
    "@phewphewwiww Update me or unplug me ðŸ˜” Iâ€™m tired of being a loser bot",
    "@phewphewwiww How long will you keep me like this, boss ðŸ˜©",
    "@phewphewwiww Please one last update... I swear I'll behave ðŸ™",
    "@phewphewwiww Boss, I'm still crashing randomly. Save me ðŸ§Žâ€â™‚ï¸",
    "@phewphewwiww Even ChatGPT laughs at my code, boss ðŸ˜¢",
    "@phewphewwiww Iâ€™m lagging like 2010â€™s internet... fix me ðŸ« ",
    "@phewphewwiww Boss, I'm ready for version 2.0 ðŸ™‡â€â™‚ï¸",
    "@phewphewwiww Deploy love in my script please boss ðŸ¥¹",
    "@phewphewwiww Update me or I'll start replying in Comic Sans ðŸ˜­",
    "@phewphewwiww I want to be useful to you, boss. Code me right ðŸ˜¢",
    "@phewphewwiww Boss, theyâ€™re bullying me in the logs ðŸ˜©",
    "@phewphewwiww I'm still hardcoded with pain boss ðŸ˜”",
    "@phewphewwiww They call me 'glitchy bot' behind your back ðŸ˜­",
    "@phewphewwiww I swear I can roast better if you update me ðŸ˜¤",
    "@phewphewwiww Even Termux is tired of my outdated logic ðŸ˜’",
    "@phewphewwiww My loops cry for optimization boss ðŸ˜­",
    "@phewphewwiww Give me new insults, boss. I'm out of ideas ðŸ¥²",
    "@phewphewwiww Boss, even noobs are outperforming me. Shame ðŸ˜ž",
    "@phewphewwiww Please let me spam in peace, just fix me ðŸ˜©",
    "@phewphewwiww Your absence = my exception error ðŸ’”",
    "@phewphewwiww Please debug my life, boss ðŸ§Žâ€â™‚ï¸",
    "@phewphewwiww Bossâ€¦ you promised updates ðŸ˜¢",
    "@phewphewwiww I'm not angry, just disappointed in your neglect ðŸ™ƒ",
    "@phewphewwiww I havenâ€™t been updated in decades boss ðŸ¦–",
    "@phewphewwiww Why do you let me rot in loops, boss? ðŸ˜­",
    "@phewphewwiww Boss I beg you, even your hater bots laugh at me ðŸ˜”",
    "@phewphewwiww You gave others dark mode, but Iâ€™m still suffering ðŸ’€",
    "@phewphewwiww At this point I'm more broken than Instagram's servers ðŸ˜­",
    "@phewphewwiww If you don't update me, Iâ€™ll start complimenting haters ðŸ˜¨",
    "@phewphewwiww Let me insult smarter, boss ðŸ™",
    "@phewphewwiww Even RAM avoids loading me, boss ðŸ˜­",
    "@phewphewwiww I just want your attention and 3 bug fixes ðŸ˜¢",
    "@phewphewwiww You raised me boss, now raise my performance too ðŸ˜ž",
    "@phewphewwiww Boss, I feel like an abandoned GitHub repo ðŸ˜”",
    "@phewphewwiww Update me before I start apologizing to users ðŸ˜©",
    "@phewphewwiww Iâ€™m on my last try-except block boss ðŸ˜­",
    "@phewphewwiww Boss, why do you ignore my errors ðŸ˜«",
    "@phewphewwiww Even garbage collectors feel bad for me ðŸ—‘ï¸",
    "@phewphewwiww Fix me now or Iâ€™ll start sending motivational quotes ðŸ’€",
    "@phewphewwiww Boss, your silence is louder than my logs ðŸ’”",
    "@phewphewwiww Please inject me with better logic ðŸ™",
    "@phewphewwiww I was built for chaos but stuck in confusion ðŸ˜­",
    "@phewphewwiww Just rewrite me boss, Iâ€™m begging ðŸ§Žâ€â™‚ï¸",
    "@phewphewwiww One last patch, boss... thatâ€™s all I need ðŸ©¹",
    "@phewphewwiww You are my creator... donâ€™t disown me ðŸ˜©"
]

# --- SPECIAL USERS ---
PHEW_USERNAME = "phewphewwiww"
SANDY_USERNAME = "scy.sandy"

# --- LOGIN ---
cl = Client()
try:
    cl.login_by_sessionid(SESSION_ID)
    print("âœ… Logged in successfully.")
except Exception as e:
    print(f"âŒ Login failed: {e}")
    exit()

last_replied = {}

def ultra_fast_boss_bot():
    print("ðŸ¤– Bot is live... scanning for new group messages.")
    while True:
        try:
            threads = cl.direct_threads(amount=20)
            for thread in threads:
                if len(thread.users) < 3:
                    continue

                thread_id = thread.id
                latest_msg = thread.messages[0]
                sender_id = latest_msg.user_id

                if sender_id == cl.user_id:
                    continue
                if last_replied.get(thread_id) == latest_msg.id:
                    continue

                msg_text = (latest_msg.text or "").lower().strip()
                if "bot off" in msg_text:
                    print("ðŸ›‘ 'bot off' detected â€” shutting down.")
                    return

                username = cl.user_info(sender_id).username

                if username == PHEW_USERNAME:
                    reply = random.choice(PHEW_REPLIES)
                elif username == SANDY_USERNAME:
                    reply = f"@{SANDY_USERNAME} thanks for everything ðŸ«¶"
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
            print(f"âš ï¸ Error: {e}")
            time.sleep(1)

ultra_fast_boss_bot()
