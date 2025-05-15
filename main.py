import os
import json
import random
import string
from datetime import date, datetime, timedelta
import time
from typing import Dict, List, Optional, Union

from numpy import float32
import requests
from bs4 import BeautifulSoup
import capsolver
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class to store all settings"""

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.website_url = os.getenv("WEBSITE_URL")
        self.website_key = os.getenv("WEBSITE_KEY")
        self.username = os.getenv("USER_NAME")
        self.password = os.getenv('PASSWORD')

        # Load data files
        with open('personal_data.json', 'r', encoding='utf-8') as f:
            self.pessoas = json.load(f)
        with open('proxy_list.json', 'r') as f:
            self.proxy_list = json.load(f)
        with open('cookies.json', 'r', encoding='utf-8') as f:
            self.logined_cookies = json.load(f)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",

        }


class CookieManager:
    """Handles cookie operations"""

    def __init__(self, config: Config):
        self.config = config

    def get_cookies(self, username: str) -> Optional[Dict]:
        """Get stored cookies for a username"""
        cookies = [
            item for item in self.config.logined_cookies if item['username'] == username]
        return cookies[0] if cookies else None

    def add_cookies(self, cookie: Dict, username: str, proxy: str) -> None:
        """Add new cookies to storage"""
        with open('cookies.json', 'r') as f:
            data = json.load(f)

        # Add user_consent to cookie dictionary
        cookie['user_consent'] = '1'

        new_data = {
            'username': username,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cookie': cookie,
            'proxy': proxy
        }
        data.append(new_data)

        with open('cookies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def update_cookies(self, cookie: Dict, username: str, proxy: str) -> None:
        """Update existing cookies"""
        with open('cookies.json', 'r') as f:
            data = json.load(f)

        for item in data:
            if item['username'] == username:
                item.update({
                    'cookie': cookie,
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'proxy': proxy
                })

        with open('cookies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)


class VisaApplication:
    """Main visa application handler"""

    def __init__(self, config: Config):
        self.config = config
        self.cookie_manager = CookieManager(config)
        self.session = requests.Session()
        self.session.headers.update(config.headers)

        # Load form data from JSON files
        with open('form1.json', 'r', encoding='utf-8') as f:
            self.form_data1 = json.load(f)
        # with open('form2.json', 'r', encoding='utf-8') as f:
        #     self.form_data2 = json.load(f)

        # Check for stored cookies first
        stored_cookies = self.cookie_manager.get_cookies(self.config.username)
        if stored_cookies:
            stored_data = stored_cookies
            self.session.cookies.update(stored_data['cookie'])
            self.proxy = stored_data['proxy']
        else:
            self.proxy = random.choice(config.proxy_list)

        self.session.proxies.update({
            "http": self.proxy,
            'https': self.proxy
        })

    def login(self) -> Optional[Dict]:
        """Handle login process"""
        capsolver.api_key = self.config.api_key
        try:
            solution = capsolver.solve({
                "type": "ReCaptchaV2Task",
                "websiteURL": self.config.website_url,
                "websiteKey": self.config.website_key,
                "proxy": self.proxy
            })

            if 'gRecaptchaResponse' not in solution:
                print("CAPTCHA solution failed")
                return None

            payload = {
                "username": self.config.username,
                "password": self.config.password,
                "rgpd": "Y",
                "language": "PT",
                "captchaResponse": solution["gRecaptchaResponse"]
            }
            response = self.session.post(
                "https://pedidodevistos.mne.gov.pt/$J@5Yg0RAhCxKgAhgfwtTouVMlnWPHDd_ubZzU6uSScB8ZmN3SlXxLKGpc",
                data=payload
            )
            if response.status_code == 200:
                response_json = response.json()
                if response_json["type"] == 'error':
                    print(f'Error: {response_json["description"]}')
                    return None
                return self.session.cookies.get_dict()

            print(f"Login failed: {response.status_code}")
            return None

        except Exception as e:
            print(f"Login error: {str(e)}")
            return None

    def submit_form(self) -> None:
        """Handle form submission process"""
        print("Starting form submission...")

        # Get or create cookies
        stored_cookies = self.cookie_manager.get_cookies(self.config.username)
        if stored_cookies:
            cookies = stored_cookies['cookie']
            self.session.proxies.update({
                "http": stored_cookies['proxy'],
                'https': stored_cookies['proxy']
            })
        else:
            cookies = self.login()
            if not cookies:
                print("Failed to get cookies")
                return
            self.cookie_manager.add_cookies(
                cookies, self.config.username, self.proxy)

        if not cookies or "Vistos_sid" not in cookies:
            print("Session initialization failed")
            return

        try:
            self.session.cookies.update(cookies)
            response = self.session.post(
                "https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",
                data=self.form_data1,
            )
            if response.status_code == 403:
                print("Session expired, attempting relogin...")
                new_cookies = self.login()
                if new_cookies:
                    self.cookie_manager.update_cookies(
                        new_cookies, self.config.username, self.proxy)
                    self.session.cookies.update(new_cookies)
                    response = self.session.post(
                        "https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",
                        data=self.form_data1
                    )

            with open('form1.html', 'w', encoding='utf-8') as f:
                f.write(response.text)

            self._handle_second_form(response)

        except Exception as e:
            print(f"Form submission error: {str(e)}")

    def _handle_second_form(self, first_response: requests.Response) -> None:
        """Handle second form submission"""
        try:
            soup = BeautifulSoup(first_response.text, 'html.parser')

            # Extract required form fields with error handling
            token_input = soup.find(
                'input', attrs={'name': '__RequestVerificationToken'})
            if not token_input:
                print("Error: Could not find CSRF token in the response")
                return

            csrf_token = token_input.get('value')
            if not csrf_token:
                print("Error: CSRF token value is empty")
                return

            f0 = soup.find('input', attrs={'name': 'f0'}).get('value')
            f1 = soup.find('input', attrs={'name': 'f1'}).get('value')
            f3 = soup.find('input', attrs={'name': 'f3'}).get('value')
            f4 = soup.find('input', attrs={'name': 'f4'}).get('value')
            f9 = soup.find('input', attrs={'name': 'f9'}).get('value')
            f14 = soup.find('input', attrs={'name': 'f14'}).get('value')

            select_tag = soup.find('select', {'name': 'f7sf1'})
            selected_option = select_tag.find('option', selected=True)
            f7sf1 = selected_option['value']

            select_tag = soup.find('select', {'name': 'f29'})
            selected_option = select_tag.find('option', selected=True)
            f29 = selected_option['value']

            select_tag = soup.find('select', {'name': 'f13'})
            selected_option = select_tag.find('option', selected=True)
            f13 = selected_option['value']
            form2_data = {
                "lang": "PT",
                "txtHuman": "",
                "__RequestVerificationToken": csrf_token,
                "RGPDAccepted": "",
                "posto_representacao": "null",
                "f0sf1": "5088",
                "f1": f1,
                "f2": "Angela Sonia Ribeiro Furtado",
                "f3": f3,
                "f4": f4,
                "f6": "Santiago, Cabo Verde",
                "f6sf1": "CPV",
                "f7sf1": f7sf1,
                "f8": "CPV",
                "f9": f9,
                "f10": "1",
                "txtApelidoPaternal": "",
                "txtNomePaternal": "",
                "txtEnderecoPaternal": "",
                "txtTelefonePaternal": "",
                "txtEmailPaternal": "",
                "cmbNacionalidadePaternal": "",
                "f5": "",
                "f13": f13,
                "f14": f14,
                "f16": "2024/04/15",
                "f17": "2029/04/14",
                "f15": "CPV",
                "f43": "",
                "f43sf2": "",
                "f43sf3": "",
                "f43sf4": "",
                "f43sf5": "",
                "f43sf6": "",
                "f0": f0,
                "f45": "PRAIA",
                "f46": "9951033",
                "f18sf1": "",
                "f18sf2": "",
                "f18sf3": "",
                "f19": "14",
                "f20sf1": "Irmaos Correia",
                "f20sf2": "Achada Grande Frente",
                "f29": f29,
                "f29sf2": "",
                "f29sf3": "",
                "txtInfoMotEstada": "Ferias",
                "em_destino_1": "PRT",
                "em_destino_2": "",
                "em_destino_3": "",
                "f32": "PRT",
                "f24": "1",
                "f25": "15",
                "f30": "2025/05/17",
                "f31": "2025/06/06",
                "cmbImpressoesDigitais": "N",
                "dataImpressoesDigitais": "",
                "numVinImpressoesDigitais": "",
                "f27": "N",
                "f27sf2": "",
                "f27sf3": "",
                "cmbReferencia": "individual",
                "f34": "HOTEL LISBON",
                "f34sf3": "",
                "f34sf2": "AVENIDA LISBON",
                "f34sf4": "",
                "f34sf5": "1",
                "cmbDespesasRequerente_1": "1",
                "cmbDespesasRequerente_2": "",
                "cmbDespesasRequerente_3": "",
                "cmbDespesasRequerente_4": "",
                "cmbDespesasPatrocinador_1": "2",
                "cmbDespesasPatrocinador_2": "",
                "cmbDespesasPatrocinador_3": "",
                "cmbDespesasPatrocinador_4": "",
                "tipo_visto": self.form_data1['tipo_visto'],
                "tipo_visto_desc": self.form_data1['tipo_visto_desc'],
                "class_visto": self.form_data1['class_visto'],
                "cod_estada": self.form_data1['cod_estada'],
                "id_visto_doc": self.form_data1['id_visto_doc'],
                "tipo_passaporte": self.form_data1['tipo_passaporte'],
                "nacionalidade": self.form_data1['nacionalidade'],
                "pais_residencia": self.form_data1['pais_residencia'],
                "f_date_c": "",
                "cmbPeriodo": ""
            }
            # Submit second form
            files = {
                'foto': ('', b''),
                'file1': ('', b''),
                'file2': ('', b''),
                'file3': ('', b''),
                'file4': ('', b'')
            }

            response = self.session.post(
                "https://pedidodevistos.mne.gov.pt/VistosOnline/ScheduleController",
                data=form2_data,
                files=files,
                allow_redirects=False
            )

            self._handle_form_response(response)

        except Exception as e:
            print(f"Error in second form handling: {str(e)}")
            # Save the response for debugging
            with open('error_response.html', 'w', encoding='utf-8') as f:
                f.write(first_response.text)

    def _handle_form_response(self, response: requests.Response) -> None:
        """Handle the response from the second form submission"""
        if response.status_code == 200:
            error_td = BeautifulSoup(response.text, 'html.parser').find(
                'td', class_='texto_erro')
            if error_td:
                print(f"Form error: {error_td.get_text(strip=True)}")
                return
        elif response.status_code == 302:
            redirect_url = response.headers['Location']
            print(redirect_url)
            stored_cookies = self.cookie_manager.get_cookies(
                self.config.username)
            if stored_cookies and 'cookie' in stored_cookies:
                self.session.cookies.update(stored_cookies['cookie'])
            res = self.session.get(
                f'https://pedidodevistos.mne.gov.pt/VistosOnline/{redirect_url}')
            print(res.text)

            # with open('test1.html', 'w', encoding='utf-8') as f:
            #     f.write(res.text)
            # self.get_available_days(3018)

        else:
            print(f"Form submission failed: {response.status_code}")

    def get_busy_periods(self, date_scheduling: str) -> str:
        """Get busy periods for a specific date"""
        url = f"https://pedidodevistos.mne.gov.pt/VistosOnline/getPeriodosOcupados?id_posto=3018&data_agendamento={date_scheduling}"
        response = self.session.get(url)
        # retern value is periodos_ocupados='4,5,7,1,2,3,6,9,10,11,12,13,14,';
        res_text = response.text
        periodos_ocupados = res_text.split('=')[1].strip("'")
        return periodos_ocupados.split(',')

    def get_available_days(self, id_posto: str):
        """Get available days for a specific posto"""
        url = f"https://pedidodevistos.mne.gov.pt/VistosOnline/gettime?id_posto={id_posto}"
        response = self.session.get(url)
        res_text = response.text
        # return value is SPECIAL_DAYS[2025] = new Array();SPECIAL_DAYS[2026] = new Array();SPECIAL_DAYS[2025][4] = new Array(15,16,19,20,26);SPECIAL_DAYS[2025][5] = new Array('18');SPECIAL_DAYS[2025][6] = new Array('31');SPECIAL_DAYS[2025][7] = new Array('1');
        # That is javascrpt code, we need to parse it
        # what is the result in python?
        # result is a dictionary
        print(res_text)


def main():
    """Main entry point"""
    config = Config()
    application = VisaApplication(config)
    application.submit_form()


if __name__ == "__main__":
    main()
