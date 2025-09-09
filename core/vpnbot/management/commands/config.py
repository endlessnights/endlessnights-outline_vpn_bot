import requests
from telebot import types
from ...models import Accounts
from .get_vpn_api import get_stats_api

start_text_new = '''
Привет, {}
Этот Бот выдает настройки Outline VPN по протоколу Shadowsocks.

Personal - 10 Гб/мес - 300 руб/год
Plus - 50 Гб/мес - 1000 руб/год
Pro - 100 Гб/мес - 1500 руб/год
Premium - 200 Гб/мес - 2400 руб/год
Варианты оплаты: СБП РФ, YooMoney, TonCoin, USDT (TRX)

После оплаты у вас будут доступны 4 локации:
1. 🇺🇸США (Нью-Йорк)
2. 🇫🇮Финляндия (Хельсинки)
3. 🇰🇿Казахстан (Алматы)
4. 🇷🇺Россия (СПб)

По любым вопросам и предложениям: 
'''

start_text = '''
Привет, {}
Этот Бот выдает настройки Outline VPN по протоколу Shadowsocks.

Personal - 10 Гб/мес - 300 руб/год
Plus - 50 Гб/мес - 1000 руб/год
Pro - 100 Гб/мес - 1500 руб/год
Premium - 200 Гб/мес - 2400 руб/год
Варианты оплаты: СБП РФ, YooMoney, TonCoin, USDT (TRX)

После оплаты у вас будут доступны 4 локации:
1. 🇺🇸США (Нью-Йорк)
2. 🇫🇮Финляндия (Хельсинки)
3. 🇰🇿Казахстан (Алматы)
4. 🇷🇺Россия (СПб)

По любым вопросам и предложениям: 
'''
ask_password = '''Введите пароль, чтобы начать пользоваться ботом. 

По любым вопросам и предложениям писать: 
'''
password_is_wrong = 'Пароль введен неверно, нажмите /start , чтобы начать сначала.'

my_settings_button_fin = 'Мой VPN в 🇫🇮Финляндии (Хельсинки)'
my_settings_button_ny = 'Мой VPN в 🇺🇸США (Нью-Йорк)'
my_settings_button_almaty = 'Мой VPN в 🇰🇿Казахстане (Алматы)'
my_settings_button_spb = 'Мой VPN в 🇷🇺России (СПб)'

keyboard_settings = 'Мои настройки'
keyboard_stats = 'Моя статистика'
keyboard_change_rateclass = 'Сменить тарифный план'
keyboard_admin = 'Администрирование'


def change_rateclass_text(p):
    text = f'''
Отправьте в ЛС  следующие данные для смены тарифа
<code>
TGID: {p.tgid}
Key_ID: {p.vpn_key_id}
Key_Name: {p.vpn_key_name}
Rate: {p.get_rateclass_display()} ({'10' if p.rateclass=='free' else '50' if 
p.rateclass=='paid1' else '100' if p.rateclass=='paid2' else '200' if p.rateclass=='paid3' else '0'} Гб/мес)
</code>

А также укажите желаемый тарифный план на который хотите перейти:

Personal - 10 Гб/мес
Plus - 50 Гб/мес - 1000 руб/год
Pro - 100 Гб/мес - 1500 руб/год
Premium - 200 Гб/мес - 2400 руб/год

Варианты оплаты: СБП, YooMoney, TonCoin, USDT
'''
    return text


def show_vpn_settings_fin(p):
    vpn_settings = f'''
Настройки Outline VPN 🇫🇮Финляндия (Хельсинки):
    
Ваш тарифный план: <b>{p.get_rateclass_display()} - {'10' if p.rateclass=='free' else '50' if 
p.rateclass=='paid1' else '100' if p.rateclass=='paid2' else '200' if p.rateclass=='paid3' else '0'} Гб/мес</b>

Ключ доступа: <code>{p.vpn_access_url}</code>

<i>Нажмите на содержимое и оно автоматически скопируется в буфер обмена.
Для получения настроек для других регионов (Финляндия, США, Казахстан или Россия), нажмите /start.</i>
'''
    return vpn_settings


def show_vpn_settings_ny(p):
    vpn_settings = f'''
Настройки Outline VPN 🇺🇸США (Нью-Йорк):

Ваш тарифный план: <b>{p.get_rateclass_display()} - {'10' if p.rateclass == 'free' else '50' if
    p.rateclass == 'paid1' else '100' if p.rateclass == 'paid2' else '200' if p.rateclass == 'paid3' else '0'} Гб/мес</b>

Ключ доступа: <code>{p.vpn_url_ny}</code>

<i>Нажмите на содержимое и оно автоматически скопируется в буфер обмена.
Для получения настроек для других регионов (Финляндия, США, Казахстан или Россия), нажмите /start.</i>
'''
    return vpn_settings

def show_vpn_settings_spb(p):
    vpn_settings = f'''
Настройки Outline VPN 🇷🇺Россия (СПб):

Ваш тарифный план: <b>{p.get_rateclass_display()} - {'10' if p.rateclass == 'free' else '50' if
    p.rateclass == 'paid1' else '100' if p.rateclass == 'paid2' else '200' if p.rateclass == 'paid3' else '0'} Гб/мес</b>

Ключ доступа: <code>{p.vpn_url_spb}</code>

<i>Нажмите на содержимое и оно автоматически скопируется в буфер обмена.
Для получения настроек для других регионов (Финляндия, США, Казахстан или Россия), нажмите /start.</i>
'''
    return vpn_settings


def show_vpn_settings_almaty(p):
    vpn_settings = f'''
Настройки Outline VPN 🇰🇿Казахстан (Алматы):

Ваш тарифный план: <b>{p.get_rateclass_display()} - {'10' if p.rateclass == 'free' else '50' if
    p.rateclass == 'paid1' else '100' if p.rateclass == 'paid2' else '200' if p.rateclass == 'paid3' else '0'} Гб/мес</b>

Ключ доступа: <code>{p.vpn_url_almaty}</code>

<i>Нажмите на содержимое и оно автоматически скопируется в буфер обмена.
Для получения настроек для других регионов (Финляндия, Казахстан или Россия), нажмите /start.</i>
'''
    return vpn_settings


def show_vpn_settings(p):
    vpn_settings = f'''
Настройки Outline VPN:

Ваш тарифный план: <b>{p.get_rateclass_display()} - {'10' if p.rateclass == 'free' else '50' if
p.rateclass == 'paid1' else '100' if p.rateclass == 'paid2' else '200' if p.rateclass == 'paid3' else '0'} Гб/мес</b>

🇫🇮Финляндия (Хельсинки): {"<code>"+p.vpn_access_url+"</code>" if p.vpn_access_url else "<i>получить настройки, нажмите /start </i>"}

🇺🇸США (Нью-Йорк): {"<code>"+p.vpn_url_ny+"</code>" if p.vpn_url_ny else "<i>получить настройки, нажмите /start </i>"}

🇰🇿Казахстан (Алматы): {"<code>"+p.vpn_url_almaty+"</code>" if p.vpn_url_almaty else "<i>получить настройки, нажмите /start </i>"}

🇷🇺Россия (СПб): {"<code>"+p.vpn_url_spb+"</code>" if p.vpn_url_spb else "<i>получить настройки, нажмите /start </i>"}

<i>Нажмите на содержимое и оно автоматически скопируется в буфер обмена.
Для получения настроек для других регионов (Финляндия, Казахстан или Россия), нажмите /start. </i>
    '''
    return vpn_settings


def show_vpn_stats(p):
    get_stats = get_stats_api(p)
    data_limit, used_traffic, used_traffic_mb = get_stats
    vpn_stats = f'''
Тариф: {p.get_rateclass_display()}
Всего трафика в мес: {data_limit} Гб
Использовано: {f'{used_traffic} Гб' if used_traffic > 1 else f'{used_traffic_mb} Мб'}
Осталось: {data_limit-used_traffic} Гб

Для смены тарифа обращаться к
'''
    return vpn_stats


def show_admin_stats(message, bot, bot_admin):
    server_ip = ''
    if message.chat.id == bot_admin:
        url = 'https://ifconfig.me/ip'
        response = requests.get(url)
        if response.status_code == 200:
            server_ip = response.text
        else:
            if response.status_code == 200:
                response = requests.get('http://api.ipify.org')
                server_ip = response.text
        show_text = f'''
Привет, <i>Admin</i>!

Пользователей: <b>{Accounts.objects.all().count()}</b>
Personal: <b>{Accounts.objects.filter(rateclass='free', has_access=True).count()}</b>
Plus: <b>{Accounts.objects.filter(rateclass='paid1').count()}</b>
Pro: <b>{Accounts.objects.filter(rateclass='paid2').count()}</b>
Premium: <b>{Accounts.objects.filter(rateclass='paid3').count()}</b>
Без доступа: <b>{Accounts.objects.filter(has_access=False).count()}</b>

    '''

        return show_text, server_ip


friends_password = 'friends_password'
