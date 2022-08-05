# import packages and required params
import getpass
import requests
from pathlib import Path
from platform import system
from os.path import exists
from bs4 import BeautifulSoup as bs
import sys

def verifyCredentials(username: str, password:str) -> bool:

        cas_url = 'https://cmems-cas.cls.fr/cas/login'
        session = requests.session()
        soup = bs(session.get(cas_url).text, features='html.parser')
        login_ticket = soup.find('input', {'name':'lt'})['value']
        json = {
                'lt':login_ticket,
                '_eventId':'submit',
                'username':username,
                'password':password
        }
        soup = bs(session.post(cas_url, data=json).text, features='html.parser')
        status = soup.find('div', {'class':'success'})

        return status != None


username = input("Enter your Copernicus Marine Service username: ")
password = getpass.getpass("Enter your password: ")

if not verifyCredentials(username, password):
        print("Wrong credentials.")
        sys.exit()

HOME = Path.home()
OPeNDAP_SERVERS = ["my.cmems-du.eu", "nrt.cmems-du.eu"]

# créer fichier _netrc
netrc_file = "_netrc" if system() == "Windows" else ".netrc"
if not exists(netrc_file):
        with open(netrc_file, "a") as file:
            for server in OPeNDAP_SERVERS:
                file.write(f"\n machine {server} login {username} password {password}")


# créer fichier .dodsrc
dodsrc_file = HOME / ".dodsrc"
cookies_file = HOME / ".cookies"
if not exists(dodsrc_file):
        with open(dodsrc_file, "a") as file:
            file.write(f"HTTP.NETRC={netrc_file}\nHTTP.COOKIEJAR={cookies_file}")
