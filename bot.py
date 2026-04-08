import discord
import os
from flask import Flask
from threading import Thread

# ========== ВЕБ-СЕРВЕР ДЛЯ RAILWAY ==========
app = Flask('')

@app.route('/')
def home():
    return "✅ Бот активен и играет музыку!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ============================================

TOKEN = os.getenv("DISCORD_TOKEN")

# ===== НАСТРОЙКИ =====
VOICE_CHANNEL_ID = 981189520135454791   # ЗАМЕНИТЕ НА ВАШ ID
MUSIC_FILE = "track.mp3"
# ====================

class MusicBot(discord.Client):
    async def on_ready(self):
        print(f"✅ Бот {self.user} запущен")
        
        channel = self.get_channel(VOICE_CHANNEL_ID)
        if not isinstance(channel, discord.VoiceChannel):
            print("❌ Ошибка: указанный ID не является голосовым каналом")
            await self.close()
            return
        
        try:
            vc = await channel.connect()
            print(f"🔊 Подключился к каналу {channel.name}")
        except Exception as e:
            print(f"❌ Не удалось подключиться: {e}")
            await self.close()
            return
        
        track_name = os.path.splitext(os.path.basename(MUSIC_FILE))[0]
        try:
            await channel.edit(name=f"🎵 {track_name}")
            print(f"🏷️ Название канала изменено на: {track_name}")
        except Exception as e:
            print(f"⚠️ Не удалось изменить название канала: {e}")
        
        def repeat(error):
            if error:
                print(f"❌ Ошибка воспроизведения: {error}")
                return
            if vc.is_connected():
                vc.play(discord.FFmpegPCMAudio(MUSIC_FILE), after=repeat)
            else:
                print("⚠️ Соединение потеряно, повтор не запущен")
        
        vc.play(discord.FFmpegPCMAudio(MUSIC_FILE), after=repeat)
        print(f"🎶 Играет: {track_name} (зациклено)")

client = MusicBot()

if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)