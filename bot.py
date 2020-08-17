import youtube_dl
from aiogram import Bot, Dispatcher, executor, types
import os, time

token = ''  # You need a telegram token, you can create your own bot with this,
            # just search for a video on how to create a bot on telegram (15 seconds), and input the token here.
bot = Bot(token=token)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.from_user.id, 'Hello!, Just input a URL to download!')


@dispatcher.message_handler()
async def start(message: types.message):
    await bot.send_message(message.from_user.id, 'Great! Wait a few seconds.. im downloading it for you..')
    video = await run(message.text)
    await bot.send_message(message.from_user.id, 'Downloaded..sending it to you...')
    mp3 = video[0]
    await bot.send_audio(message.from_user.id, audio=mp3)
    time.sleep(5)
    os.remove(video[1])


async def run(url):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=url, download=False
    )
    filename = f"{video_info['title']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
        video = open(f'{filename}', 'rb')
        return [video, filename]


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
