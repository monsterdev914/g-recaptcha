import os  
import json  
import random  
import requests  
from dotenv import load_dotenv  
from bs4 import BeautifulSoup  
import capsolver  
import re
from datetime import date, datetime, timedelta
import uuid
load_dotenv()  

# Load data files  
with open('personal_data.json', 'r', encoding='utf-8') as f:  
    pessoas = json.load(f)  
with open('proxy_list.json', 'r') as f:  
    proxy_list = json.load(f)

#Loading logined cookies

with open('cookies.json', 'r', encoding='utf-8') as f:
    logined_cookies = json.load(f)  


# Environment variables  
api_key = os.getenv("API_KEY")  
website_url = os.getenv("WEBSITE_URL")  
website_key = os.getenv("WEBSITE_KEY")  
username = os.getenv("USER_NAME")  
password = os.getenv('PASSWORD')  
# proxy = random.choice(proxy_list)  
# http://user-john123_F6xyN:Pwd123@pr.u26x17fh.lunaproxy.net:32233
# http://user-abcde_N0ieA:Pwd123@pr.j5vjhbtp.lunaproxy.net:32233
# Configure proxies  
proxies = {  
    "http": 'http://noah2024-GM-7:Saulo2020@p.webshare.io:8', 
    'https':'http://noah2024-GM-7:Saulo2020@p.webshare.io:8' 
}  

# Consolidated headers  
HEADERS = {  
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  
    "Accept": "ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",  
    "Accept-Language": "en-US,en;q=0.9",  
    "Content-Type": "application/x-www-form-urlencoded"  # 🛠️ Fixed content type  
}  

def get_cookies_from_logined_cookies(username):
    return [item for item in logined_cookies if item['username'] == username]

def add_cookies_to_logined_cookies(cookie, username, proxy):
    with open('cookies.json', 'r') as f:
            data = json.load(f)
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = {
        'username': username,
        'created': create_date,
        'cookie': cookie,
        'proxy': proxy
    }
    data.append(new_data)
    with open('cookies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
def update_cookies_to_logined_cookies(cookie, username, proxy):
    with open('cookies.json', 'r') as f:
            data = json.load(f)
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for item in data:
        if item['username'] == username:
           item['cookie'] = cookie
           item['created'] = create_date
           item['proxy'] = proxy 
    with open('cookies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
def getBusyPeriods(reqHandle, id_post, appointment_date):
    endPoint = f'https://pedidodevistos.mne.gov.pt/VistosOnline/getPeriodosOcupados?id_posto={id_post}&data_agendamento={appointment_date}'
    try:
        response = reqHandle.get(endPoint)
        str = response.text
        numbers = re.findall(r'\d+', str)
        numbers_list = list(map(int, numbers))
        return numbers_list
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
    
def availablePeriods(busyPeriods):
    array1 = list(range(1, 15))
    result = list(set(array1) - set(busyPeriods))
    return result


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
        # session.cookies.update(init_res.cookies.get_dict())
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
        # print('reCapture passed\n', solution["gRecaptchaResponse"])
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
    print("Starting....")
    stored_cookies = get_cookies_from_logined_cookies(username=username)
    if stored_cookies:
        cookies = stored_cookies[0]['cookie']
        proxies = stored_cookies[0]['proxy']
    # cookies = {'Vistos_sid': 'iq8DqGqkX9I0g+9xWnxt/UDSEmZWBFpCbsUEfXqKBQ6ZoWQT+UMhuZ4xT9hJtje0kd12XMhKxeRMJj5yIYVWKkYNRdJ1G1zTN2JBM8DgcYX9/DbW+1DsjWqOCqSqvcjU', 'cookiesession1': '678B2870BCD751A215494FCA233427C0'}
    else:
        cookies = login(api_key, website_url, website_key, username, password, proxies)
        add_cookies_to_logined_cookies(cookie=cookies,username=username, proxy=proxies)
        print(f'Added cookie:\n \tuser: {username}\n\tcookie: {cookies}')
    if not cookies or "Vistos_sid" not in cookies:  
        print("Session initialization failed")  
        return  
    print(proxies)
    
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
            # "cb_motivo_estada_sch": "10",  
            # "cb_viaja_reune_turismo": "FAM_N",  
            "tipo_visto": "CT",  
            "tipo_visto_desc": "VISTO DE CURTA DURAÇÃO - TRABALHO SAZONAL",  
            "class_visto": "SCH",  
            "cod_estada": "10",  
            "id_visto_doc": "2"  
        } 
        # form_data1 = {  
        #     "lang": "ENG",  
        #     "nacionalidade": "CPV",  
        #     "pais_residencia": "FRA",  
        #     "tipo_passaporte": "01",  
        #     "copia_pedido": "null",  
        #     "cb_pais_residencia": "CPV",  
        #     "cb_tipo_passaporte": "01",  
        #     "cb_qt_dias": "SCH",  
        #     "cb_trab_sazonal": "O",  
        #     "cb_motivo_estada_sch": "10",  
        #     "cb_viaja_reune_turismo": "FAM_N",  
        #     "tipo_visto": "C",  
        #     "tipo_visto_desc": "SHORT STAY VISA (SCHENGEN)",  
        #     "class_visto": "SCH",  
        #     "cod_estada": "10",  
        #     "id_visto_doc": "36"  
        # } 
        
        session = requests.Session()  
        session.headers.update(HEADERS)
        session.cookies.update(cookies)  
        session.proxies.update(proxies)
        res1 = session.post(  
            "https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",  
            data=form_data1
        )
        with open('form1.html', 'w', encoding="utf-8") as file:
            file.write(res1.text) 
        if res1.status_code == 403:  
            print(f"Session Error: {res1.status_code}")
            new_cookies = login(api_key=api_key, website_url=website_url, website_key=website_key, username=username, password=password, proxies=proxies)
            update_cookies_to_logined_cookies(cookie=new_cookies, username=username, proxy=proxies)
            session.cookies.update(new_cookies)  
        elif res1.status_code != 200:
            print(f'Unexpected Error in Form1: {res1.status_code}')
        # print(res1.text)
        if res1.text.find('Perdeu a sessão. Volte para a') != -1:
            print(f"Session Error: {res1.status_code}")
            
            # print('Loging Out...')
            
            # session.get('https://pedidodevistos.mne.gov.pt/VistosOnline/logout')
            
            new_cookies = login(api_key=api_key, website_url=website_url, website_key=website_key, username=username, password=password, proxies=proxies)
            
            if not new_cookies or "Vistos_sid" not in new_cookies:  
                print("Plz try again after")
                return
            if new_cookies['Vistos_sid'] == '':
                print("Plz try another account after")
                return
            update_cookies_to_logined_cookies(cookie=new_cookies, username=username, proxy=proxies)
            session.cookies.update(new_cookies)
            res1 = session.post(  
                "https://pedidodevistos.mne.gov.pt/VistosOnline/Formulario",  
                data=form_data1
            )
    
        # Extract CSRF token 🛠️ Critical fix
        soup = BeautifulSoup(res1.text, 'html.parser')
        token_input = soup.find('input', attrs={'name': '__RequestVerificationToken'})
        if not token_input:  
            print("CSRF token missing")  
            return  
            
        csrf_token = token_input['value']  
        print(f'__RequestVerificationToken: {csrf_token}')
        # Second form submission 🛠️ Fixed token reference  
        
        # form_data2 = {  
        #         'lang': 'ENG',  
        #         'txtHuman': '',  
        #         '__RequestVerificationToken': csrf_token,  
        #         'RGPDAccepted': '',  
        #         'posto_representacao': 'null',  
        #         'f0sf1': "3018",  
        #         'f1': pessoas[0]['nome_completo'],  
        #         'f2': pessoas[0]['nome_completo'],  
        #         'f3': pessoas[0]['nome_pai'],  
        #         'f4': pessoas[0]['nascimento'],  
        #         'f6': pessoas[0]['local_nascimento'],  
        #         'f6sf1': "CPV",  
        #         'f7sf1': "CPV",  
        #         'f8': "CPV",
        #         'f9':'FEMININO', 
        #         'f10': "1",  
        #         'txtApelidoPaternal': '',  
        #         'txtNomePaternal': '',  
        #         'txtEnderecoPaternal': '',  
        #         'txtTelefonePaternal': '',  
        #         'txtEmailPaternal': '',  
        #         'cmbNacionalidadePaternal': '',  
        #         'f5': '',
        #         'f13': "01",  
        #         'f14': pessoas[0]['passaporte'],  
        #         'f16': pessoas[0]['validade_passaporte']['inicio'],  
        #         'f17': pessoas[0]['validade_passaporte']['fim'],  
        #         'f15': "CPV",  
        #         'f43': '',  
        #         'f43sf2': '',  
        #         'f43sf3': '',  
        #         'f43sf4': '',  
        #         'f43sf5': '',  
        #         'f43sf6': '',  
        #         'f0': pessoas[0]['email'],  
        #         'f45': "PRAIA",  
        #         'f46': "9951033",  
        #         'f18sf1': '',  
        #         'f18sf2': '',  
        #         'f18sf3': '',  
        #         'f19': "01", #14 
        #         'f20sf1': "NO WORK", #"IRMAOS CORREIA",  
        #         'f20sf2': "PRAIA 9951033", #"ACHADA GRANDE FRENTE",
        #         'f29':'10',  
        #         'f29sf2': '',  
        #         'f29sf3': '',  
        #         'txtInfoMotEstada': pessoas[0]['motivo'],  
        #         'em_destino_1':'PRT',
        #         'em_destino_2':'',
        #         'em_destino_3':'',
        #         'f32': "PRT",
        #         'f24':'1',  
        #         'f25': "15",  
        #         'f30': pessoas[0]['data_viagem']['partida'],  
        #         'f31': pessoas[0]['data_viagem']['retorno'],
        #         'cmbImpressoesDigitais' : 'N', 
        #         'dataImpressoesDigitais': '',  
        #         'numVinImpressoesDigitais': '',
        #         'f27':'N',  
        #         'f27sf2': '',  
        #         'f27sf3': '',  
        #         'cmbReferencia': 'individual',
        #         'f34': "HOTEL LISBON", #pessoas[0]['patrocinador'],  
        #         'f34sf3': '',  
        #         'f34sf2': "AVENIDA LISBON", #pessoas[0]['endereco_patrocinador'],  
        #         'f34sf4': '',  
        #         'f34sf5': '1', #"6",  
        #         'cmbDespesasRequerente_1': "1",  
        #         'cmbDespesasRequerente_2': "",  
        #         'cmbDespesasRequerente_3': "",  
        #         'cmbDespesasRequerente_4': "",  
        #         'cmbDespesasPatrocinador_1': "2",  
        #         'cmbDespesasPatrocinador_2': '',  
        #         'cmbDespesasPatrocinador_3': '',  
        #         'cmbDespesasPatrocinador_4': '', 
        #         'tipo_visto':'C', 
        #         'tipo_visto_desc': form_data1['tipo_visto_desc'],
        #         'class_visto':form_data1['class_visto'],
        #         "cod_estada": form_data1['cod_estada'],  
        #         "id_visto_doc": form_data1['id_visto_doc'],
        #         'tipo_passaporte': form_data1['tipo_passaporte'],
        #         "nacionalidade": form_data1['nacionalidade'],  
        #         "pais_residencia": 'FRA', #form_data1['pais_residencia'],
        #         'f_date_c': '',  
        #         'cmbPeriodo': '',
        # }
        #Real Data
        form_data2 = {  
            'lang': 'PT',  
            'txtHuman': '',  
            '__RequestVerificationToken': csrf_token,  
            'RGPDAccepted': '',  
            'posto_representacao': 'null',  
            'f0sf1': "5088",  
            'f1': pessoas[0]['nome_completo'],  
            'f2': pessoas[0]['nome_completo'],  
            'f3': pessoas[0]['nome_pai'],  
            'f4': pessoas[0]['nascimento'],  
            'f6': pessoas[0]['local_nascimento'],  
            'f6sf1': "CPV",  
            'f7sf1': "CPV",  
            'f8': "CPV",
            'f9':'FEMININO', 
            'f10': "1",  
            'txtApelidoPaternal': '',  
            'txtNomePaternal': '',  
            'txtEnderecoPaternal': '',  
            'txtTelefonePaternal': '',  
            'txtEmailPaternal': '',  
            'cmbNacionalidadePaternal': '',  
            'f5': '',
            'f13': "01",  
            'f14': pessoas[0]['passaporte'],  
            'f16': pessoas[0]['validade_passaporte']['inicio'],  
            'f17': pessoas[0]['validade_passaporte']['fim'],  
            'f15': "CPV",  
            'f43': '',  
            'f43sf2': '',  
            'f43sf3': '',  
            'f43sf4': '',  
            'f43sf5': '',  
            'f43sf6': '',  
            'f0': pessoas[0]['email'],  
            'f45': "PRAIA",  
            'f46': "9951033",  
            'f18sf1': '',  
            'f18sf2': '',  
            'f18sf3': '',  
            'f19': "14", #14 
            'f20sf1': "NO WORK", #"IRMAOS CORREIA",  
            'f20sf2': "PRAIA 9951033", #"ACHADA GRANDE FRENTE",
            'f29':'10',  
            'f29sf2': '',  
            'f29sf3': '',  
            'txtInfoMotEstada': pessoas[0]['motivo'],  
            'em_destino_1':'PRT',
            'em_destino_2':'',
            'em_destino_3':'',
            'f32': "PRT",
            'f24':'1',  
            'f25': "15",  
            'f30': pessoas[0]['data_viagem']['partida'],  
            'f31': pessoas[0]['data_viagem']['retorno'],
            'cmbImpressoesDigitais' : 'N', 
            'dataImpressoesDigitais': '',  
            'numVinImpressoesDigitais': '',
            'f27':'N',  
            'f27sf2': '',  
            'f27sf3': '',  
            'cmbReferencia': 'individual',
            'f34': "HOTEL LISBON", #pessoas[0]['patrocinador'],  
            'f34sf3': '',  
            'f34sf2': "AVENIDA LISBON", #pessoas[0]['endereco_patrocinador'],  
            'f34sf4': '',  
            'f34sf5': '1', #"6",  
            'cmbDespesasRequerente_1': "1",  
            'cmbDespesasRequerente_2': "",  
            'cmbDespesasRequerente_3': "",  
            'cmbDespesasRequerente_4': "",  
            'cmbDespesasPatrocinador_1': "2",  
            'cmbDespesasPatrocinador_2': '',  
            'cmbDespesasPatrocinador_3': '',  
            'cmbDespesasPatrocinador_4': '', 
            'tipo_visto':'C', 
            'tipo_visto_desc': form_data1['tipo_visto_desc'],
            'class_visto':form_data1['class_visto'],
            "cod_estada": form_data1['cod_estada'],  
            "id_visto_doc": form_data1['id_visto_doc'],
            'tipo_passaporte': form_data1['tipo_passaporte'],
            "nacionalidade": form_data1['nacionalidade'],  
            "pais_residencia": form_data1['pais_residencia'],
            'f_date_c': '',  
            'cmbPeriodo': '',
        }
        boundary = f'----{uuid.uuid4().hex}'
        # temp = {  
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",  
        #     "Accept-Language": "en-US,en;q=0.9",  
        # }
        HEADERS["Content-Type"] = f'multipart/form-data; boundary={boundary}'
        session.cookies.update(res1.cookies.get_dict())
        session.headers.update(HEADERS)
        files = {
            'foto': ('', None),
            'file1': ('', None),
            'file2': ('', None),
            'file3': ('', None),
            'file4': ('', None)
        }
        # Form 2 Request
        res2 = session.post(  
            "https://pedidodevistos.mne.gov.pt/VistosOnline/ScheduleController",  
            data=form_data2,
            files=files,
            allow_redirects=False
        )
        with open('form2.html', 'w', encoding="utf-8") as file:
            file.write(res2.text)
        HEADERS['Content-Type'] = 'application/x-www-form-urlencoded'
        if res2.status_code == 200:
            print(f'Form2--->{res2.status_code}')
            error_td = BeautifulSoup(res2.text, 'html.parser').find('td', class_='texto_erro')
            if error_td:
                print(f"Form error: {error_td.get_text(strip=True)}")
                return
        elif res2.status_code == 302:
            print(f'Form2--->{res2.status_code}')
            print(res2.headers["Location"])
            start_date = date.today()
            end_date = date(2025, 5, 10)
            current_date = start_date
            while current_date <= end_date:
                print(current_date.strftime("%Y-%m-%d"))  # Format as YYYY-MM-DD
                current_date += timedelta(days=1)  # Increment by one day
                # busyPeriods = getBusyPeriods(session, 5084, current_date)
                # print(f'Busy Periods: {busyPeriods}')
                # a_period = availablePeriods(busyPeriods)
                final_payload = {
                    'lang': 'ENG',
                    'f_date_c': current_date,
                    'cmbPeriodo': 1
                }
                final_res = session.post(
                    "https://pedidodevistos.mne.gov.pt/VistosOnline/SubmeterVistoCriaPDF",
                    data=final_payload,
                    allow_redirects=False
                )
                with open('booking_result.html', 'w', encoding="utf-8") as file:
                    file.write(final_res.text)
                if final_res.status_code == 200:
                    print("Trying new slot")
                elif final_res.status_code == 302:
                    print(final_res.headers['Location'])
                    rrr3 = session.get('https://pedidodevistos.mne.gov.pt/VistosOnline/MostrarPdf?')
                    with open("pdf.html", "w", encoding='utf-8') as pdf_file:
                        pdf_file.write(rrr3.text)

                    print(f'PDF:{rrr3.status_code}')
                    with open("downloaded.pdf", "wb") as pdf_file:
                        pdf_file.write(rrr3.content)
                    print("Booking successful!")
                    break
                else:
                    print(f"Booking Failed: {final_res.status_code}")
        else:
            print(f'Form2: Error {res2.status_code}')

    except Exception as e:  
        print(f"Workflow error: {str(e)}")  

if __name__ == "__main__":  
    reCaptcha(api_key, website_url, website_key, username, password, proxies, pessoas)
    
    
    
# https://pedidodevistos.mne.gov.pt/VistosOnline/MostrarPdf?