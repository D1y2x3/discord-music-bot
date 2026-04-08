import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ===== НАСТРОЙКИ (ИЗМЕНИ ПОД СЕБЯ) =====
VOICE_CHANNEL_ID = 981189520135454791   # ID голосового канала
MUSIC_FILE = "./music/track.mp3"        # путь к твоему одному треку
# =======================================

class SingleTrackBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        super().__init__(intents=intents)
        self.has_played = False   # флаг, чтобы не играть повторно при переподключении

    async def on_ready(self):
        print(f"Бот {self.user} запущен. Захожу в канал...")
        channel = self.get_channel(VOICE_CHANNEL_ID)
        if not isinstance(channel, discord.VoiceChannel):
            print("Ошибка: указанный ID не является голосовым каналом")
            return
        try:
            voice_client = await channel.connect()
            print(f"Подключился к каналу {channel.name}")
        except Exception as e:
            print(f"Не удалось подключиться: {e}")
            return

        # Меняем название канала на имя трека (без расширения)
        track_name = os.path.basename(MUSIC_FILE).replace(".mp3", "")
        await channel.edit(name=f"🎵 {track_name}")
        print(f"Название канала изменено на: {track_name}")

        # Начинаем проигрывание
        if not self.has_played:
            voice_client.play(discord.FFmpegPCMAudio(MUSIC_FILE))
            self.has_played = True
            print("Играет музыка...")

client = SingleTrackBot()
client.run(TOKEN)