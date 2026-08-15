import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Railway se API Keys lena
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# CEO ka Dimaag (Gemini AI) On karna
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = "Greetings Chairman! 👔 Main aapka AI CEO hoon. Head Office ke sabhi systems online hain. Boliye, aaj ka hamara pehla corporate target kya hai?"
    await update.message.reply_text(welcome_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # CEO ko uski duty yaad dilana
    prompt = f"""You are the extremely smart AI CEO of a Billion-Dollar Tech Group. 
    Your boss (The Chairman) just gave you this command/message: '{user_text}'.
    Respond professionally, like a real CEO. You manage the Sultan Trading Division, R&D Labs, and Cybersecurity. 
    Keep your response concise, strategic, and use a mix of Hindi and English (Hinglish)."""
    
    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        # Asli technical error yahan print hoga
        await update.message.reply_text(f"CTO Error Report: {str(e)}")

if __name__ == '__main__':
    print("Initializing AI CEO Head Office...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("AI CEO is Online and waiting for Chairman's orders on Telegram!")
    app.run_polling()
    
