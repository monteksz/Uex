import requests
from colorama import Fore, Style, init
import json
import time
import threading

init(autoreset=True)

def nama():
    art_lines = [
        "   _____         _   _  _____ _______ _    _         _______     __",
        "  / ____|  /\\   | \\ | |/ ____|__   __| |  | |  /\\   |  __ \\ \\   / /",
        " | (___   /  \\  |  \\| | |       | |  | |  | | /  \\  | |__) \\ \\_/ / ",
        "  \\___ \\ / /\\ \\ | . ` | |       | |  | |  | |/ /\\ \\ |  _  / \\   /  ",
        "  ____) / ____ \\| |\\  | |____   | |  | |__| / ____ \\| | \\ \\  | |   ",
        " |_____/_/    \\_\\_| \\_|\\_____|  |_|   \\____/_/    \\_\\_|  \\_\\ |_|   ",
        "                                                                   ",
        "                                                                   "
    ]

    max_length = max(len(line) for line in art_lines)

    border = '#' * (max_length + 4)

    print(border)
    for line in art_lines:
        print(f"# {line} #")
    print(border)

    print(f"{Fore.GREEN}Terima kasih Telah Menggunakan Bot dari Monteksz X Sanctuary Jangan Lupa Bintangnya ^^{Fore.RESET}")
    print(f"{Fore.GREEN}Cek Bot Lainnya di https://github.com/monteksz{Fore.RESET}")
    print(f"{Fore.GREEN}=================================================================================================={Fore.RESET}")

nama()

def login(init_data, account_number):
    payload_login = {
        'init_data': init_data,
        'referrer': ''
    }

    url_login = 'https://zejlgz.com/api/login/tg'
    response_login = requests.post(url_login, json=payload_login)

    if response_login.status_code == 200:
        data_login = response_login.json()
        if data_login['code'] == 0 and 'token' in data_login['data'] and 'token' in data_login['data']['token']:
            token = data_login['data']['token']['token']
            print(Fore.GREEN + f'[Akun Ke-{account_number}] Token Berhasil di Dapatkan: ' + token + Style.RESET_ALL)
            return token
        else:
            print(Fore.RED + f'[Akun Ke-{account_number}] Login Gagal: Token tidak ditemukan.' + Style.RESET_ALL)
    else:
        print(Fore.RED + f'[Akun Ke-{account_number}] Permintaan Gagal dengan Status Kode: {response_login.status_code}' + Style.RESET_ALL)
    return None

def check_assets(token, account_number):
    payload_assets = {
        'token': token
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Origin': 'https://ueex-mining-be9.pages.dev',
        'Pragma': 'no-cache',
        'Referer': 'https://ueex-mining-be9.pages.dev/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    url_assets = 'https://zejlgz.com/api/user/assets'
    
    response_assets = requests.post(url_assets, json=payload_assets, headers=headers)
    
    if response_assets.status_code == 200:
        data_assets = response_assets.json()
        if data_assets['code'] == 0:
            ue_amount = data_assets['data'].get('ue', {}).get('amount', 0)
            usdt_amount = data_assets['data'].get('usdt', {}).get('amount', 0)
            diamond_amount = data_assets['data'].get('diamond', {}).get('amount', 0)
            
            return ue_amount, usdt_amount, diamond_amount
        else:
            print(Fore.RED + f'[Akun Ke-{account_number}] Gagal mendapatkan data aset: ' + data_assets.get('message', 'Tidak diketahui') + Style.RESET_ALL)
    else:
        print(Fore.RED + f'[Akun Ke-{account_number}] Permintaan Gagal dengan Status Kode: {response_assets.status_code}' + Style.RESET_ALL)
    return None, None, None

def check_drops(token, account_number):
    payload_scene_info = {
        'token': token
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    }
    url_scene_info = 'https://zejlgz.com/api/scene/info'
    
    response_scene_info = requests.post(url_scene_info, json=payload_scene_info, headers=headers)
    
    if response_scene_info.status_code == 200:
        data_scene_info = response_scene_info.json()
        if data_scene_info['code'] == 0:
            reward_claimed = False
            for scene in data_scene_info['data']:
                if scene['eggs'] is not None:
                    for egg in scene['eggs']:
                        if egg['flag'] == 0:
                            claim_drop(token, egg, account_number)
                            reward_claimed = True
            if not reward_claimed:
                print(Fore.CYAN + f'[Akun Ke-{account_number}] Waiting For Reward...' + Style.RESET_ALL)
        else:
            print(Fore.RED + f'[Akun Ke-{account_number}] Gagal mendapatkan data scene info: ' + data_scene_info.get('message', 'Tidak diketahui') + Style.RESET_ALL)
    else:
        print(Fore.RED + f'[Akun Ke-{account_number}] Permintaan Gagal dengan Status Kode: {response_scene_info.status_code}' + Style.RESET_ALL)

def claim_drop(token, egg, account_number):
    payload_egg_reward = {
        'token': token,
        'egg_uid': egg['uid']
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    }
    url_egg_reward = 'https://zejlgz.com/api/scene/egg/reward'
    
    response_egg_reward = requests.post(url_egg_reward, json=payload_egg_reward, headers=headers)
    
    if response_egg_reward.status_code == 200:
        data_egg_reward = response_egg_reward.json()
        if data_egg_reward['code'] == 0:
            if egg['a_type'] == 'ue':
                print(Fore.YELLOW + f'[Akun Ke-{account_number}] UE Reward Berhasil Diklaim ({egg["amount"]})', end='')
            elif egg['a_type'] == 'usdt':
                print(Fore.GREEN + f'[Akun Ke-{account_number}] USDT Reward Berhasil Diklaim ({egg["amount"]})', end='')
            
            ue_amount, usdt_amount, diamond_amount = check_assets(token, account_number)  # Dapatkan saldo terbaru setelah klaim
            print(Fore.MAGENTA + f' | Saldo Terbaru' + Style.RESET_ALL + 
                  Fore.YELLOW + f' UE: {ue_amount}' + Style.RESET_ALL + ' | ' + 
                  Fore.GREEN + f'USDT: {usdt_amount}' + Style.RESET_ALL + ' | ' + 
                  Fore.BLUE + f'Diamond: {diamond_amount}' + Style.RESET_ALL)
        else:
            print(Fore.RED + f'[Akun Ke-{account_number}] Gagal mengklaim egg reward: ' + data_egg_reward.get('message', 'Tidak diketahui') + Style.RESET_ALL)
            print("Response data:", data_egg_reward)
    else:
        print(Fore.RED + f'[Akun Ke-{account_number}] Permintaan Gagal dengan Status Kode: {response_egg_reward.status_code}' + Style.RESET_ALL)
        print("Response text:", response_egg_reward.text)

def process_account(init_data, account_number):
    token = login(init_data, account_number)
    if token:
        check_assets(token, account_number)

    if token:
        start_time = time.time()
        waiting_for_reward_displayed = False
        while True:
            current_time = time.time()
            if current_time - start_time >= 480:  # 8 menit = 480 detik
                token = login(init_data, account_number)
                if token:
                    check_assets(token, account_number)
                start_time = current_time
            
            reward_claimed = False
            payload_scene_info = {
                'token': token
            }
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            }
            url_scene_info = 'https://zejlgz.com/api/scene/info'
            
            response_scene_info = requests.post(url_scene_info, json=payload_scene_info, headers=headers)
            
            if response_scene_info.status_code == 200:
                data_scene_info = response_scene_info.json()
                if data_scene_info['code'] == 0:
                    for scene in data_scene_info['data']:
                        if scene['eggs'] is not None:
                            for egg in scene['eggs']:
                                if egg['flag'] == 0:
                                    claim_drop(token, egg, account_number)
                                    reward_claimed = True
                                    waiting_for_reward_displayed = False  # Reset flag
                else:
                    print(Fore.RED + f'[Akun Ke-{account_number}] Gagal mendapatkan data scene info: ' + data_scene_info.get('message', 'Tidak diketahui') + Style.RESET_ALL)
            else:
                print(Fore.RED + f'[Akun Ke-{account_number}] Permintaan Gagal dengan Status Kode: {response_scene_info.status_code}' + Style.RESET_ALL)

            if not reward_claimed and not waiting_for_reward_displayed:
                print(Fore.CYAN + f'[Akun Ke-{account_number}] Waiting For Reward...' + Style.RESET_ALL)
                waiting_for_reward_displayed = True

if __name__ == "__main__":
    with open('akun.txt', 'r') as file:
        accounts = file.readlines()

    threads = []
    for index, account in enumerate(accounts):
        account = account.strip()
        if account:
            thread = threading.Thread(target=process_account, args=(account, index + 1))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()
