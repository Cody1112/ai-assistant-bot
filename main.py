import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

WELCOME_MESSAGE = (
    "Привет! Я твой ИИ-ассистент, сочетающий в себе тёплого друга и уверенного наставника. "
    "Я помогу тебе на пути к самореализации. С чего начнём?"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — ИИ-коуч, сочетающий тёплого друга и уверенного наставника. Поддержи пользователя, помоги поверить в себя и начать путь."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.8
    )
    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()