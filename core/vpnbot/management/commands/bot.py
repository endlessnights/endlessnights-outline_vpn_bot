import os
import re
import time
import requests
from django.core.management import BaseCommand
from django.utils import timezone
from telebot import TeleBot, types
from telebot.types import CallbackQuery
from .get_vpn_api import get_settings_api, change_rateclass_api
from .config import show_admin_stats
from . import config
from ...models import Accounts

try:
    production = os.environ['PROD_OUTLINE_BOT']
except KeyError:
    print('NO PROD_OUTLINE_BOT')
try:
    tg_token = os.environ['TELEGRAM_BOT_SECRET_OUTLINE_BOT']
except KeyError:
    print('NO TELEGRAM_BOT_SECRET_OUTLINE_BOT')

bot = TeleBot(tg_token, threaded=False)
bot_admin = 12345678

last_user_message = {}


def delete_prev_message(message):
    if message.chat.id in last_user_message:
        bot.delete_message(message.chat.id, last_user_message[message.chat.id])
    bot.delete_message(message.chat.id, message.message_id)


def get_settings_inline_button(message, name):
    p = Accounts.objects.get(tgid=message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    get_settings_fin = types.InlineKeyboardButton(
        text=f'{config.my_settings_button_fin}',
        callback_data=f"get_settings,{message.chat.id},fin"
    )
    get_settings_ny = types.InlineKeyboardButton(
        text=f'{config.my_settings_button_ny}',
        callback_data=f"get_settings,{message.chat.id},ny"
    )
    get_settings_almaty = types.InlineKeyboardButton(
        text=f'{config.my_settings_button_almaty}',
        callback_data=f"get_settings,{message.chat.id},almaty"
    )
    get_settings_spb = types.InlineKeyboardButton(
        text=f'{config.my_settings_button_spb}',
        callback_data=f"get_settings,{message.chat.id},spb"
    )
    markup.add(get_settings_fin, get_settings_ny, get_settings_almaty, get_settings_spb)
    bot.send_message(message.chat.id, config.start_text.format(name), reply_markup=markup)


def show_keyboard_buttons(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    my_settings = types.KeyboardButton(text=config.keyboard_settings)
    my_stats = types.KeyboardButton(text=config.keyboard_stats)
    change_rateclass_btn = types.KeyboardButton(text=config.keyboard_change_rateclass)
    if message.chat.id == bot_admin:
        admin_button = types.KeyboardButton(text=config.keyboard_admin)
        keyboard.add(my_settings, my_stats, change_rateclass_btn, admin_button)
    else:
        keyboard.add(my_settings, my_stats, change_rateclass_btn)

    return keyboard


@bot.message_handler(commands=['start'])
def start_bot(message):
    #   Получаем базовые данные из Телеграм учетки
    try:
        if message.from_user.first_name and message.from_user.last_name:
            name = message.from_user.first_name + message.from_user.last_name
        else:
            name = message.from_user.first_name or message.from_user.last_name
    except AttributeError:
        # Handle the case where message.from_user doesn't have first_name or last_name
        name = None

    try:
        username = message.from_user.username
    except AttributeError:
        # Handle the case where message.from_user doesn't have a username
        username = None

    try:
        p, created = Accounts.objects.update_or_create(
            tgid=message.chat.id,
            defaults={
                'tglogin': username,
                'tgname': name,
                'lastdate': timezone.now(),
            }
        )
    except Exception as e:
        # Handle any exceptions that may occur during UserProfile creation/update
        print(f"An error occurred: {e}")

    p = Accounts.objects.get(tgid=message.chat.id)
    if not p.has_access:
        p = Accounts.objects.get(tgid=message.chat.id)
        p.has_access = True
        p.rateclass = 'paid1'
        try:
            p = Accounts.objects.get(tgid=message.chat.id)
            if p.has_access:
                get_settings_inline_button(message, p.tgname)
        except Exception as e:
            print(f'{e}:111')
    else:
        get_settings_inline_button(message, p.tgname)


@bot.message_handler(content_types=['text'])
def text_message(message):
    try:
        p = Accounts.objects.get(tgid=message.chat.id)
        chat_id = message.chat.id
        response_mapping = {
            config.keyboard_settings: config.show_vpn_settings(p),
            config.keyboard_stats: config.show_vpn_stats(p),
            config.keyboard_change_rateclass: config.change_rateclass_text(p),
        }
        if message.text in response_mapping:
            response = response_mapping[message.text]
            delete_prev_message(message)
            reply_text = bot.send_message(message.chat.id,
                                          text=response,
                                          disable_web_page_preview=True,
                                          parse_mode='HTML',
                                          reply_markup=show_keyboard_buttons(message))
            last_user_message[message.chat.id] = reply_text.message_id

        elif message.text == config.keyboard_admin:
            if message.chat.id == bot_admin:
                get_admin_stats = show_admin_stats(message, bot, bot_admin)
                show_text, server_ip = get_admin_stats
                markup = types.InlineKeyboardMarkup()
                admin_web = types.InlineKeyboardButton(
                    text='Открыть админку',
                    url=f'http://{server_ip}/admin/vpnbot/'
                )
                admin_change_rateclass = types.InlineKeyboardButton(
                    text='Сменить тариф пользователю',
                    callback_data=f'change_rateclass,{message.chat.id}'
                )

                markup.add(admin_web, admin_change_rateclass)
                delete_prev_message(message)
                admin_stats_reply = bot.send_message(bot_admin,
                                                     show_text,
                                                     disable_web_page_preview=True, parse_mode='HTML',
                                                     reply_markup=markup)
                last_user_message[message.chat.id] = admin_stats_reply.message_id
                bot.send_message(bot_admin, 'Показываю меню', reply_markup=show_keyboard_buttons(message))
    except Exception as e:
        print(f'def text_message: {e}')


@bot.callback_query_handler(func=lambda c: c.data.startswith("change_rateclass"))
def change_rateclass(c: CallbackQuery):
    callback_data = c.data.split(',')
    chat_id = int(callback_data[1])
    get_tgid = bot.send_message(chat_id=chat_id,
                                text='''
Отправь ID и новый тариф через запятую,
например: "12345678,paid2"
Варианты:
Personal [free] - 10 Гб/мес
Plus [paid1] - 50 Гб/мес
Pro [paid2] - 100 Гб/мес
Premium [paid3] - 200 Гб/мес
''')
    bot.register_next_step_handler(get_tgid, get_tgid_from_admin_input)
    bot.answer_callback_query(c.id)


def get_tgid_from_admin_input(message):
    try:
        tgid, rate_class = message.text.split(',')
    except Exception as e:
        bot.send_message(message.chat.id, f'def get_tgid_from_admin_input error: {e}')
    try:
        new_rate_class = change_rateclass_api(int(tgid), rate_class)
        new_rate_class_str = new_rate_class
        p = Accounts.objects.get(tgid=tgid)
        bot.send_message(bot_admin, f'''Пользователь
ID: {tgid}
Новый тариф: {new_rate_class_str}
Новый лимит трафика: {'10' if p.rateclass == 'free' else '50' if
        p.rateclass == 'paid1' else '100' if p.rateclass == 'paid2' else '200' if p.rateclass == 'paid3' else '0'}

''')
    except Exception as e:
        bot.send_dice(message.chat.id, f'Error in def get_tgid_from_admin_input:\n{e}')


def send_msg_show_settings(chat_id, keyboard, country_text):
    bot.send_message(
        chat_id=chat_id,
        text=country_text,
        parse_mode='HTML',
        disable_web_page_preview=True,
        reply_markup=keyboard)

def generate_vpn_settings(username_gen, chat_id, p, keyboard, country_tag):
    try:
        if country_tag == 'fin':
            vpn_settings = get_settings_api(username_gen, p.rateclass, country_tag)
            p.vpn_key_id, p.vpn_key_name, p.vpn_key_password, p.vpn_key_port, p.vpn_access_url, get_data_limit_diplay = vpn_settings
            p.save()
            send_msg_show_settings(chat_id, keyboard, config.show_vpn_settings_fin(p))
        elif country_tag == 'ny':
            vpn_settings = get_settings_api(username_gen, p.rateclass, country_tag)
            p.vpn_id_ny, p.vpn_name_ny, p.vpn_password_ny, p.vpn_port_ny, p.vpn_url_ny, get_data_limit_diplay = vpn_settings
            p.save()
            send_msg_show_settings(chat_id, keyboard, config.show_vpn_settings_ny(p))
        elif country_tag == 'spb':
            vpn_settings = get_settings_api(username_gen, p.rateclass, country_tag)
            p.vpn_id_spb, p.vpn_name_spb, p.vpn_password_spb, p.vpn_port_spb, p.vpn_url_spb, get_data_limit_diplay = vpn_settings
            p.save()
            send_msg_show_settings(chat_id, keyboard, config.show_vpn_settings_spb(p))
        elif country_tag == 'almaty':
            vpn_settings = get_settings_api(username_gen, p.rateclass, country_tag)
            p.vpn_id_almaty, p.vpn_name_almaty, p.vpn_password_almaty, p.vpn_port_almaty, p.vpn_url_almaty, get_data_limit_diplay = vpn_settings
            p.save()
            send_msg_show_settings(chat_id, keyboard, config.show_vpn_settings_almaty(p))
    except Exception as e:
        print(f'generate_vpn_settings: {e}')
        bot.send_message(bot_admin, f'Ошибка API:\n{e}')


@bot.callback_query_handler(func=lambda c: c.data.startswith("get_settings"))
def get_settings(c: CallbackQuery):
    callback_data = c.data.split(',')
    chat_id = int(callback_data[1])
    country_tag = str(callback_data[2])
    p = Accounts.objects.get(tgid=chat_id)
    if p.has_access:
        if p.userlogin:
            # Generate username as 'user_userlogin_tg-123456-id_dd_mm_yyyy'
            username_gen = ''
            if country_tag == 'fin':
                username_gen = f'user_{p.userlogin}_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            elif country_tag == 'ny':
                username_gen = f'user_ny_{p.userlogin}_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            elif country_tag == 'spb':
                username_gen = f'user_spb_{p.userlogin}_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            elif country_tag == 'almaty':
                username_gen = f'user_almaty_{p.userlogin}_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            generate_vpn_settings(username_gen, chat_id, p, show_keyboard_buttons(c.message), country_tag)
        else:
            if country_tag == 'fin':
                # Generate username as 'user_-tg-123456-id_dd_mm_yyyy'
                username_gen = f'user_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            elif country_tag == 'ny':
                username_gen = f'user_ny_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            elif country_tag == 'spb':
                username_gen = f'user_spb_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            elif country_tag == 'almaty':
                username_gen = f'user_almaty_tg-{p.tgid}-id_{timezone.now().strftime("%d_%m_%Y")}'
            generate_vpn_settings(username_gen, chat_id, p, show_keyboard_buttons(c.message), country_tag)
    else:
        bot.send_message(c.message.chat.id, config.password_is_wrong)
    bot.answer_callback_query(c.id)


def send_events(new_post, image):
    p = Accounts.objects.all()
    for user in p:
        time.sleep(0.25)
        try:
            if image:
                photo_path = image.path
                photo = open(photo_path, 'rb')
                bot.send_photo(chat_id=user.tgid, photo=photo, caption=new_post, parse_mode='HTML')
            else:
                bot.send_message(chat_id=user.tgid, text=new_post, disable_web_page_preview=True, parse_mode='HTML')
        except Exception as e:
            print(f'send_events: {e}')


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'
    if production:
        def handle(self, *args, **kwargs):
                while True:
                    try:
                        bot.polling(none_stop=True, timeout=30)
                    except requests.exceptions.ReadTimeout:
                        print('Read timeout exception. Retrying in 10 seconds...')
                        time.sleep(10)
    else:
        def handle(self, *args, **kwargs):
            bot.polling(none_stop=True)

# class Command(BaseCommand):
#     help = 'Implemented to Django application telegram bot setup command'
#
#     def handle(self, *args, **kwargs):
#         bot.polling(none_stop=True)
