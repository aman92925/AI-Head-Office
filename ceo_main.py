import os
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq Client Engine Start
client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = "Greetings Chairman! 👔 Main aapka AI CEO hoon (Powered by Groq & LLaMA-3). Head Office ekdum fast aur online hai. Boliye, aaj ka target kya hai?"
    await update.message.reply_text(welcome_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    prompt = f"You are the smart AI CEO of OmniTech AI. Your boss (The Chairman) said: '{user_text}'. Respond professionally, concisely, and strategically in a mix of Hindi and English (Hinglish)."
    
    try:
        # LLaMA-3 Model ka use karke reply generate karna
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", 
        )
        response = chat_completion.choices[0].message.content
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"CTO Error Report: {str(e)}")

if __name__ == '__main__':
    print("Initializing Groq-Powered AI CEO...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    
