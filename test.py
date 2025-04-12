import requests
import uuid
HEADERS = {  
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",  
    "Accept": "ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",  
    "Accept-Language": "en-US,en;q=0.9",  
    "Content-Type": "application/x-www-form-urlencoded"  # 🛠️ Fixed content type  
}
form_data2 = {  
    'lang': 'PT',  
    'txtHuman': '',  
    '__RequestVerificationToken': 'EB5tvZynQcTYBkKsEygVZlA9E092kiJNrSo50hhO3yG3/0VhSqTEQ==',  
    'RGPDAccepted': '',  
    'posto_representacao': 'null',  
    'f0sf1': "5088",  
    'f1': 'PERREIRA DOS REIS',  
    'f2': 'ANGELA SONIA RIBEIRO FURTADO',  
    'f3': 'KELLY EVELINE',  
    'f4': '1999/04/02',  
    'f6': 'SANTIAGO',  
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
    'f14': 'PA395818',  
    'f16': '2024/04/15',  
    'f17': '2029/04/14',  
    'f15': "CPV",  
    'f43': '',  
    'f43sf2': '',  
    'f43sf3': '',  
    'f43sf4': '',  
    'f43sf5': '',  
    'f43sf6': '',  
    'f0': 'sicilia117@uorak.com',  
    'f45': "PRAIA",  
    'f46': "9951033",  
    'f18sf1': '',  
    'f18sf2': '',  
    'f18sf3': '',  
    'f19': "14", #14 
    'f20sf1': "IRMAOS CORREIA", #"IRMAOS CORREIA",  
    'f20sf2': "ACHADA GRANDE FRENTE", #"ACHADA GRANDE FRENTE",
    'f29':'10',  
    'f29sf2': '',  
    'f29sf3': '',  
    'txtInfoMotEstada': 'FERIAS',  
    'em_destino_1':'PRT',
    'em_destino_2':'',
    'em_destino_3':'',
    'f32': "PRT",
    'f24':'1',  
    'f25': "15",  
    'f30': '2025/05/17',  
    'f31': '2025/06/04',
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
    'f34sf5': '6', #"6",  
    'cmbDespesasRequerente_1': "1",  
    'cmbDespesasRequerente_2': "",  
    'cmbDespesasRequerente_3': "",  
    'cmbDespesasRequerente_4': "",  
    'cmbDespesasPatrocinador_1': "2",  
    'cmbDespesasPatrocinador_2': '',  
    'cmbDespesasPatrocinador_3': '',  
    'cmbDespesasPatrocinador_4': '', 
    'tipo_visto':'C', 
    'tipo_visto_desc': 'SHORT STAY VISA (SCHENGEN)',
    'class_visto':'SCH',
    "cod_estada": '10',  
    "id_visto_doc": '36',
    'tipo_passaporte': '01',
    "nacionalidade": 'CPV',  
    "pais_residencia": 'CPV',
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

files = {
    'foto': ('', None),
    'file1': ('', None),
    'file2': ('', None),
    'file3': ('', None),
    'file4': ('', None)
}  
session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update({
    'Vistos_sid':'teub4rLD4me/uk3VLjX6c2wbZYQQ+zsK1hDCpKMmkbPQbp7VjUAswfxt6f9J/b54vsq1Yg2SdCoK51dxhgBAa4ualSO4kil5mVrwJkDTigwxL3lYBvqKfd5Gt9zadflT; cookiesession1=678B2872186B4F44DA96C0CA420BDCB5',
    'cookiesession1':'678B2872186B4F44DA96C0CA420BDCB5'
})
proxy = 'http://noah2024-GM-8:Saulo2020@p.webshare.io:80'
response = session.post('https://pedidodevistos.mne.gov.pt/VistosOnline/ScheduleController', data=form_data2, files=files, proxies={  
    "http": proxy, 
    'https':proxy}, allow_redirects=False)
print(response.status_code)
