import youtube_dl  # pip install youtube-dl==2020.5.29
from aiogram import Bot, Dispatcher, executor, types
import os, time

token = ''  # You need a bot token, search for BotFather on telegram.
bot = Bot(token=token)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.from_user.id, 'Hello!, I am a HK ROBOT YOUTUBE DOWNLOADER BOT Just input a URL to download!')


@dispatcher.message_handler()
async def start(message: types.message):
    """
    Takes the url, sends it to the download func.
    The download func returns a list of the file.mp3, and the title.
    The file is sent to the user, and the title is just so we can delete the file later on
    :param message:
    :return:
    """
    await bot.send_message(message.from_user.id, 'Great! Wait a few seconds.. im downloading it for you..')
    video = await download(message.text)
    await bot.send_message(message.from_user.id, 'Downloaded..sending it to you...')
    mp3 = video[0]
    await bot.send_audio(message.from_user.id, audio=mp3)
    # Delete the file.
    time.sleep(5)
    os.remove(video[1])


async def download(url):
    video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
    filename = f"{video_info['title']}.mp3"
    options = {'format': 'bestaudio/best', 'keepvideo': False, 'outtmpl': filename}

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
        video = open(f'{filename}', 'rb')
        return [video, filename]


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
