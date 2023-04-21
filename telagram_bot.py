import telebot
from pytube import YouTube, exceptions
from io import BytesIO
import YouTubeMusicAPI


class YTAudio:
    def __init__(self):
        self.streams = None  # Interface to query both adaptive (DASH) and progressive streams
        self.title = None  # Title of the video
        self.duration = None  # Video length
        self.author = None  # Video uploader
        self.thumbnail = None  # Video thumbnail


def validate_link(yt):
    try:
        yt.check_availability()
        return True
    except exceptions.VideoUnavailable:
        return False


def get_info(message):
    try:
        result = YouTubeMusicAPI.search(message.text)
        yt = YouTube(result['url'])
        err_msg = "Please send a YT link :-)"
    except exceptions.RegexMatchError:
        return False, err_msg

    if not validate_link(yt):
        err_msg = "Video unavailable 😕"
        return False, err_msg
    else:
        yt_streams = yt.streams
        yt_title = yt.title
        yt_author = yt.author
        yt_thumb = yt.thumbnail_url
        return yt_streams, yt_title, yt_author, yt_thumb


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
                         "Welcome, {0.first_name}!\n"
                         "I am a bot for converting YouTube videos to downloadable audio."
                         "\n\nPlease send a link to a YT video to start :-)"""
                         "\n\n<b>Available commands:</b>"
                         "\n/start - initialize the bot"
                         "\n/help - to see available commands".format(message.from_user, bot.get_me()),
                         parse_mode='html')


    # @bot.message_handler(commands=['help'])
    # def command_help(message):
    #     chat_id = message.chat.id
    #     bot.send_message(chat_id, "<b>Available commands:</b>"
    #                               "\n/start - initialize the bot"
    #                               "\n/help - to see available commands"
    #                               "\n/info - to get info about the last video",
    #                      parse_mode='html')

    # @bot.message_handler(commands=['info'])
    # def command_info(message):
    #     chat_id = message.chat.id
    #     if chat_id not in chats.keys() or chats[chat_id].streams is None:
    #         bot.send_message(chat_id, "Please send a link first")
    #     else:
    #         bot.send_message(chat_id,
    #                          "<b>Title:</b> {0}\n"
    #                          "<b>Uploader:</b> {1}\n"
    #                          "<b>Duration:</b> {2} seconds\n"
    #                          "<b>Views:</b> {3} views\n"
    #                          "<b>Description:</b> {4}\n".format(chats[chat_id].title,
    #                                                             chats[chat_id].author,
    #                                                             chats[chat_id].duration,
    #                                                             chats[chat_id].views,
    #                                                             chats[chat_id].description),
    #                          parse_mode='html')

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        chat_id = message.chat.id
        if message.chat.type == "private":
            if chat_id not in chats.keys():
                bot.send_message(message.chat.id, "Please initialize chat with /start")
            else:
                cur_chat = chats[chat_id]
                link = message.text
                audio_info = get_info(link)
                if not audio_info[0]:
                    bot.send_message(chat_id, audio_info[1])
                else:
                    try:
                        msg = bot.send_message(chat_id, "Please wait⌛ ⌛ ⌛ ")
                        cur_chat.streams = audio_info[0]
                        cur_chat.title = audio_info[1]
                        cur_chat.author = audio_info[2]
                        cur_chat.thumbnail = audio_info[6]
                        audio_stream = cur_chat.streams.filter(only_audio=True).first()
                        buffer = BytesIO()
                        audio_stream.stream_to_buffer(buffer)
                        buffer.seek(0)
                        bot.delete_message(chat_id, msg.message_id)
                        bot.send_audio(chat_id, buffer, duration=cur_chat.duration,
                                       title=cur_chat.title, performer=cur_chat.author, thumb=cur_chat.thumbnail)

                        bot.send_message(chat_id,
                                         "<b>Title:</b> {0}\n"
                                         "<b>Uploader:</b> {1}\n".format(chats[chat_id].title,
                                                                         chats[chat_id].author),
                                         parse_mode='html')

                    except telebot.apihelper.ApiTelegramException:
                        bot.send_message(chat_id, "Audio of such size cannot be sent through telegram 🤓")

                    except Exception:
                        bot.send_message(chat_id, "Something went wrong 🤔")


    bot.polling(none_stop=True)
