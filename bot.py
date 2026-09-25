#━━━━━━━━━━━━━━━━━━━
# MADE BY FF MAX LIKE BOT OB55
# PROJECTS KABIR
# MY USER : @loardvishu
#━━━━━━━━━━━━━━━━━━━
import json
import asyncio
import os
import logging
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest

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

# 🎯 SCANNER IMAGE FILE ID (High Quality Resolution)
QR_FILE_ID = "AgACAgUAAxkBAAEvHcJqtV3Sk6iT7xINNLJCR5UpebinkAACtxJrG3-dsFWi7geOJ6Wd0gEAAwIAA3kAAz0E"

REGIONS_LIST = [
    "IND", "BR", "SG", "RU", "ID", "TW",
    "US", "VN", "TH", "ME", "PK", "CIS", "BD"
]

INR_PLANS = {
    "plan_1": {"name": "1 Day (25 Likes)", "price": 1, "likes": "25", "days": 1},
    "plan_2": {"name": "1 Day (50 Likes)", "price": 2, "likes": "50", "days": 1},
    "plan_3": {"name": "1 Day (75 Likes)", "price": 3, "likes": "75", "days": 1},
    "plan_4": {"name": "1 Day (100 Likes)", "price": 4, "likes": "100", "days": 1},
    "plan_5": {"name": "1 Day (125 Likes)", "price": 5, "likes": "125", "days": 1},
    "plan_6": {"name": "1 Day (150 Likes)", "price": 6, "likes": "150", "days": 1},
    "plan_7": {"name": "1 Day (180 Likes)", "price": 7, "likes": "180", "days": 1},
    "plan_8": {"name": "1 Day (200-220 Likes)", "price": 8, "likes": "200-220", "days": 1},
    "plan_bulk_7": {"name": "7 Days (200+ Likes/Day)", "price": 45, "likes": "200+", "days": 7},
    "plan_bulk_15": {"name": "15 Days (200+ Likes/Day)", "price": 80, "likes": "200+", "days": 15},
    "plan_bulk_30": {"name": "30 Days (200+ Likes/Day)", "price": 140, "likes": "200+", "days": 30},
    "plan_bulk_45": {"name": "45 Days (200+ Likes/Day)", "price": 200, "likes": "200+", "days": 45},
    "plan_bulk_60": {"name": "60 Days (200+ Likes/Day)", "price": 250, "likes": "200+", "days": 60},
    "plan_bulk_90": {"name": "90 Days (200+ Likes/Day)", "price": 380, "likes": "200+", "days": 90},
    "plan_bulk_120": {"name": "120 Days (200+ Likes/Day)", "price": 500, "likes": "200+", "days": 120},
}

# ================= ⌨️ KEYBOARD MENUS =================

def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("❤️ GET LIKES"), KeyboardButton("🔥 AUTOLIKE")],
        [KeyboardButton("💳 BALANCE / PLANS"), KeyboardButton("👤 OWNER")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_payment_method_keyboard():
    keyboard = [
        [KeyboardButton("💳 UPI"), KeyboardButton("⭐ TG STARS")],
        [KeyboardButton("🔙 Main Menu")]
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
        [InlineKeyboardButton("1 Day - 25 Likes (₹1)", callback_data="plan_1")],
        [InlineKeyboardButton("1 Day - 50 Likes (₹2)", callback_data="plan_2")],
        [InlineKeyboardButton("1 Day - 75 Likes (₹3)", callback_data="plan_3")],
        [InlineKeyboardButton("1 Day - 100 Likes (₹4)", callback_data="plan_4")],
        [InlineKeyboardButton("1 Day - 125 Likes (₹5)", callback_data="plan_5")],
        [InlineKeyboardButton("1 Day - 150 Likes (₹6)", callback_data="plan_6")],
        [InlineKeyboardButton("1 Day - 180 Likes (₹7)", callback_data="plan_7")],
        [InlineKeyboardButton("1 Day - 200-220 Likes (₹8)", callback_data="plan_8")],
        [InlineKeyboardButton("7 Days - 200+ Likes/Day (₹45)", callback_data="plan_bulk_7")],
        [InlineKeyboardButton("15 Days - 200+ Likes/Day (₹80)", callback_data="plan_bulk_15")],
        [InlineKeyboardButton("30 Days - 200+ Likes/Day (₹140)", callback_data="plan_bulk_30")],
        [InlineKeyboardButton("45 Days - 200+ Likes/Day (₹200)", callback_data="plan_bulk_45")],
        [InlineKeyboardButton("60 Days - 200+ Likes/Day (₹250)", callback_data="plan_bulk_60")],
        [InlineKeyboardButton("90 Days - 200+ Likes/Day (₹380)", callback_data="plan_bulk_90")],
        [InlineKeyboardButton("120 Days - 200+ Likes/Day (₹500)", callback_data="plan_bulk_120")],
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
    """ Direct Telegram File ID se Instant QR Scanner Bhejne Ke Liye """
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
        context.user_data.clear()
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
            "🥷 Get An Instant Like Boost With Just 8 ⭐ Per Request!\n\n"
            "🌐 Choose Your Region From The Keyboard Below To Continue:"
        )
        await update.message.reply_text(msg, reply_markup=get_region_keyboard(), parse_mode="Markdown")
        return

    if ("AUTOLIKE" in clean_text or "AUTOLIKE" in text) and "CREATE" not in clean_text and "MY" not in clean_text:
        context.user_data.clear()
        msg = "🪙 **AUTOLIKES PRICING & MODES!**\n\n💳 Choose your payment method to continue:"
        await update.message.reply_text(msg, reply_markup=get_payment_method_keyboard(), parse_mode="Markdown")
        return

    if "OWNER" in clean_text or "OWNER" in text:
        context.user_data.clear()
        await update.message.reply_text(f"👤 **Bot Owner:** {OWNER_USERNAME}\n👑 **Group:** {CHANNEL_1}", parse_mode="Markdown")
        return

    if text == "💳 UPI":
        context.user_data["payment_method"] = "UPI"
        await update.message.reply_text("✅ **UPI Selected.** Choose Option:", reply_markup=get_autolike_system_keyboard())
        return

    if text == "⭐ TG STARS":
        context.user_data["payment_method"] = "STARS"
        await update.message.reply_text("⭐ **Telegram Stars Selected.** Choose Option:", reply_markup=get_autolike_system_keyboard())
        return

    if text == "🛒 Create New AutoLike":
        await update.message.reply_text("📅 **Select Duration:**", reply_markup=get_duration_keyboard(), parse_mode="Markdown")
        return

    if text == "📋 My AutoLikes":
        data = load_data()
        user_uids = [x for x in data["uids"] if x.get("tg_id") == update.effective_user.id]
        if not user_uids:
            await update.message.reply_text("❌ Aapka koi active AutoLike plan nahi hai.")
        else:
            resp = "📋 **Your Active AutoLikes Orders:**\n\n"
            for u in user_uids:
                resp += f"🆔 UID: `{u['uid']}` | Region: {u['region'].upper()} | Validity: {u.get('days')} Days\n"
            await update.message.reply_text(resp, parse_mode="Markdown")
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

            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⭐ Pay 8 Stars", pay=True)]])
            await update.message.reply_invoice(
                title="⚡ Instant Likes Boost",
                description=f"Instant like boost for UID {uid} (Region: {region.upper()}).",
                payload=f"likes_{uid}_{region}",
                provider_token="",
                currency="XTR",
                prices=[LabeledPrice("8 Stars", 8)],
                reply_markup=keyboard
            )
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
            payment_method = context.user_data.get("payment_method", "UPI")
            
            context.user_data.clear()

            if payment_method == "STARS":
                keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⭐ Pay Stars", pay=True)]])
                await update.message.reply_invoice(
                    title=f"🔥 {plan['days']} Days AutoLike",
                    description=f"AutoLikes for UID {uid} ({region}).",
                    payload=f"autolike_{uid}_{region}_{plan['days']}",
                    provider_token="",
                    currency="XTR",
                    prices=[LabeledPrice(f"{plan['days']} Days Plan", plan['price'])],
                    reply_markup=keyboard
                )
            else:
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

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Payment Successful! Likes process starts now.")

# ================= 🚀 MAIN FUNCTION =================

def main():
    print("⏳ Starting Telegram Bot...")
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
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))

    print("🤖 Bot is successfully running and listening!")
    app.run_polling()

if __name__ == "__main__":
    main()
