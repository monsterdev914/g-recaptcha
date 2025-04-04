import os  
import json  
import random  
import requests  
from dotenv import load_dotenv  
from bs4 import BeautifulSoup  
import capsolver  
load_dotenv()  



with open('personal_data.json', 'r', encoding='utf-8') as f:  
    pessoas = json.load(f)
# Load proxy list  
with open('proxy_list.json', 'r') as f:  
    proxy_list = json.load(f)
headers = {  
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  
}  
# Load environment variables  
api_key = os.getenv("API_KEY")  
website_url = os.getenv("WEBSITE_URL")  
website_key = os.getenv("WEBSITE_KEY")  
username = os.getenv("USER_NAME")  
password = os.getenv('PASSWORD')  
proxy = random.choice(proxy_list)

proxies = {  
    "http": 'http://user-john123_F6xyN:Pwd123@pr.u26x17fh.lunaproxy.net:32233',  
}  

def login(api_key, website_url, website_key, username, password, proxies):  
    """Handles user login and returns session cookies."""  
    capsolver.api_key = api_key
    try:  
        # Solve the reCAPTCHA   
        res = requests.get('https://pedidodevistos.mne.gov.pt/VistosOnline/Authentication.jsp', headers=headers, proxies=proxies)
        cookies = res.cookies.get_dict()
        # payload = {
        #     "fwib_dat": "R0VUIC9WaXN0b3NPbmxpbmUvQXV0aGVudGljYXRpb24uanNwIEhUVFAvMS4xDQpIb3N0OiBwZWRpZG9kZXZpc3Rvcy5tbmUuZ292LnB0DQpDb25uZWN0aW9uOiBrZWVwLWFsaXZlDQpzZWMtY2gtdWE6ICJDaHJvbWl1bSI7dj0iMTM0IiwgIk5vdDpBLUJyYW5kIjt2PSIyNCIsICJHb29nbGUgQ2hyb21lIjt2PSIxMzQiDQpzZWMtY2gtdWEtbW9iaWxlOiA/MA0Kc2VjLWNoLXVhLXBsYXRmb3JtOiAiV2luZG93cyINClVwZ3JhZGUtSW5zZWN1cmUtUmVxdWVzdHM6IDENClVzZXItQWdlbnQ6IE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzQuMC4wLjAgU2FmYXJpLzUzNy4zNg0KQWNjZXB0OiB0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS9hdmlmLGltYWdlL3dlYnAsaW1hZ2UvYXBuZywqLyo7cT0wLjgsYXBwbGljYXRpb24vc2lnbmVkLWV4Y2hhbmdlO3Y9YjM7cT0wLjcNClNlYy1GZXRjaC1TaXRlOiBzYW1lLW9yaWdpbg0KU2VjLUZldGNoLU1vZGU6IG5hdmlnYXRlDQpTZWMtRmV0Y2gtVXNlcjogPzENClNlYy1GZXRjaC1EZXN0OiBkb2N1bWVudA0KQWNjZXB0LUVuY29kaW5nOiBnemlwLCBkZWZsYXRlLCBiciwgenN0ZA0KQWNjZXB0LUxhbmd1YWdlOiBlbi1VUyxlbjtxPTAuOQ0KQ29va2llOiBWaXN0b3Nfc2lkPTVDbTQvRStGV3VCRUgybFZHdEhqVzh2dDlydlh3OGtZN0Jkb1hGb3NGTkxqRG9uWlB0N2RxbUlkZGtrU2FJQU5DbnBFSW1VcURRdVhrWWlNc0RnTjAwN0gyMTRtc2htc1JmR1IrUEpvNVZuaDVENG1ZT3lQd2xmV3RxM0hBTVBpOyB1c2VyX2NvbnNlbnQ9MTsgY29va2llc2Vzc2lvbjE9Njc4QjI4NzA5MUVEODhFM0U3QjEzN0JFRUUwMjg0MTc7IHN0YXRzX2dhPUdBMS40LjIwNjMzMzk4ODguMTc0MzY0OTQ4NDsgc3RhdHNfZ2FfQlJKWDBXODBYOD1HUzEuNC4xNzQzNjk0MjA3LjguMS4xNzQzNjk2NDYzLjAuMC4wDQoNCg=="
        # }
        # print(cookies['cookiesession1'])
        # res= requests.post(f'https://pedidodevistos.mne.gov.pt/VistosOnline/Authentication.jsp?cookiesession8341={cookies["cookiesession1"]}', headers=headers, data=payload, proxies=proxies)
        # cookies = res.cookies.get_dict()
        solution = capsolver.solve({  
            "type": "ReCaptchaV2Task",  
            "websiteURL": website_url,  
            "websiteKey": website_key,  
            "proxy": proxies["http"]  
        }) 
        # Check if solution is successful  
        if 'gRecaptchaResponse' not in solution:  
            print("Error: Could not solve reCAPTCHA.")  
            return None 
        payload = {  
            "username": username,  
            "password": password,  
            "rgpd": "Y",  
            "language": "PT",  
            "captchaResponse": solution["gRecaptchaResponse"]  
        }  
        # Make the login POST request  
        res = requests.post("https://pedidodevistos.mne.gov.pt/$J@5Yg0RAhCxKgAhgfwtTouVMlnWPHDd_ubZzU6uSScB8ZmN3SlXxLKGpc",  
                            headers=headers,  
                            data=payload,
                            # cookies=cookies,  
                            proxies=proxies)  

        # Check the response status
        if res.status_code == 200:  
            cookies = res.cookies.get_dict()
            return cookies  
        else:  
            # return cookies
            print(f"Login failed: {res.status_code} - {res.text}")  
            return None  

    except requests.exceptions.RequestException as e:  
        print(f"A request error occurred: {e}")  
        return None  
    except Exception as general_error:  
        print(f"An unexpected error occurred: {general_error}")  
        return None  

def reCaptcha(api_key, website_url, website_key, username, password, proxies, pessoas):  
    """Handles reCAPTCHA solving and form submissions."""  
    cookies = login(api_key, website_url, website_key, username, password, proxies)  
    
    # Check if login attempt was successful  
    if cookies is None:  
        print("Login failed. Exiting reCaptcha function.")  
        return  # Exit if login failed  
    
    # Check if 'Vistos_sid' exists and is empty  
    while "Vistos_sid" not in cookies or cookies["Vistos_sid"] == '':  
        print("Vistos_sid not found or is empty. Logging out...")
        # proxy = random.choice(proxy_list)  
        # proxies = {  
        #     "http": proxy,  
        #     "https": proxy,  
        # }    
        # Attempt to log out
        cookies = login(api_key, website_url, website_key, username, password, proxies)
        # cookies["Vistos_sid"] = 'owaT3sqcST/drWiESvK7nVL74bgA/+BzhScSKWJs+8VP0Tp3pdiuL8tUrpaI6doA8dppTyZYJhImOnLS0tBbbLDW5pUU2gvGU1vbdU2iLieTNQoRqPxmVN8OQkiC2j0U'  
    print("Successfully obtained cookies:", cookies)  

    try:  
        print(f"Received Cookies: {cookies}")  
        form_data1 = {  
            "lang": "ENG",  
            "nacionalidade": "CPV",  
            "pais_residencia": "CPV",  
            "tipo_passaporte": "01",  
            "copia_pedido": "null",  
            "cb_pais_residencia": "CPV",  
            "cb_tipo_passaporte": "01",  
            "cb_qt_dias": "SCH",  
            "cb_trab_sazonal": "O",  
            "cb_motivo_estada_sch": "10",  
            "cb_viaja_reune_turismo": "FAM_N",  
            "tipo_visto": "C",  
            "tipo_visto_desc": "SHORT STAY VISA (SCHENGEN)",  
            "class_visto": "SCH",  
            "cod_estada": "10",  
            "id_visto_doc": "36"  
        }  
        
        # Send the first form submission
        # cookies["Vistos_sid"] = 'owaT3sqcST/drWiESvK7nVL74bgA/+BzhScSKWJs+8VP0Tp3pdiuL8tUrpaI6doA8dppTyZYJhImOnLS0tBbbLDW5pUU2gvGU1vbdU2iLieTNQoRqPxmVN8OQkiC2j0U'
        res1 = requests.post("https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",   
                             cookies=cookies, headers=headers,   
                             proxies=proxies, data=form_data1)
        
        if res1.status_code == 200:  
            print("First form submitted successfully.\n")  
            soup = BeautifulSoup(res1.text, 'html.parser')  
            token_input = soup.find('input', attrs={'name': '__RequestVerificationToken'})  
            request_verification_token = token_input['value'] if token_input else None  
            
            if request_verification_token is None:  
                print("Error: __RequestVerificationToken not found.")  
                return  
            
            print(f'request_verification_token: {request_verification_token}')  
            # Preparing the second form submission data  
            form_data = {  
                'lang': 'ENG',  
                'txtHuman': '',  
                '__RequestVerificationToken': "request_verification_token",  
                'RGPDAccepted': '',  
                'posto_representacao': 'null',  
                'txtApelidoPaternal': '',  
                'txtNomePaternal': '',  
                'txtEnderecoPaternal': '',  
                'txtTelefonePaternal': '',  
                'txtEmailPaternal': '',  
                'cmbNacionalidadePaternal': '',  
                'f5': '',  
                'f0': pessoas[0]['email'],  
                'f0sf1': "5084",  
                'f1': pessoas[0]['nome_completo'],  
                'f2': pessoas[0]['nome_completo'],  
                'f3': pessoas[0]['nome_pai'],  
                'f4': pessoas[0]['nascimento'],  
                'f6': pessoas[0]['local_nascimento'],  
                'f6sf1': "CPV",  
                'f7sf1': "CPV",  
                'f8': "CPV",  
                'f45': "Praia",  
                'f46': "9951033",  
                'f10': "1",  
                'f13': "01",  
                'f19': "14",  
                'f20sf1': "Irmaos Correia",  
                'f20sf2': "Achada Grande Frente",  
                'f14': pessoas[0]['passaporte'],  
                'f16': pessoas[0]['validade_passaporte']['inicio'],  
                'f17': pessoas[0]['validade_passaporte']['fim'],  
                'f15': "CPV",  
                'txtInfoMotEstada': pessoas[0]['motivo'],  
                'f32': "PRT",  
                'f25': "15",  
                'f34sf5': "6",  
                'f30': pessoas[0]['data_viagem']['partida'],  
                'f31': pessoas[0]['data_viagem']['retorno'],  
                'cmbDespesasRequerente_1': "1",  
                'cmbDespesasRequerente_2': "",  
                'cmbDespesasPatrocinador_1': "2",  
                'cmbDespesasPatrocinador_2': '',  
                'f34': pessoas[0]['patrocinador'],  
                'f34sf2': pessoas[0]['endereco_patrocinador'],  
                'f43': '',  
                'f43sf2': '',  
                'f43sf3': '',  
                'f43sf4': '',  
                'f43sf5': '',  
                'f43sf6': '',  
                'f18sf1': '',  
                'f18sf2': '',  
                'f18sf3': '',  
                'f29sf2': '',  
                'txtInfoMotEstada': '',  
                'em_destino_2': '',  
                'dataImpressoesDigitais': '',  
                'numVinImpressoesDigitais': '',  
                'f27sf2': '',  
                'f34sf3': '',  
                'f34sf4': '',  
                'f_date_c': '',  
                'cmbPeriodo': ''  
            }  
            
            res2 = requests.post("https://pedidodevistos.mne.gov.pt/VistosOnline/ScheduleController",  
                                 cookies=cookies, headers=headers,  
                                 proxies=proxies, data=form_data)  
            if res2.status_code == 200:
                soup = BeautifulSoup(res2.text, 'html.parser')  
                error_div = soup.find('div', id='div_erro')  
                if error_div:  
                    error_message = error_div.find('td', class_='texto_erro').get_text(strip=True)
                    print(error_message)
                    return
                else:
                    print('Second form submitted successfully.\n') 
                    # Here f_date_c comes from Telegram 
                    payload = {  
                        'lang': 'ENG',  
                        'txtHuman': '',
                        'back': '',  
                        'f_date_c': '2025/05/03',  
                        'cmbPeriodo': '4'  
                    }
                    res = requests.post("https://pedidodevistos.mne.gov.pt/VistosOnline/SubmeterVistoCriaPDF", cookies=cookies, headers=headers,  
                                 proxies=proxies, data=payload)
                    soup = BeautifulSoup(res.text, 'html.parser')  
                    error_div = soup.find('div', id='div_erro')  
                    if error_div:  
                        error_message = error_div.find('td', class_='texto_erro').get_text(strip=True)
                        print(error_message)
                        return  
                    else:
                        print("Booking is success!")
            else:  
                print(f"Error in second submission: {res2.status_code} - {res2.text}")  

        else:  
            print(f"Error: {res1.status_code}")  

    except Exception as e:  
        print(f"We encountered an error: {e}")  

if __name__ == "__main__":  
    reCaptcha(api_key, website_url, website_key, username, password, proxies, pessoas)