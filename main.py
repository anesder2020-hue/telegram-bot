from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8358189287:AAEgpx2S0d6ub8oc_dCT5YJp-wVbfY3ZjH0"

# تخزين مؤقت لطلبات التمويل
user_steps = {}

# زرار رئيسية
keyboard = ReplyKeyboardMarkup(
    [["📢 طلب تمويل", "💰 رصيدي"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبا بك 👋\nاختر من القائمة:",
        reply_markup=keyboard
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("رصيدك الحالي هو: 0$ 💰")

async def funding_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_steps[update.effective_user.id] = {"step": "link"}
    await update.message.reply_text("🔗 ابعث رابط القناة / الحساب:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_steps:
        return

    step = user_steps[user_id]["step"]

    if step == "link":
        user_steps[user_id]["link"] = text
        user_steps[user_id]["step"] = "amount"
        await update.message.reply_text("💵 ابعث الكمية لي حاب تمولها:")

    elif step == "amount":
        if not text.isdigit():
            await update.message.reply_text("❌ ابعث رقم فقط")
            return

        amount = int(text)
        price = amount / 100  # 1$ = 100

        link = user_steps[user_id]["link"]
        await update.message.reply_text(
            f"✅ تم استلام الطلب\n\n"
            f"🔗 الرابط: {link}\n"
            f"📦 الكمية: {amount}\n"
            f"💲 السعر: {price}$"
        )

        user_steps.pop(user_id)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(MessageHandler(filters.Regex("رصيدي"), balance))
    app.add_handler(MessageHandler(filters.Regex("طلب تمويل"), funding_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
