import os  
import json  
import random  
import requests  
from dotenv import load_dotenv  
from bs4 import BeautifulSoup  
import capsolver  
load_dotenv()  

# Load data files  
with open('personal_data.json', 'r', encoding='utf-8') as f:  
    pessoas = json.load(f)  
with open('proxy_list.json', 'r') as f:  
    proxy_list = json.load(f)  

# Environment variables  
api_key = os.getenv("API_KEY")  
website_url = os.getenv("WEBSITE_URL")  
website_key = os.getenv("WEBSITE_KEY")  
username = os.getenv("USER_NAME")  
password = os.getenv('PASSWORD')  
proxy = random.choice(proxy_list)  
# http://user-john123_F6xyN:Pwd123@pr.u26x17fh.lunaproxy.net:32233
# http://user-abcde_N0ieA:Pwd123@pr.j5vjhbtp.lunaproxy.net:32233
# Configure proxies  
proxies = {  
    "http": 'user-john123_F6xyN:Pwd123@pr.u26x17fh.lunaproxy.net:32233',  
}  

# Consolidated headers  
HEADERS = {  
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",  
    "Accept-Language": "en-US,en;q=0.9",  
    "Content-Type": "application/x-www-form-urlencoded"  # 🛠️ Fixed content type  
}  

def login(api_key, website_url, website_key, username, password, proxies):  
    capsolver.api_key = api_key  
    try:  
        # Initialize session  
        session = requests.Session()  
        session.headers.update(HEADERS)  
        session.proxies.update(proxies)
        
        # Get initial cookies  
        # init_res = session.get(  
        #     'https://pedidodevistos.mne.gov.pt/VistosOnline/Authentication.jsp',  
        #     proxies=proxies  
        # )  
        # Solve CAPTCHA  
        solution = capsolver.solve({  
            "type": "ReCaptchaV2Task",  
            "websiteURL": website_url,  
            "websiteKey": website_key,  
            "proxy": proxies["http"]  
        })
        if 'gRecaptchaResponse' not in solution:  
            print("CAPTCHA solution failed")  
            return None  
        print('reCapture passed')
        # Authentication payload  
        payload = {  
            "username": username,  
            "password": password,  
            "rgpd": "Y",  
            "language": "PT",  
            "captchaResponse": solution["gRecaptchaResponse"]  
        }  

        # Login POST request

        login_res = session.post(  
            "https://pedidodevistos.mne.gov.pt/$J@5Yg0RAhCxKgAhgfwtTouVMlnWPHDd_ubZzU6uSScB8ZmN3SlXxLKGpc",  
            data=payload,
        )
        
        if login_res.status_code == 200:
            login_res_json = login_res.json()  
            if login_res_json["type"] == 'error':
                print(f'Error: {login_res_json['description']}')
                return None    
            else:
                return session.cookies.get_dict()
        print(f"Login failed: {login_res.status_code}")  
          

    except Exception as e:  
        print(f"Login error: {str(e)}")  
        return None  

def reCaptcha(api_key, website_url, website_key, username, password, proxies, pessoas):  
    """Main form submission workflow"""  
    cookies = login(api_key, website_url, website_key, username, password, proxies) 
    print(cookies) 
    if not cookies or "Vistos_sid" not in cookies:  
        print("Session initialization failed")  
        return  

    try:  
        # First form submission  

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
        
        session = requests.Session()  
        session.headers.update(HEADERS)  
        session.cookies.update(cookies)  
        
        res1 = session.post(  
            "https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",  
            data=form_data1
        )  
        if res1.status_code != 200:  
            print(f"Form1 error: {res1.status_code}")  
            return  

        # Extract CSRF token 🛠️ Critical fix
        soup = BeautifulSoup(res1.text, 'html.parser')
        token_input = soup.find('input', attrs={'name': '__RequestVerificationToken'})  
        if not token_input:  
            print("CSRF token missing")  
            return  
            
        csrf_token = token_input['value']  

        # Second form submission 🛠️ Fixed token reference  
        form_data2 = {  
                'lang': 'ENG',  
                'txtHuman': '',  
                '__RequestVerificationToken': csrf_token,  
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
        cookies = res1.cookies.get_dict()
        session.cookies.update(cookies) 
        # with open('form1.html', 'w', encoding="utf-8") as file:
        #     file.write(res1.text) 
        res2 = session.post(  
            "https://pedidodevistos.mne.gov.pt/VistosOnline/ScheduleController",  
            data=form_data2
        )   
        with open('1.html', 'w') as file:
            file.write(res2.text)
        if res2.status_code == 200:
            error_td = BeautifulSoup(res2.text, 'html.parser').find('td', class_='texto_erro')  
            if error_td:  
                print(f"Form error: {error_td.get_text(strip=True)}")  
                return  
            # Final submission  
            final_payload = {  
                'lang': 'ENG',  
                'f_date_c': '2025/05/03',  
                'cmbPeriodo': '4'  
            }  
            
            final_res = session.post(  
                "https://pedidodevistos.mne.gov.pt/VistosOnline/SubmeterVistoCriaPDF",  
                data=final_payload
            )  
            
            if final_res.status_code == 200:  
                print("Booking successful!")  
            else:
                print(f"Final submission failed: {final_res.status_code}") 
        else:
            print(f'Form2: Error {res2.status_code}') 

    except Exception as e:  
        print(f"Workflow error: {str(e)}")  

if __name__ == "__main__":  
    reCaptcha(api_key, website_url, website_key, username, password, proxies, pessoas)