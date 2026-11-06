import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL = "@logovo12"
CHANNEL_URL = "https://t.me/logovo12"

SUB_BLACK = "https://gist.githubusercontent.com/horko236/cb207302b58fdf64e06e79b7ac572f09/raw/pulod.txt?v=2"
# ТУТ ОБНОВЛЕННЫЙ БЕЛЫЙ СПИСОК
SUB_WHITE = "https://gist.githubusercontent.com/horko236/4766da8a03aee9044f3dd92b04290cc0/raw/pulod.txt?t=2"
SUB_INCY  = "https://gist.githubusercontent.com/horko236/399bbbf8a9dea85300986fc22cac9d3e/raw/pulod.txt?v=2"

PROXIES = {
    "us": ("США", "https://t.me/proxy?server=web.gktmfrv.sbs&port=443&secret=ee8d2347ee3bfd6ba6299947017bf28dc16364656b2e7275"),
    "de": ("Германия", "https://t.me/proxy?server=static.antenna-mzt.live&port=443&secret=ee5a42e3752e724f2fdae9c117e7f076fe73746f72652e737465616d706f77657265642e636f6d"),
    "fr": ("Франция", "https://t.me/proxy?server=surf.suslik-cloud.com&port=443&secret=eed7f61466f824eafe116a533553e01bca737572662e7375736c696b2d636c6f75642e636f6d"),
    "ua": ("Украина", "https://t.me/proxy?server=posude79.fernlark.xyz&port=443&secret=ee37a60897c9ca648e94350eb8919ea47f706f7375646537392e6665726e6c61726b2e78797a"),
}

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Подключиться", callback_data="connect"))
    markup.add(InlineKeyboardButton("Подключить прокси", callback_data="proxy"))
    return markup

def connect_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Чёрный список", callback_data="sub:black"))
    markup.add(InlineKeyboardButton("Белый список", callback_data="sub:white"))
    markup.add(InlineKeyboardButton("Для Incy", callback_data="sub:incy"))
    markup.add(InlineKeyboardButton("Назад", callback_data="back_main"))
    return markup

def proxy_menu():
    markup = InlineKeyboardMarkup()
    for key, (label, _) in PROXIES.items():
        markup.add(InlineKeyboardButton(label, callback_data=f"px:{key}"))
    markup.add(InlineKeyboardButton("Назад", callback_data="back_main"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "<b>Добро пожаловать в Chad VPN!</b>\n\n"
        "Мы рады видеть тебя в нашем VPN.\n\n"
        "Здесь ты найдёшь подписки для <b>Happ</b> и <b>Incy</b>.\n"
        "Выбирай нужный вариант и подключайся — VPN безлимитный и бесконечный.\n\n"
        "Нажми кнопку ниже:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "back_main":
        bot.edit_message_text("<b>Главное меню Chad VPN</b>\n\nВыбирай действие:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
        bot.answer_callback_query(call.id)
    elif call.data == "connect":
        bot.edit_message_text("<b>Выбери тип подписки:</b>\n\nЧёрный список — базовый набор\nБелый список — расширенный\nДля Incy — отдельная подписка", call.message.chat.id, call.message.message_id, reply_markup=connect_menu())
        bot.answer_callback_query(call.id)
    elif call.data == "proxy":
        bot.edit_message_text("<b>Выбери страну прокси:</b>\n\nПосле выбора бот пришлёт кликабельную ссылку — нажми на неё, и Telegram предложит подключить прокси.", call.message.chat.id, call.message.message_id, reply_markup=proxy_menu())
        bot.answer_callback_query(call.id)
    elif call.data.startswith("px:"):
        key = call.data.split(":")[1]
        label, link = PROXIES[key]
        bot.send_message(call.message.chat.id, f"{label} — прокси готов.\n\nНажми на ссылку, чтобы подключить:\n{link}", disable_web_page_preview=True)
        bot.answer_callback_query(call.id, "Ссылка отправлена")
    elif call.data.startswith("sub:"):
        kind = call.data.split(":")[1]
        if not is_subscribed(call.from_user.id):
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Подписаться", url=CHANNEL_URL))
            markup.add(InlineKeyboardButton("Я подписался", callback_data=f"check_sub:{kind}"))
            bot.edit_message_text(f"<b>Доступ только для подписчиков.</b>\n\nЧтобы получить ссылку, подпишись на наш канал {CHANNEL_URL}\n\nПосле подписки нажми «Я подписался».", call.message.chat.id, call.message.message_id, reply_markup=markup)
            bot.answer_callback_query(call.id)
        else:
            give_sub(call, kind)
    elif call.data.startswith("check_sub:"):
        kind = call.data.split(":")[1]
        if not is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "Ты ещё не подписался", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Подписка подтверждена")
            if kind == "back":
                bot.edit_message_text("<b>Главное меню Chad VPN</b>\n\nВыбирай действие:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
            else:
                give_sub(call, kind)

def give_sub(call, kind):
    if kind == "black":
        title, url = "Чёрный список", SUB_BLACK
    elif kind == "white":
        title, url = "Белый список", SUB_WHITE
    else:
        title, url = "Для Incy", SUB_INCY
    text = (
        f"{title} — готово.\n\n"
        f"Твоя ссылка подписки:\n<code>{url}</code>\n\n"
        "<b>Как подключить:</b>\n"
        "Happ — открой приложение, нажми «+», выбери «Импорт из буфера или по ссылке», вставь ссылку\n"
        "Incy — открой, выбери «Добавить подписку», вставь ссылку\n\n"
        "Подписка безлимитная и бесконечная."
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    print("Бот Chad VPN успешно запущен в облаке!")
    bot.infinity_polling(timeout=20, long_polling_timeout=20, none_stop=True)