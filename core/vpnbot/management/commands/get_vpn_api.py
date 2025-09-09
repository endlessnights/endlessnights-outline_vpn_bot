import os
import re
from ...models import Accounts
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from outline_vpn.outline_vpn import OutlineVPN

try:
    api_url = os.environ['API_URL_OUTLINE_BOT']
    api_url_spb = os.environ['api_url_spb']
    api_url_almaty = os.environ['api_url_almaty']
    api_url_ny = os.environ['api_url_ny']
    cert_sha = os.environ['CERT_SHA256_OUTLINE_BOT']
    cert_sha_spb = os.environ['cert_sha256_spb']
    cert_sha_almaty = os.environ['cert_sha256_almaty']
    cert_sha_ny = os.environ['cert_sha256_ny']
    client_fin = OutlineVPN(api_url=api_url,
                        cert_sha256=cert_sha)
    client_spb = OutlineVPN(api_url=api_url_spb,
                            cert_sha256=cert_sha_spb)
    client_almaty = OutlineVPN(api_url=api_url_almaty,
                            cert_sha256=cert_sha_almaty)
    client_ny = OutlineVPN(api_url=api_url_ny,
                               cert_sha256=cert_sha_ny)
except KeyError as e:
    print(f'NO API_URL or CERT_SHA256 for OUTLINE BOT in OS ENVIRON: {e}')


def extract_tg_id(input_string):
    try:
        match = re.search(r'tg-(\d+)-id', input_string)

        if match:
            tg_id_value = match.group(1)
            return tg_id_value
        else:
            return None
    except Exception as e:
        print(f'extract_tg_id: {e}')


data_limits = {
    'free': 10 * 1000 * 1000 * 1000,  # 10 GB/month
    'paid1': 50 * 1000 * 1000 * 1000,  # 50 GB/month
    'paid2': 100 * 1000 * 1000 * 1000,  # 100 GB/month
    'paid3': 200 * 1000 * 1000 * 1000,  # 200 GB/month
}


def get_settings_api(username, rateclass, country_tag):
    user_tgid = extract_tg_id(username)
    p = Accounts.objects.get(tgid=user_tgid)
    print(user_tgid)
    #   Проверяем наличие tgid в имени ключа в базе Outline VPN
    if country_tag == 'fin':
        for key in client_fin.get_keys():
            try:
                if user_tgid in extract_tg_id(key.name):
                    p.vpn_key_id = key.key_id
                    p.vpn_key_name = key.name
                    p.vpn_key_password = key.password
                    p.vpn_key_port = key.port
                    p.vpn_access_url = key.access_url
                    p.save()
                    get_data_limit_diplay = int(float(key.data_limit) / (1000 ** 3))
                    return (p.vpn_key_id, p.vpn_key_name, p.vpn_key_password, p.vpn_key_port, p.vpn_access_url,
                            get_data_limit_diplay)
            except Exception as e:
                print(e)
        print('No key found for fin')
        #   Если в базе Outline VPN tgid не входит в какой-либо key.name, создаем новый ключ
        new_key = client_fin.create_key(key_name=username)
        get_data_limit = data_limits.get(rateclass, data_limits['free'])
        client_fin.add_data_limit(new_key.key_id, get_data_limit)
        get_data_limit_diplay = int(float(get_data_limit) / (1000 ** 3))

        return (new_key.key_id, new_key.name, new_key.password, new_key.port, new_key.access_url,
                get_data_limit_diplay)
    elif country_tag == 'spb':
        for key in client_spb.get_keys():
            try:
                if user_tgid in extract_tg_id(key.name):
                    p.vpn_id_spb = key.key_id
                    p.vpn_name_spb = key.name
                    p.vpn_password_spb = key.password
                    p.vpn_port_spb = key.port
                    p.vpn_url_spb = key.access_url
                    p.save()
                    get_data_limit_diplay = int(float(key.data_limit) / (1000 ** 3))
                    return (p.vpn_id_spb, p.vpn_name_spb, p.vpn_password_spb, p.vpn_port_spb, p.vpn_url_spb,
                            get_data_limit_diplay)
            except Exception as e:
                print(e)
        print('No key found for spb')
        #   Если в базе Outline VPN tgid не входит в какой-либо key.name, создаем новый ключ
        new_key = client_spb.create_key(key_name=username)
        get_data_limit = data_limits.get(rateclass, data_limits['free'])
        client_spb.add_data_limit(new_key.key_id, get_data_limit)
        get_data_limit_diplay = int(float(get_data_limit) / (1000 ** 3))

        return (new_key.key_id, new_key.name, new_key.password, new_key.port, new_key.access_url,
                get_data_limit_diplay)
    elif country_tag == 'almaty':
        for key in client_almaty.get_keys():
            try:
                if user_tgid in extract_tg_id(key.name):
                    p.vpn_id_almaty = key.key_id
                    p.vpn_name_almaty = key.name
                    p.vpn_password_almaty = key.password
                    p.vpn_port_almaty = key.port
                    p.vpn_url_almaty = key.access_url
                    p.save()
                    get_data_limit_diplay = int(float(key.data_limit) / (1000 ** 3))
                    return (p.vpn_id_almaty, p.vpn_name_almaty, p.vpn_password_almaty, p.vpn_port_almaty, p.vpn_url_almaty,
                            get_data_limit_diplay)
            except Exception as e:
                print(e)
        print('No key found for almaty')
        #   Если в базе Outline VPN tgid не входит в какой-либо key.name, создаем новый ключ
        new_key = client_almaty.create_key(key_name=username)
        get_data_limit = data_limits.get(rateclass, data_limits['free'])
        client_almaty.add_data_limit(new_key.key_id, get_data_limit)
        get_data_limit_diplay = int(float(get_data_limit) / (1000 ** 3))

        return (new_key.key_id, new_key.name, new_key.password, new_key.port, new_key.access_url,
                get_data_limit_diplay)
    elif country_tag == 'ny':
        for key in client_ny.get_keys():
            try:
                if user_tgid in extract_tg_id(key.name):
                    p.vpn_id_ny = key.key_id
                    p.vpn_name_ny = key.name
                    p.vpn_password_ny = key.password
                    p.vpn_port_ny = key.port
                    p.vpn_url_ny = key.access_url
                    p.save()
                    get_data_limit_diplay = int(float(key.data_limit) / (1000 ** 3))
                    return (p.vpn_id_ny, p.vpn_name_ny, p.vpn_password_ny, p.vpn_port_ny, p.vpn_url_ny,
                            get_data_limit_diplay)
            except Exception as e:
                print(e)
        print('No key found for ny')
        #   Если в базе Outline VPN tgid не входит в какой-либо key.name, создаем новый ключ
        new_key = client_ny.create_key(key_name=username)
        get_data_limit = data_limits.get(rateclass, data_limits['free'])
        client_ny.add_data_limit(new_key.key_id, get_data_limit)
        get_data_limit_diplay = int(float(get_data_limit) / (1000 ** 3))

        return (new_key.key_id, new_key.name, new_key.password, new_key.port, new_key.access_url,
                get_data_limit_diplay)



def get_stats_api(p):
    for key in client_fin.get_keys():
        if p.tgid in extract_tg_id(key.name):
            data_limit = key.data_limit / (1000 ** 3)
            try:
                used_traffic = key.used_bytes / (1000 ** 3)
                used_traffic = round(used_traffic, 1)
                used_traffic_mb = key.used_bytes / (1000 ** 2)
                used_traffic_mb = round(used_traffic_mb, 2)

                return data_limit, used_traffic, used_traffic_mb
            except Exception as e:
                print(f'get_stats_api: {timezone.now()} {e}')
                return data_limit, 0, 0


#   Testing
def change_rateclass_api(user_tgid, new_rateclass):
    p = Accounts.objects.get(tgid=user_tgid)
    user_tgid = extract_tg_id(p.vpn_key_name)
    try:
        for key in client_fin.get_keys():
            if user_tgid in extract_tg_id(key.name) and new_rateclass in data_limits:
                print(new_rateclass)
                data_limit = data_limits[new_rateclass]
                client_fin.add_data_limit(key.key_id, data_limit)
                p.rateclass = new_rateclass
                p.save()
            else:
                print('def change_fin: Неправильный ввод')
        for key in client_spb.get_keys():
            try:
                if user_tgid in extract_tg_id(key.name) and new_rateclass in data_limits:
                    print(new_rateclass)
                    data_limit = data_limits[new_rateclass]
                    client_spb.add_data_limit(key.key_id, data_limit)
                else:
                    print('def change_spb: Неправильный ввод')
            except Exception as e:
                print(e)
        for key in client_almaty.get_keys():
            try:
                if user_tgid in extract_tg_id(key.name) and new_rateclass in data_limits:
                    print(new_rateclass)
                    data_limit = data_limits[new_rateclass]
                    client_almaty.add_data_limit(key.key_id, data_limit)
                else:
                    print('def change_almaty: Неправильный ввод')
            except Exception as e:
                print(e)
        for key in client_ny.get_keys():
            try:
                if user_tgid in extract_tg_id(key.name) and new_rateclass in data_limits:
                    print(new_rateclass)
                    data_limit = data_limits[new_rateclass]
                    client_ny.add_data_limit(key.key_id, data_limit)
                else:
                    print('def change_ny: Неправильный ввод')
            except Exception as e:
                print(e)
        return p.get_rateclass_display()
    except Exception as e:
        return e
