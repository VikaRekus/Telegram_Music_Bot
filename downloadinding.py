def downloading(link, message):
    bot.send_message(message.chat.id, 'Скачиваем... '+link)

    my_video = YouTube(link)
    path = my_video.streams.get_highest_resolution().download()
    video = open(path, 'rb')
    print(path)
    bot.send_video(message.chat.id, video)