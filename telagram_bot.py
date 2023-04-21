import telebot
from pytube import YouTube, exceptions
from io import BytesIO
import YouTubeMusicAPI


class YTAudio:
    def __init__(self):
        self.streams = None  # Interface to query both adaptive (DASH) and progressive streams
        self.title = None  # Title of the video
        self.author = None  # Video uploader
        self.views = None  # Current views on the video


def get_info(message):
    try:
        res = YouTubeMusicAPI.search(message)
        err_msg = "Введите название песни..."
        yt = YouTube(res['url'])
    except exceptions.RegexMatchError:
        return False, err_msg
    else:
        yt_title = res['title']
        yt_author = res['author']['name']
        yt_views = yt.views
        yt_streams = yt.streams
        return yt_title, yt_author, yt_views, yt_streams


if __name__ == '__main__':
    bot = telebot.TeleBot('6109358676:AAGubiYah6wQccqZRDI1G-BXqO4WAcm8TO4')
    chats = {}
    error_msg = None


    @bot.message_handler(commands=['start'])
    def welcome(message):
        chat_id = message.chat.id
        yt_audio = YTAudio()
        chats[chat_id] = yt_audio
        bot.send_message(chat_id,
                         "Добро Пожаловать, {0.first_name}!\n"
                         ""
                         "♫ Это бот, который не только найдёт песню, но и порекомендует свою! ♫"
                         "\n\n<b>Доступные команды:</b>"
                         "\n/start - запустить бота"
                         "\n/find - найти свою песню"
                         "\n/recommend - наши рекомендации".format(message.from_user, bot.get_me()),
                         parse_mode='html')


    @bot.message_handler(commands=['find'])
    def get_text_messages(message):
        chat_id = message.chat.id
        if message.chat.type == "private":
            if chat_id not in chats.keys():
                bot.send_message(message.chat.id, "Плиииз, возобновите работу бота с помощью команды /start")
            else:
                bot.send_message(message.chat.id, "Введите название песни...")
                cur_chat = chats[chat_id]
                mes = message.text
                audio_info = get_info(mes)
                try:
                    msg = bot.send_message(chat_id, "Минуточку...")
                    cur_chat.title = audio_info[0]
                    cur_chat.author = audio_info[1]
                    cur_chat.views = audio_info[2]
                    cur_chat.streams = audio_info[3]
                    audio_stream = cur_chat.streams.filter(only_audio=True).first()
                    buffer = BytesIO()
                    audio_stream.stream_to_buffer(buffer)
                    buffer.seek(0)
                    bot.delete_message(chat_id, msg.message_id)
                    bot.send_audio(chat_id, buffer,
                                   title=cur_chat.title, performer=cur_chat.author)

                    bot.send_message(chat_id,
                                     "<b>► Название:</b>  {0}\n"
                                     "<b>► Автор:</b>  {1}\n"
                                     "<b>► Просмотры:</b>  {2} views\n".format(chats[chat_id].title,
                                                                        chats[chat_id].author,
                                                                        chats[chat_id].views,),
                                     parse_mode='html')

                except telebot.apihelper.ApiTelegramException:
                    bot.send_message(chat_id, "К сожалению, Telegram не поддерживает размер такого файла (￣︿￣)")

                except Exception:
                    bot.send_message(chat_id, "Упс! Что-то пошло не так (o_O)")


    bot.polling(none_stop=True)
