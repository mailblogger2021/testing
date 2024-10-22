import os
import sqlite3
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '6511501073:AAHbWvFY_dKcUQfKNGFODOeYK8PEUJ4vXPI'

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

def add_link(keyword, link):
    conn = sqlite3.connect('affiliate_links.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO links (keyword, link) VALUES (?, ?)', (keyword, link))
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
    add_link('book', 'https://www.amazon.com/your-affiliate-link-for-book')
    add_link('laptop', 'https://www.amazon.com/your-affiliate-link-for-laptop')

    updater = Updater(token=TOKEN, use_context=True)
    
    # Add handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    # Start polling in a separate thread
    updater.start_polling()
    
    # Run the bot for 6 hours (21600 seconds)
    time.sleep(21600)  # 6 hours in seconds
    
    updater.stop()  # Stop the bot after 6 hours
    print("Bot has run for 6 hours and is now stopping.")

if __name__ == '__main__':
    main()
