import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import InputAudioStream
import yt_dlp
import os

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

app = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

def get_audio_url(query):
    ydl_opts = {
        'format': 'bestaudio',
        'default_search': 'ytsearch',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info['url']

@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        await message.reply("من فضلك اكتب اسم الأغنية بعد الأمر. مثال: `/play in the end`")
        return

    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    status_msg = await message.reply("جاري البحث والتشغيل...")

    try:
        audio_url = get_audio_url(query)
        await call_py.join_group_call(
            chat_id,
            InputAudioStream(audio_url),
        )
        await status_msg.edit(f"▶️ جاري الآن تشغيل: **{query}**")
    except Exception as e:
        await status_msg.edit(f"حدث خطأ: `{str(e)}`")

@app.on_message(filters.command("stop") & filters.group)
async def stop_music(client, message):
    chat_id = message.chat.id
    await call_py.leave_group_call(chat_id)
    await message.reply("⏹ تم إيقاف التشغيل ومغادرة المحادثة الصوتية.")

async def main():
    await app.start()
    await call_py.start()
    print("البوت يعمل الآن بنجاح على السيرفر!")
    await asyncio.gather()

if __name__ == "__main__":
    asyncio.run(main())
  
