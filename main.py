import wikipedia, re
import logging
import os

from aiogram import Bot, Dispatcher, types, executor



logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token='5028446744:AAHaG-2_ph0udlgyhZHXj9VK0UZaoSXLXN0')
dp = Dispatcher(bot)
# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
# Функция, обрабатывающая команду /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Отправьте мне любое слово, и я найду его значение на Wikipedia')

# Получение сообщений от юзера
@dp.message_handler(content_types=["text"])
async def send_echo(message):
    await message.answer(getwiki(message.text))
# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)