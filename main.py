from pyrogram import Client, filters
import yt_dlp
import pyromod
from pyrogram.types import Message
import os

BOT_TOKEN = "6417384180:AAET1sC3LMkRUSwaYjXrWe1vu6u6EY4Ls5Y"
api_id = 6590520
api_hash = "7f31db7e8cd1c0959c187e2651935c00"
app = Client("hma_bot", api_id=api_id, api_hash=api_hash, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["video"]))
async def request_url(client, m: Message):
    editable = await m.reply_text("**Send the YouTube Video Link**")
    input_message: Message = await app.listen(editable.chat.id)
    
    if not input_message.text:
        await editable.edit("**Please send a valid YouTube URL**")
        return
    
    url = input_message.text
    await editable.edit("**Send the desired video quality (e.g., 720p, 1080p)**")
    quality_message: Message = await app.listen(editable.chat.id)
    
    if not quality_message.text:
        await editable.edit("**Please specify a valid quality option**")
        return
    
    quality = quality_message.text.strip().lower()
    path = "./downloads/"
    os.makedirs(path, exist_ok=True)
    
    # Map quality options to yt-dlp formats
    quality_map = {
        '360p': 'worstvideo',
        '480p': 'bestaudio/best',
        '720p': 'bestvideo[height<=720]+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best',
        'best': 'bestvideo+bestaudio/best'
    }
    
    # Default to best if quality not in map
    format_option = quality_map.get(quality, 'bestvideo+bestaudio/best')
    
    # Set up yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'format': format_option,
        'noplaylist': True
    }
    
    # Download the video
    await editable.edit("**Starting Downloading Video...**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            video_file = os.path.join(path, f"{video_title}.mp4")
        
        # Check if the file exists
        if not os.path.isfile(video_file):
            await editable.edit("**Failed to download the video. The file does not exist.**")
            return
        
        # Customize the caption
        caption = f"Here is your video: *{video_title}*\nQuality: *{quality}*"
        
        # Send the downloaded video to the user
        await editable.edit("**Uploading Video...**")
        await client.send_video(chat_id=m.chat.id, video=video_file, caption=caption, parse_mode='markdown')
        
    except Exception as e:
        await editable.edit(f"**Error: {str(e)}**")
    
    finally:
        # Clean up downloaded files
        if os.path.exists(video_file):
            os.remove(video_file)

app.run()
