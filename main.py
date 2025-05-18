import os
import openai
from fastapi import FastAPI, Request
import uvicorn
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

app = FastAPI()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)
openai.api_key = os.getenv("OPENAI_API_KEY")

WELCOME_MESSAGE = (
    "Привет! Я твой ИИ-ассистент, сочетающий в себе тёплого друга и уверенного наставника. "
    "Я помогу тебе на пути к самореализации. С чего начнём?"
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — ИИ-коуч, сочетающий тёплого друга и уверенного наставника. Говори мягко, поддерживающе, но с уверенностью. Помоги пользователю начать путь к своей цели, поверить в себя."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.8
    )
    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

def setup_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

@app.on_event("startup")
async def startup_event():
    setup_bot()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)