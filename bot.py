import os
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace with your actual bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize the database
def init_db():
    conn = sqlite3.connect('affiliate_links.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            link TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I am your Amazon affiliate bot. Ask me about products!')

# Function to respond to user messages
def respond(update: Update, context: CallbackContext):
    message_text = update.message.text
    conn = sqlite3.connect('affiliate_links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT link FROM links WHERE keyword = ?', (message_text,))
    result = cursor.fetchone()
    
    if result:
        update.message.reply_text(f'Here is your link: {result[0]}')
    else:
        update.message.reply_text("Sorry, I don't have a link for that keyword.")
    
    conn.close()

def main():
    init_db()
    
    updater = Updater(token=TOKEN, use_context=True)
    
    # Add handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
