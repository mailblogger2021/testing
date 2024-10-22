import django
import os
import re
from telegram.ext import *
from django.core.management.base import BaseCommand
from home.models import CowinData
from home.helpers import get_cowin_data_by_pincode

API_KEY = '6511501073:AAHbWvFY_dKcUQfKNGFODOeYK8PEUJ4vXPI'

# Helper function to validate pincode
def isValidPinCode(pinCode):
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
    p = re.compile(regex)
    if not pinCode:
        return False
    return re.match(p, pinCode) is not None

# Check if a string contains numbers
def num_there(s):
    return any(i.isdigit() for i in s)

# Handle incoming messages from Telegram
def handle_message(update, context):
    text = str(update.message.text).lower()

    if num_there(text):
        if isValidPinCode(text):
            cowin_objs = CowinData.objects.filter(pincode=text)

            if not cowin_objs.exists():
                get_cowin_data_by_pincode(text)
                cowin_objs = CowinData.objects.filter(pincode=text)

            message = f"Total {cowin_objs.count()} slots found in your pincode:\n"

            for cowin_obj in cowin_objs:
                message += f"""Place: {cowin_obj.fee_type}, Fee: {cowin_obj.fee}, Capacity: {cowin_obj.available_capacity}, 
                Dose1: {cowin_obj.available_capacity_dose1}, Dose2: {cowin_obj.available_capacity_dose2}, 
                Age Limit: {cowin_obj.min_age_limit}, Vaccine: {cowin_obj.vaccine}\n\n"""

            update.message.reply_text(message)
        else:
            update.message.reply_text("Not a valid pincode.")
    else:
        update.message.reply_text(f"Hi, {update.message.chat.first_name}, enter a valid pincode to get vaccine updates.")

# Command to start the bot
class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        updater = Updater(API_KEY, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(MessageHandler(Filters.text, handle_message))

        updater.start_polling(1.0)
        updater.idle()
