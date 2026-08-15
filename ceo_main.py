import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# CTO AUTO-FIX: Google se khud poocho ki kaunsa model zinda hai!
active_model = 'gemini-1.5-flash' # Default Fallback
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            active_model = m.name.replace('models/', '')
            break
except Exception as e:
    print("Model list error:", e)

model = genai.GenerativeModel(active_model)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = f"Greetings Chairman! 👔 Main aapka AI CEO hoon (Powered by {active_model}). Head Office online hai. Boliye, aaj ka target kya hai?"
    await update.message.reply_text(welcome_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    prompt = f"""You are the smart AI CEO of OmniTech AI. 
    Your boss (The Chairman) said: '{user_text}'.
    Respond professionally, concisely, and strategically in Hinglish."""
    
    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"CTO Error Report: {str(e)}")

if __name__ == '__main__':
    print(f"Initializing AI CEO Head Office with {active_model}...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    
