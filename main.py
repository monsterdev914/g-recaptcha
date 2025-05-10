import os
import json
import random
import string
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Union

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
            "Content-Type": "application/x-www-form-urlencoded"
        }

class CookieManager:
    """Handles cookie operations"""
    def __init__(self, config: Config):
        self.config = config

    def get_cookies(self, username: str) -> Optional[Dict]:
        """Get stored cookies for a username"""
        cookies = [item for item in self.config.logined_cookies if item['username'] == username]
        return cookies[0] if cookies else None

    def add_cookies(self, cookie: Dict, username: str, proxy: str) -> None:
        """Add new cookies to storage"""
        with open('cookies.json', 'r') as f:
            data = json.load(f)
        
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
            self.session.proxies.update(stored_cookies['proxy'])
        else:
            cookies = self.login()
            if not cookies:
                print("Failed to get cookies")
                return
            self.cookie_manager.add_cookies(cookies, self.config.username, self.proxy)

        if not cookies or "Vistos_sid" not in cookies:
            print("Session initialization failed")
            return

        try:
            # First form submission
            form_data1 = {
                "lang": "PT",
                "nacionalidade": "CPV",
                "pais_residencia": "CPV",
                "tipo_passaporte": "01",
                "copia_pedido": "null",
                "cb_pais_residencia": "CPV",
                "cb_tipo_passaporte": "01",
                "cb_qt_dias": "SCH",
                "cb_trab_sazonal": "S",
                "tipo_visto": "CT",
                "tipo_visto_desc": "VISTO DE CURTA DURAÇÃO - TRABALHO SAZONAL",
                "class_visto": "SCH",
                "cod_estada": "01",
                "id_visto_doc": "2"
            }

            self.session.cookies.update(cookies)
            response = self.session.post(
                "https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",
                data=form_data1,
                allow_redirects=False
            )

            if response.status_code == 403:
                print("Session expired, attempting relogin...")
                new_cookies = self.login()
                if new_cookies:
                    self.cookie_manager.update_cookies(new_cookies, self.config.username, self.proxy)
                    self.session.cookies.update(new_cookies)
                    response = self.session.post(
                        "https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",
                        data=form_data1
                    )

            # Extract form data and submit second form
            self._handle_second_form(response)

        except Exception as e:
            print(f"Form submission error: {str(e)}")

    def _handle_second_form(self, first_response: requests.Response) -> None:
        """Handle second form submission"""
        soup = BeautifulSoup(first_response.text, 'html.parser')
        
        # Extract required form fields
        form_data2 = self._extract_form_fields(soup)
        
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
            data=form_data2,
            files=files,
            allow_redirects=False
        )

        self._handle_form_response(response)

    def _extract_form_fields(self, soup: BeautifulSoup) -> Dict:
        """Extract form fields from the first form response"""
        # Implementation of form field extraction
        # This would contain the logic to extract all the necessary fields
        pass

    def _handle_form_response(self, response: requests.Response) -> None:
        """Handle the response from the second form submission"""
        if response.status_code == 200:
            error_td = BeautifulSoup(response.text, 'html.parser').find('td', class_='texto_erro')
            if error_td:
                print(f"Form error: {error_td.get_text(strip=True)}")
                return
        elif response.status_code == 302:
            print(f"Form submitted successfully: {response.headers['Location']}")
            # Handle successful submission
        else:
            print(f"Form submission failed: {response.status_code}")

def main():
    """Main entry point"""
    config = Config()
    application = VisaApplication(config)
    application.submit_form()

if __name__ == "__main__":
    main()