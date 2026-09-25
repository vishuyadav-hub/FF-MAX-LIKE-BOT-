# ===================================
# MADE BY FF MAX LIKE BOT OB55
# PROJECTS KABIR
# MY USER : @loardvishu
# ===================================
import json
import asyncio
import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest

# ================= 🌐 LIGHTWEIGHT KEEP-ALIVE SERVER =================
class HealthCheckHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is Alive!')

    def log_message(self, format, *args):
        return  # Clean logs

def run_keep_alive_server():
    try:
        port = int(os.environ.get('PORT', 10000))
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        server.serve_forever()
    except Exception as e:
        logger.error(f"Keep-alive server error: {e}")

# Server ko background thread mein safely start karein
Thread(target=run_keep_alive_server, daemon=True).start()

# ================= 📝 LOGGING SETUP =================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================= 👑 CONFIG =================
CHANNEL_1 = "@FFMAXLIKEGROUP"
BOT_TOKEN = "8986200151:AAGEDkYDJNqxN88-EWbSwMxAV1bT2WPysU4"
OWNER_USERNAME = "@loardvishu"
DATA_FILE = "autolike_data.json"

# File ID ki jagah Direct QR Photo Link ya valid File ID
QR_FILE_ID = "AgACAgUAAxkBAAEvHcJqtV3Sk6iT7xINNLJCR5UpebinkAACtxJrG3-dsFWi7geOJ6Wd0gEAAwIAA3kAAz0E"

REGIONS_LIST = [
    "IND", "BR", "SG", "RU", "ID", "TW",
    "US", "VN", "TH", "ME", "PK", "CIS", "BD"
]

# Updated Plans
INR_PLANS = {
    "plan_1": {"name": "1 Day (200+ Likes/Day)", "price": 8, "likes": "200+", "days": 1},
    "plan_7": {"name": "7 Days (200+ Likes/Day)", "price": 45, "likes": "200+", "days": 7},
    "plan_15": {"name": "15 Days (200+ Likes/Day)", "price": 80, "likes": "200+", "days": 15},
    "plan_30": {"name": "30 Days (200+ Likes/Day)", "price": 140, "likes": "200+", "days": 30},
    "plan_45": {"name": "45 Days (200+ Likes/Day)", "price": 200, "likes": "200+", "days": 45},
    "plan_60": {"name": "60 Days (200+ Likes/Day)", "price": 250, "likes": "200+", "days": 60},
    "plan_90": {"name": "90 Days (200+ Likes/Day)", "price": 380, "likes": "200+", "days": 90},
    "plan_120": {"name": "120 Days (200+ Likes/Day)", "price": 500, "likes": "200+", "days": 120},
}

# ================= ⌨️ KEYBOARD MENUS =================
def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("❤️ GET LIKES"), KeyboardButton("🔥 AUTOLIKE")],
        [KeyboardButton("💳 BALANCE / PLANS"), KeyboardButton("👤 OWNER")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_autolike_system_keyboard():
    keyboard = [
        [KeyboardButton("🛒 Create New AutoLike")],
        [KeyboardButton("📋 My AutoLikes")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_duration_keyboard():
    keyboard = [
        [KeyboardButton("1 Days (₹8)"), KeyboardButton("7 Days (₹45)")],
        [KeyboardButton("15 Days (₹80)"), KeyboardButton("30 Days (₹140)")],
        [KeyboardButton("45 Days (₹200)"), KeyboardButton("60 Days (₹250)")],
        [KeyboardButton("90 Days (₹380)"), KeyboardButton("120 Days (₹500)")],
        [KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_region_keyboard():
    keyboard = [
        [KeyboardButton("IND"), KeyboardButton("BR"), KeyboardButton("SG")],
        [KeyboardButton("RU"), KeyboardButton("ID"), KeyboardButton("TW")],
        [KeyboardButton("US"), KeyboardButton("VN"), KeyboardButton("TH")],
        [KeyboardButton("ME"), KeyboardButton("PK"), KeyboardButton("CIS")],
        [KeyboardButton("BD"), KeyboardButton("🔙 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_inr_plans_keyboard():
    buttons = [
        [InlineKeyboardButton("1 Days (₹8)", callback_data="plan_1"), InlineKeyboardButton("7 Days (₹45)", callback_data="plan_7")],
        [InlineKeyboardButton("15 Days (₹80)", callback_data="plan_15"), InlineKeyboardButton("30 Days (₹140)", callback_data="plan_30")],
        [InlineKeyboardButton("45 Days (₹200)", callback_data="plan_45"), InlineKeyboardButton("60 Days (₹250)", callback_data="plan_60")],
        [InlineKeyboardButton("90 Days (₹380)", callback_data="plan_90"), InlineKeyboardButton("120 Days (₹500)", callback_data="plan_120")],
    ]
    return InlineKeyboardMarkup(buttons)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}
    data.setdefault("uids", [])
    return data

async def send_qr_photo(chat_id, caption, context, reply_markup):
    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=QR_FILE_ID,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error sending photo via File ID: {e}")
        # Agar photo send na ho paaye, toh message text ke saath zarur aayega
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ **Payment Details:**\n\n{caption}",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# ================= 📩 HANDLERS =================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 **Welcome to FF MAX LIKE BOT!**\n\nChoose an option from the menu below:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )

async def plan_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan_key = query.data
    if plan_key in INR_PLANS:
        plan = INR_PLANS[plan_key]
        user_uid = context.user_data.get("selected_uid", "Not Provided")

        text = (
            f"🛒 **PAYMENT DETAILS (INR)**\n\n"
            f"👤 **Account Name:** VISHAL KUMAR\n"
            f"📌 **Plan:** {plan['name']}\n"
            f"💰 **Amount:** ₹{plan['price']} INR\n"
            f"🎯 **Target Likes:** {plan['likes']}\n"
            f"⏳ **Validity:** {plan['days']} Day(s)\n"
            f"🆔 **Game UID:** `{user_uid}`\n\n"
            f"👉 **Steps to Activate:**\n"
            f"1. Niche diye gaye Scanner par ₹{plan['price']} Pay karein.\n"
            f"2. Screenshot Admin ko bhej dein: {OWNER_USERNAME}\n"
            f"3. Verification ke baad plan Instant Active ho jayega!"
        )

        await send_qr_photo(query.message.chat_id, text, context, get_main_menu_keyboard())

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    clean_text = text.encode('ascii', 'ignore').decode('ascii').strip().upper()

    if "MAIN MENU" in clean_text or "BACK" in clean_text or text in ["🔙 Back", "🔙 Main Menu"]:
        context.user_data.clear()
        await update.message.reply_text("🔙 Main Menu Screen:", reply_markup=get_main_menu_keyboard())
        return

    if "BALANCE" in clean_text or "PLANS" in clean_text or "BALANCE / PLANS" in text:
        context.user_data["step"] = "BALANCE_AWAITING_UID"
        await update.message.reply_text(
            "💳 **BALANCE & PLANS**\n\n"
            "🎯 Plan buy karne ke liye apna **Free Fire Game UID** enter karein:", 
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 Main Menu")]], resize_keyboard=True),
            parse_mode="Markdown"
        )
        return

    if "GET LIKES" in clean_text or "GET LIKES" in text:
        context.user_data.clear()
        context.user_data["step"] = "GET_LIKES_SELECT_REGION"
        msg = (
            "💎 **GET LIKES!**\n\n"
            "🥷 Get An Instant Like Boost With Just ₹8 INR Per Request!\n\n"
            "🌐 Choose Your Region From The Keyboard Below To Continue:"
        )
        await update.message.reply_text(msg, reply_markup=get_region_keyboard(), parse_mode="Markdown")
        return

    if ("AUTOLIKE" in clean_text or "AUTOLIKE" in text) and "CREATE" not in clean_text and "MY" not in clean_text:
        context.user_data.clear()
        msg = "🔥 **AUTOLIKE SYSTEM**\n\nChoose an option from below:"
        await update.message.reply_text(msg, reply_markup=get_autolike_system_keyboard(), parse_mode="Markdown")
        return

    if "OWNER" in clean_text or "OWNER" in text:
        context.user_data.clear()
        await update.message.reply_text(f"👤 **Bot Owner:** {OWNER_USERNAME}\n👑 **Group:** {CHANNEL_1}", parse_mode="Markdown")
        return

    if text == "🛒 Create New AutoLike":
        await update.message.reply_text("📅 **Select Duration:**", reply_markup=get_duration_keyboard(), parse_mode="Markdown")
        return

    if text == "📋 My AutoLikes":
        context.user_data["step"] = "CHECK_MY_AUTOLIKE_UID"
        await update.message.reply_text(
            "📋 **MY AUTOLIKES SEARCH**\n\n"
            "🔍 Apna AutoLike status check karne ke liye apna **Free Fire UID** enter karein:",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 Main Menu")]], resize_keyboard=True),
            parse_mode="Markdown"
        )
        return

    if any(d in text for d in ["1 Days", "7 Days", "15 Days", "30 Days", "45 Days", "60 Days", "90 Days", "120 Days"]):
        plan_matrix = {
            "1 Days": {"name": "1 Day Autolikes", "price": 8, "days": 1},
            "7 Days": {"name": "7 Days Autolikes", "price": 45, "days": 7},
            "15 Days": {"name": "15 Days Autolikes", "price": 80, "days": 15},
            "30 Days": {"name": "30 Days Autolikes", "price": 140, "days": 30},
            "45 Days": {"name": "45 Days Autolikes", "price": 200, "days": 45},
            "60 Days": {"name": "60 Days Autolikes", "price": 250, "days": 60},
            "90 Days": {"name": "90 Days Autolikes", "price": 380, "days": 90},
            "120 Days": {"name": "120 Days Autolikes", "price": 500, "days": 120},
        }
        for key in plan_matrix:
            if key in text:
                context.user_data["selected_plan"] = plan_matrix[key]
                break

        context.user_data["step"] = "AUTOLIKE_SELECT_REGION"
        await update.message.reply_text("💎 **Select Your Region:**", reply_markup=get_region_keyboard(), parse_mode="Markdown")
        return

    current_step = context.user_data.get("step")

    if current_step == "CHECK_MY_AUTOLIKE_UID":
        if text.isdigit() and len(text) >= 5:
            search_uid = text.strip()
            data = load_data()
            matched_orders = [x for x in data.get("uids", []) if str(x.get("uid")).strip() == search_uid]
            
            context.user_data.clear()
            if not matched_orders:
                await update.message.reply_text(
                    f"❌ **UID `{search_uid}` ke liye koi active AutoLike plan nahi mila.**", 
                    reply_markup=get_main_menu_keyboard(), 
                    parse_mode="Markdown"
                )
            else:
                resp = f"📋 **Active AutoLikes Status for UID `{search_uid}`:**\n\n"
                for u in matched_orders:
                    region = str(u.get("region", "N/A")).upper()
                    days = u.get("days", "N/A")
                    resp += f"🆔 UID: `{u['uid']}` | Region: {region} | Validity: {days} Days\n"
                await update.message.reply_text(resp, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Galat UID! Sahi Numeric Free Fire UID enter karein.")
        return

    if current_step == "GET_LIKES_SELECT_REGION":
        if text.upper() in REGIONS_LIST:
            context.user_data["get_likes_region"] = text.lower()
            context.user_data["step"] = "GET_LIKES_AWAITING_UID"
            await update.message.reply_text(f"🌐 Region Selected: *{text.upper()}*\n\n🆔 Please Enter Your Free Fire UID Below:", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Please select a valid region from the keyboard.")
        return

    if current_step == "GET_LIKES_AWAITING_UID":
        if text.isdigit() and len(text) >= 5:
            uid = text
            region = context.user_data.get("get_likes_region", "ind")
            context.user_data.clear()

            caption_msg = (
                f"🛍️ **Product:** Instant Likes Boost\n"
                f"❤️ **Likes Rate:** Instant Boost\n"
                f"🌐 **Region:** {region.upper()}\n"
                f"🆔 **UID:** `{uid}`\n"
                f"💰 **Amount:** ₹8 INR\n"
                f"💳 **Method:** UPI / Scanner\n\n"
                f"👉 **Steps to Activate:**\n"
                f"1. Niche diye gaye Scanner par ₹8 Pay karein.\n"
                f"2. Screenshot Admin ko bhej dein: {OWNER_USERNAME}\n"
                f"3. Verification ke baad likes Instant send ho jayenge!"
            )

            await send_qr_photo(update.effective_chat.id, caption_msg, context, get_main_menu_keyboard())
        else:
            await update.message.reply_text("❌ Galat UID! Sahi Numeric Free Fire UID enter karein.")
        return

    if current_step == "BALANCE_AWAITING_UID":
        if text.isdigit() and len(text) >= 5:
            context.user_data["selected_uid"] = text
            context.user_data["step"] = None

            await update.message.reply_text(
                f"✅ **Saved UID:** `{text}`\n\n👇 **Niche se apna Plan select karein:**",
                reply_markup=get_inr_plans_keyboard(),
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ Please enter a valid numerical Free Fire UID.")
        return

    if current_step == "AUTOLIKE_SELECT_REGION":
        if text.upper() in REGIONS_LIST:
            context.user_data["selected_region"] = text.upper()
            context.user_data["step"] = "AUTOLIKE_AWAITING_UID"
            await update.message.reply_text(f"🆔 **Region Selected: {text.upper()}**\n\nReply with your Free Fire UID.", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Select a valid region from the keyboard.")
        return

    if current_step == "AUTOLIKE_AWAITING_UID":
        if text.isdigit() and len(text) >= 5:
            uid = text
            region = context.user_data.get("selected_region", "IND")
            plan = context.user_data.get("selected_plan", {"name": "1 Day Autolikes", "price": 8, "days": 1})
            
            context.user_data.clear()

            caption_msg = (
                f"🛍️ **Product:** {plan['days']} Day Autolikes\n"
                f"❤️ **Likes Rate:** 200+ Daily Likes\n"
                f"🌐 **Region:** {region}\n"
                f"🆔 **UID:** `{uid}`\n"
                f"💰 **Amount:** ₹{plan['price']} INR\n"
                f"💳 **Method:** UPI / Scanner\n\n"
                f"📷 **Send payment screenshot to Admin:** {OWNER_USERNAME}"
            )

            await send_qr_photo(update.effective_chat.id, caption_msg, context, get_main_menu_keyboard())
        else:
            await update.message.reply_text("❌ Please enter valid numerical UID.")
        return

# ================= 🚀 MAIN FUNCTION =================
def main():
    print("⏳ Starting Telegram Bot...")
    
    # Request timeouts
    request_kwargs = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0
    )
    
    app = ApplicationBuilder().token(BOT_TOKEN).request(request_kwargs).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("menu", start_cmd))
    
    app.add_handler(CallbackQueryHandler(plan_callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))

    print("🤖 Bot is successfully running and listening!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
    
