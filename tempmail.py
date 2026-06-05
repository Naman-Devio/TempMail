#before you copy this make sure to give credit by star or fork this will help us for build more things for you ©️ NAMAN-DEVIO //

import json
import urllib.request
import time
import ssl
import random

# ==========================================
# CONFIGURATION
# ==========================================
# REPLACE THIS WITH YOUR BOT TOKEN
BOT_TOKEN = "PLACE YOUR BOT TOKEN HERE"
# REPLACE THIS WITH YOUR NUMERIC TELEGRAM ID
OWNER_ID = 8557551725 
OWNER_USERNAME = "@wdymsexy"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# Your custom image URLs
CUSTOM_IMAGES = [
    "https://i.ibb.co/S4WD0VPJ/8b2f8d58b147.jpg",
    "https://i.ibb.co/qLT8TSxh/182850b926c8.jpg",
    "https://i.ibb.co/x06PCz4/ebc69aa08a94.jpg",
    "https://i.ibb.co/Zz6BPg4d/b6f1b70e190e.jpg",
    "https://i.ibb.co/Rp0kZzG4/5357361f0150.jpg"
]

# Stores email info and tracks known users
# Structure: { chat_id: { "email": "...", "token": "..." } }
user_data = {}

# Create an SSL context to avoid connection errors
ssl_context = ssl.create_default_context()

def get_random_image():
    """Returns a random image from the custom images list"""
    return random.choice(CUSTOM_IMAGES)

def send_message(chat_id, text, reply_markup=None):
    url = API_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)

    try:
        with urllib.request.urlopen(req, context=ssl_context) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        print(f"[✗] HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"[✗] Unexpected error: {e}")
    return None

def send_photo(chat_id, photo_url, caption=None, reply_markup=None):
    """Sends a photo to the chat."""
    url = API_URL + "sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url
    }
    if caption:
        payload["caption"] = caption
        payload["parse_mode"] = "Markdown"
    
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)

    try:
        with urllib.request.urlopen(req, context=ssl_context) as res:
            return json.loads(res.read())
    except Exception as e:
        print(f"[✗] Photo send error: {e}")
        return None

def get_updates(offset=None):
    url = API_URL + "getUpdates"
    if offset:
        url += f"?offset={offset}"
    try:
        with urllib.request.urlopen(url, context=ssl_context) as res:
            return json.loads(res.read())
    except Exception as e:
        print(f"[✗] Update fetch error: {e}")
        return {}

def notify_owner_new_user(message):
    """Sends user details to the owner if it's a new interaction."""
    chat_id = message["chat"]["id"]
    
    if chat_id not in user_data:
        user_info = message.get("from", message["chat"]) 
        
        first_name = user_info.get("first_name", "Unknown")
        last_name = user_info.get("last_name", "")
        full_name = f"{first_name} {last_name}".strip()
        user_id = user_info.get("id", "Unknown")
        username = user_info.get("username", "No username")
        
        msg = (
            f"🔔 *𝗡𝗲𝘄 𝗨𝘀𝗲𝗿 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗕𝗼𝘁*\n\n"
            f"👤 *𝗡𝗮𝗺𝗲:* `{full_name}`\n"
            f"🆔 *𝗨𝘀𝗲𝗿 𝗜𝗗:* `{user_id}`\n"
            f"💬 *𝗖𝗵𝗮𝘁 𝗜𝗗:* `{chat_id}`\n"
            f"🔗 *𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:* @{username}"
        )
        send_message(OWNER_ID, msg)
        user_data[chat_id] = {} 

def get_main_keyboard():
    """Returns the main reply keyboard with bold button names"""
    keyboard = {
        "keyboard": [
            [{"text": "📧 𝗡𝗲𝘄 𝗘𝗺𝗮𝗶𝗹"}, {"text": "📥 𝗜𝗻𝗯𝗼𝘅 𝗖𝗵𝗲𝗰𝗸"}],
            [{"text": "📬 𝗠𝘆 𝗜𝗻𝗯𝗼𝘅"}, {"text": "🗑 𝗗𝗲𝗹𝗲𝘁𝗲 𝗘𝗺𝗮𝗶𝗹"}],
            [{"text": "📊 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀"}, {"text": "❓ 𝗛𝗲𝗹𝗽"}],
            [{"text": "🏠 𝗠𝗮𝗶𝗻 𝗠𝗲𝗻𝘂"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    return keyboard

def handle_command(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user_info = message.get("from", {})
    
    first_name = user_info.get("first_name", "User")
    last_name = user_info.get("last_name", "")
    full_name = f"{first_name} {last_name}".strip()
    user_id = user_info.get("id", "Unknown")
    username = user_info.get("username", "EXU")

    notify_owner_new_user(message)

    if text == "/start":
        # New welcome message style
        welcome_text = (
            f"╔═══《 🎉 𝐓𝐄𝐌𝐏 𝐌𝐚𝐢𝐥! 》═══╗\n"
            f"👤 𝐔𝐬𝐞𝐫: {full_name[:20]}\n"
            f"🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
            f"🌟 𝐒𝐭𝐚𝐭𝐮𝐬: 𝐕𝐚𝐥𝐮𝐞𝐝 𝐔𝐬𝐞𝐫\n"
            f"╰═══════《 🤖 》═══════╝\n"
            f"𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐓𝐄𝐌𝐏 𝐌𝐀𝐈𝐋 𝐁𝐘 𝐃𝐑𝐀𝐆𝐎𝐍 !!\n"
            f"📌 𝐀𝐛𝐨𝐮𝐭 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭:\n"
            f"• 🔐 𝐒𝐞𝐜𝐮𝐫𝐞 𝐌𝐚𝐢𝐥 𝐒𝐭𝐨𝐫𝐚𝐠𝐞\n"
            f"• 📥 𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐌𝐚𝐢𝐥 𝐑𝐞𝐜𝐞𝐢𝐯𝐞\n"
            f"• 🔗 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐌𝐚𝐢𝐥 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧\n"
            f"• 📊 𝐑𝐞𝐚𝐥-𝐭𝐢𝐦𝐞 𝐈𝐧𝐛𝐨𝐱 𝐔𝐩𝐝𝐚𝐭𝐞𝐬\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝!\n"
            f"𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐣𝐨𝐢𝐧𝐞𝐝.\n"
            f"📌 𝐐𝐮𝐢𝐜𝐤 𝐆𝐮𝐢𝐝𝐞:\n"
            f"• 𝐔𝐬𝐞 𝐦𝐞𝐧𝐮 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐭𝐨 𝐧𝐚𝐯𝐢𝐠𝐚𝐭𝐞\n"
            f"• /𝐡𝐞𝐥𝐩 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧\n"
            f"• 📧 𝐌𝐲 𝐈𝐧𝐛𝐨𝐱 𝐭𝐨 𝐯𝐢𝐞𝐰 𝐫𝐞𝐜𝐞𝐢𝐯𝐞𝐝 𝐦𝐚𝐢𝐥𝐬"
        )
        
        # Send welcome message with random image
        send_photo(chat_id, get_random_image(), caption=welcome_text, reply_markup=get_main_keyboard())
    
    elif text == "📧 𝗡𝗲𝘄 𝗘𝗺𝗮𝗶𝗹":
        email, token = create_email()
        if email:
            user_data[chat_id] = {"email": email, "token": token}
            
            caption = (
                f"✅ *𝗘𝗺𝗮𝗶𝗹 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!*\n\n"
                f"📧 *𝗬𝗼𝘂𝗿 𝗘𝗺𝗮𝗶𝗹 𝗔𝗱𝗱𝗿𝗲𝘀𝘀:*\n`{email}`\n\n"
                f"📌 *𝗛𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲:*\n"
                f"• 𝗨𝘀𝗲 𝘁𝗵𝗶𝘀 𝗲𝗺𝗮𝗶𝗹 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗼𝗻 𝘄𝗲𝗯𝘀𝗶𝘁𝗲𝘀\n"
                f"• 𝗖𝗵𝗲𝗰𝗸 𝘆𝗼𝘂𝗿 𝗶𝗻𝗯𝗼𝘅 𝗳𝗼𝗿 𝘃𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗰𝗼𝗱𝗲𝘀\n"
                f"• 𝗘𝗺𝗮𝗶𝗹 𝗮𝘂𝘁𝗼-𝗱𝗲𝗹𝗲𝘁𝗲𝘀 𝗮𝗳𝘁𝗲𝗿 𝘀𝗼𝗺𝗲 𝘁𝗶𝗺𝗲"
            )
            send_photo(chat_id, get_random_image(), caption=caption, reply_markup=get_main_keyboard())
        else:
            send_message(chat_id, "❌ *𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗲𝗺𝗮𝗶𝗹. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻.*", reply_markup=get_main_keyboard())
    
    elif text == "📥 𝗜𝗻𝗯𝗼𝘅 𝗖𝗵𝗲𝗰𝗸":
        user = user_data.get(chat_id)
        if not user or "email" not in user:
            send_message(chat_id, "❌ *𝗬𝗼𝘂 𝗺𝘂𝘀𝘁 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗮𝗻 𝗲𝗺𝗮𝗶𝗹 𝗳𝗶𝗿𝘀𝘁!*\n𝗖𝗹𝗶𝗰𝗸 '📧 𝗡𝗲𝘄 𝗘𝗺𝗮𝗶𝗹' 𝘁𝗼 𝗰𝗿𝗲𝗮𝘁𝗲 𝗼𝗻𝗲.", reply_markup=get_main_keyboard())
        else:
            current_email = user["email"]
            status_msg = f"⏳ *𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗶𝗻𝗯𝗼𝘅 𝗳𝗼𝗿:*\n`{current_email}`"
            send_photo(chat_id, get_random_image(), caption=status_msg, reply_markup=get_main_keyboard())
            
            inbox = get_inbox(current_email)
            if inbox:
                recent_msgs = inbox[:5] 
                for msg in recent_msgs:
                    sender = msg.get("from", {}).get("address", "Unknown")
                    subject = msg.get("subject", "No Subject")
                    body = msg.get("body_text", "") or msg.get("text", "[No Content]")
                    
                    message_text = (
                        f"📨 *𝗡𝗲𝘄 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗥𝗲𝗰𝗲𝗶𝘃𝗲𝗱*\n"
                        f"👤 *𝗙𝗿𝗼𝗺:* {sender}\n"
                        f"📌 *𝗦𝘂𝗯𝗷𝗲𝗰𝘁:* {subject}\n"
                        f"💬 *𝗖𝗼𝗻𝘁𝗲𝗻𝘁:*\n{str(body)[:1000]}"
                    )
                    send_message(chat_id, message_text)
                
                if len(inbox) > 5:
                    send_message(chat_id, f"ℹ️ *𝗦𝗵𝗼𝘄𝗶𝗻𝗴 𝗹𝗮𝘀𝘁 𝟱 𝗼𝗳 {len(inbox)} 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀.*", reply_markup=get_main_keyboard())
                else:
                    send_message(chat_id, "✅ *𝗜𝗻𝗯𝗼𝘅 𝗰𝗵𝗲𝗰𝗸 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.*", reply_markup=get_main_keyboard())
            else:
                send_message(chat_id, "📭 *𝗬𝗼𝘂𝗿 𝗶𝗻𝗯𝗼𝘅 𝗶𝘀 𝗲𝗺𝗽𝘁𝘆. 𝗡𝗼 𝗻𝗲𝘄 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝗿𝗲𝗰𝗲𝗶𝘃𝗲𝗱.*", reply_markup=get_main_keyboard())
    
    elif text == "📬 𝗠𝘆 𝗜𝗻𝗯𝗼𝘅":
        user = user_data.get(chat_id)
        if not user or "email" not in user:
            send_photo(chat_id, get_random_image(), caption="❌ *𝗡𝗼 𝗮𝗰𝘁𝗶𝘃𝗲 𝗲𝗺𝗮𝗶𝗹 𝗳𝗼𝘂𝗻𝗱!*\n\n𝗖𝗹𝗶𝗰𝗸 '📧 𝗡𝗲𝘄 𝗘𝗺𝗮𝗶𝗹' 𝘁𝗼 𝗰𝗿𝗲𝗮𝘁𝗲 𝗼𝗻𝗲 𝗳𝗶𝗿𝘀𝘁.", reply_markup=get_main_keyboard())
        else:
            caption = (
                f"📬 *𝗠𝘆 𝗜𝗻𝗯𝗼𝘅*\n\n"
                f"📧 *𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗘𝗺𝗮𝗶𝗹:*\n`{user['email']}`\n\n"
                f"🔄 𝗖𝗹𝗶𝗰𝗸 '📥 𝗜𝗻𝗯𝗼𝘅 𝗖𝗵𝗲𝗰𝗸' 𝘁𝗼 𝗿𝗲𝗳𝗿𝗲𝘀𝗵 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀"
            )
            send_photo(chat_id, get_random_image(), caption=caption, reply_markup=get_main_keyboard())
            
            # Also check inbox automatically
            inbox = get_inbox(user["email"])
            if inbox:
                recent_msgs = inbox[:5] 
                for msg in recent_msgs:
                    sender = msg.get("from", {}).get("address", "Unknown")
                    subject = msg.get("subject", "No Subject")
                    body = msg.get("body_text", "") or msg.get("text", "[No Content]")
                    
                    message_text = (
                        f"📨 *𝗡𝗲𝘄 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗥𝗲𝗰𝗲𝗶𝘃𝗲𝗱*\n"
                        f"👤 *𝗙𝗿𝗼𝗺:* {sender}\n"
                        f"📌 *𝗦𝘂𝗯𝗷𝗲𝗰𝘁:* {subject}\n"
                        f"💬 *𝗖𝗼𝗻𝘁𝗲𝗻𝘁:*\n{str(body)[:1000]}"
                    )
                    send_message(chat_id, message_text)
                
                if len(inbox) > 5:
                    send_message(chat_id, f"ℹ️ *𝗦𝗵𝗼𝘄𝗶𝗻𝗴 𝗹𝗮𝘀𝘁 𝟱 𝗼𝗳 {len(inbox)} 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀.*", reply_markup=get_main_keyboard())
                else:
                    send_message(chat_id, "✅ *𝗜𝗻𝗯𝗼𝘅 𝘃𝗶𝗲𝘄𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.*", reply_markup=get_main_keyboard())
            else:
                send_message(chat_id, "📭 *𝗬𝗼𝘂𝗿 𝗶𝗻𝗯𝗼𝘅 𝗶𝘀 𝗲𝗺𝗽𝘁𝘆. 𝗡𝗼 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝘆𝗲𝘁.*", reply_markup=get_main_keyboard())
    
    elif text == "🗑 𝗗𝗲𝗹𝗲𝘁𝗲 𝗘𝗺𝗮𝗶𝗹":
        if chat_id in user_data:
            deleted_email = user_data[chat_id].get("email", "No email")
            user_data[chat_id] = {}
            
            caption = (
                f"🗑 *𝗘𝗺𝗮𝗶𝗹 𝗗𝗲𝗹𝗲𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!*\n\n"
                f"📧 𝗗𝗲𝗹𝗲𝘁𝗲𝗱 𝗘𝗺𝗮𝗶𝗹:\n`{deleted_email}`\n\n"
                f"🔄 𝗖𝗹𝗶𝗰𝗸 '📧 𝗡𝗲𝘄 𝗘𝗺𝗮𝗶𝗹' 𝘁𝗼 𝗰𝗿𝗲𝗮𝘁𝗲 𝗮 𝗻𝗲𝘄 𝗼𝗻𝗲"
            )
            send_photo(chat_id, get_random_image(), caption=caption, reply_markup=get_main_keyboard())
        else:
            send_photo(chat_id, get_random_image(), caption="❌ *𝗡𝗼 𝗮𝗰𝘁𝗶𝘃𝗲 𝗲𝗺𝗮𝗶𝗹 𝘁𝗼 𝗱𝗲𝗹𝗲𝘁𝗲.*\n\n𝗖𝗿𝗲𝗮𝘁𝗲 𝗼𝗻𝗲 𝗳𝗶𝗿𝘀𝘁!", reply_markup=get_main_keyboard())
    
    elif text == "📊 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀":
        total_users = len(user_data)
        active_emails = sum(1 for u in user_data.values() if u.get("email"))
        
        caption = (
            f"📊 *𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀*\n\n"
            f"👥 *𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿𝘀:* {total_users}\n"
            f"📧 *𝗔𝗰𝘁𝗶𝘃𝗲 𝗘𝗺𝗮𝗶𝗹𝘀:* {active_emails}\n"
            f"🟢 *𝗦𝘁𝗮𝘁𝘂𝘀:* 𝗢𝗽𝗲𝗿𝗮𝘁𝗶𝗼𝗻𝗮𝗹\n\n"
            f"🤖 *𝗕𝗼𝘁 𝗜𝗻𝗳𝗼:*\n"
            f"• 𝗨𝗽𝘁𝗶𝗺𝗲: 𝟮𝟰/𝟳\n"
            f"• 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 𝗧𝗶𝗺𝗲: <𝟭𝘀\n"
            f"• 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆: 𝗘𝗻𝗰𝗿𝘆𝗽𝘁𝗲𝗱"
        )
        send_photo(chat_id, get_random_image(), caption=caption, reply_markup=get_main_keyboard())
    
    elif text == "❓ 𝗛𝗲𝗹𝗽":
        help_text = (
            f"❓ *𝗛𝗲𝗹𝗽 & 𝗚𝘂𝗶𝗱𝗲*\n\n"
            f"📌 *𝗛𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁:*\n\n"
            f"1️⃣ 𝗖𝗹𝗶𝗰𝗸 '📧 𝗡𝗲𝘄 𝗘𝗺𝗮𝗶𝗹' 𝘁𝗼 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗮𝗻 𝗲𝗺𝗮𝗶𝗹\n"
            f"2️⃣ 𝗨𝘀𝗲 𝘁𝗵𝗲 𝗲𝗺𝗮𝗶𝗹 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗼𝗻 𝘄𝗲𝗯𝘀𝗶𝘁𝗲𝘀\n"
            f"3️⃣ 𝗖𝗹𝗶𝗰𝗸 '📥 𝗜𝗻𝗯𝗼𝘅 𝗖𝗵𝗲𝗰𝗸' 𝘁𝗼 𝘃𝗶𝗲𝘄 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀\n"
            f"4️⃣ 𝗖𝗹𝗶𝗰𝗸 '📬 𝗠𝘆 𝗜𝗻𝗯𝗼𝘅' 𝘁𝗼 𝘀𝗲𝗲 𝗮𝗹𝗹 𝗲𝗺𝗮𝗶𝗹𝘀\n\n"
            f"⚠️ *𝗡𝗼𝘁𝗲:*\n"
            f"• 𝗘𝗺𝗮𝗶𝗹𝘀 𝗮𝗿𝗲 𝘁𝗲𝗺𝗽𝗼𝗿𝗮𝗿𝘆 𝗮𝗻𝗱 𝘄𝗶𝗹𝗹 𝗲𝘅𝗽𝗶𝗿𝗲\n"
            f"• 𝗠𝗮𝘅𝗶𝗺𝘂𝗺 𝟭 𝗮𝗰𝘁𝗶𝘃𝗲 𝗲𝗺𝗮𝗶𝗹 𝗮𝘁 𝗮 𝘁𝗶𝗺𝗲\n"
            f"• 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗼𝘄𝗻𝗲𝗿 𝗳𝗼𝗿 𝗶𝘀𝘀𝘂𝗲𝘀\n\n"
            f"👤 *𝗢𝘄𝗻𝗲𝗿:* {OWNER_USERNAME}"
        )
        send_photo(chat_id, get_random_image(), caption=help_text, reply_markup=get_main_keyboard())
    
    elif text == "🏠 𝗠𝗮𝗶𝗻 𝗠𝗲𝗻𝘂":
        # Send welcome message again
        welcome_text = (
            f"╔═══《 🎉 𝐓𝐄𝐌𝐏 𝐌𝐚𝐈𝐋 》═══╗\n"
            f"👤 𝐔𝐬𝐞𝐫: {full_name[:20]}\n"
            f"🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
            f"🌟 𝐒𝐭𝐚𝐭𝐮𝐬: 𝐕𝐚𝐥𝐮𝐞𝐝 𝐔𝐬𝐞𝐫\n"
            f"╰═══════《 🤖 》═══════╝\n"
            f"𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐎𝐔𝐑 𝐓𝐄𝐌𝐏 𝐌𝐀𝐈𝐋 𝐁𝐘 𝐃𝐑𝐀𝐆𝐎𝐍 !!\n"
            f"📌 𝐀𝐛𝐨𝐮𝐭 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭:\n"
            f"• 🔐 𝐒𝐞𝐜𝐮𝐫𝐞 𝐌𝐚𝐢𝐥 𝐒𝐭𝐨𝐫𝐚𝐠𝐞\n"
            f"• 📥 𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐌𝐚𝐢𝐥 𝐑𝐞𝐜𝐞𝐢𝐯𝐞\n"
            f"• 🔗 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐌𝐚𝐢𝐥 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧\n"
            f"• 📊 𝐑𝐞𝐚𝐥-𝐭𝐢𝐦𝐞 𝐈𝐧𝐛𝐨𝐱 𝐔𝐩𝐝𝐚𝐭𝐞𝐬\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝!\n"
            f"📌 𝐐𝐮𝐢𝐜𝐤 𝐆𝐮𝐢𝐝𝐞:\n"
            f"• 𝐔𝐬𝐞 𝐦𝐞𝐧𝐮 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐭𝐨 𝐧𝐚𝐯𝐢𝐠𝐚𝐭𝐞\n"
            f"• /𝐡𝐞𝐥𝐩 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧\n"
            f"• 📧 𝐌𝐲 𝐈𝐧𝐛𝐨𝐱 𝐭𝐨 𝐯𝐢𝐞𝐰 𝐫𝐞𝐜𝐞𝐢𝐯𝐞𝐝 𝐦𝐚𝐢𝐥𝐬"
        )
        send_photo(chat_id, get_random_image(), caption=welcome_text, reply_markup=get_main_keyboard())
    
    elif text == "/help":
        help_text = (
            f"❓ *𝗛𝗲𝗹𝗽 & 𝗚𝘂𝗶𝗱𝗲*\n\n"
            f"📌 *𝗛𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁:*\n\n"
            f"1️⃣ 𝗖𝗹𝗶𝗰𝗸 '📧 𝗡𝗲𝘄 𝗘𝗺𝗮𝗶𝗹' 𝘁𝗼 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗮𝗻 𝗲𝗺𝗮𝗶𝗹\n"
            f"2️⃣ 𝗨𝘀𝗲 𝘁𝗵𝗲 𝗲𝗺𝗮𝗶𝗹 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗼𝗻 𝘄𝗲𝗯𝘀𝗶𝘁𝗲𝘀\n"
            f"3️⃣ 𝗖𝗹𝗶𝗰𝗸 '📥 𝗜𝗻𝗯𝗼𝘅 𝗖𝗵𝗲𝗰𝗸' 𝘁𝗼 𝘃𝗶𝗲𝘄 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀\n"
            f"4️⃣ 𝗖𝗹𝗶𝗰𝗸 '📬 𝗠𝘆 𝗜𝗻𝗯𝗼𝘅' 𝘁𝗼 𝘀𝗲𝗲 𝗮𝗹𝗹 𝗲𝗺𝗮𝗶𝗹𝘀\n\n"
            f"⚠️ *𝗡𝗼𝘁𝗲:*\n"
            f"• 𝗘𝗺𝗮𝗶𝗹𝘀 𝗮𝗿𝗲 𝘁𝗲𝗺𝗽𝗼𝗿𝗮𝗿𝘆 𝗮𝗻𝗱 𝘄𝗶𝗹𝗹 𝗲𝘅𝗽𝗶𝗿𝗲\n"
            f"• 𝗠𝗮𝘅𝗶𝗺𝘂𝗺 𝟭 𝗮𝗰𝘁𝗶𝘃𝗲 𝗲𝗺𝗮𝗶𝗹 𝗮𝘁 𝗮 𝘁𝗶𝗺𝗲\n"
            f"• 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗼𝘄𝗻𝗲𝗿 𝗳𝗼𝗿 𝗶𝘀𝘀𝘂𝗲𝘀\n\n"
            f"👤 *𝗢𝘄𝗻𝗲𝗿:* {OWNER_USERNAME}"
        )
        send_photo(chat_id, get_random_image(), caption=help_text, reply_markup=get_main_keyboard())
    
    elif text.startswith("/broadcast") and chat_id == OWNER_ID:
        try:
            broadcast_text = text.split(" ", 1)[1]
            count = 0
            for uid in user_data:
                send_photo(uid, get_random_image(), caption=f"📢 *𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗳𝗿𝗼𝗺 {OWNER_USERNAME}:*\n\n{broadcast_text}")
                count += 1
                time.sleep(0.5)
            send_message(chat_id, f"✅ *𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝘀𝗲𝗻𝘁 𝘁𝗼 {count} 𝘂𝘀𝗲𝗿𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.*", reply_markup=get_main_keyboard())
        except IndexError:
            send_message(chat_id, "❌ *𝗨𝘀𝗮𝗴𝗲: /broadcast <𝘆𝗼𝘂𝗿 𝗺𝗲𝘀𝘀𝗮𝗴𝗲>*", reply_markup=get_main_keyboard())

def handle_callback(callback):
    # This function is kept but won't be used with keyboard buttons
    pass

def create_email():
    url = "https://api.internal.temp-mail.io/api/v3/email/new"
    data = json.dumps({
        "min_name_length": 10,
        "max_name_length": 10
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ssl_context) as res:
            r = json.loads(res.read())
            return r["email"], r["token"]
    except Exception as e:
        print("[✗] Email create error:", e)
        return None, None

def get_inbox(email):
    url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
    headers = {
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ssl_context) as res:
            return json.loads(res.read())
    except Exception as e:
        return []

def main():
    last_update_id = None
    print(f"🤖 Bot is running... Owner: {OWNER_USERNAME}")
    while True:
        updates = get_updates(last_update_id)
        for update in updates.get("result", []):
            last_update_id = update["update_id"] + 1
            if "message" in update:
                handle_command(update["message"])
            elif "callback_query" in update:
                handle_callback(update["callback_query"])
        time.sleep(1)

if __name__ == "__main__":
    main()
