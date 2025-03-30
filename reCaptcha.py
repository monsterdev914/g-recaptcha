import os  
import random
from dotenv import load_dotenv  
import capsolver  
import requests  

load_dotenv()  
  
proxy_list = [  
    "http://veqxkkot-AM-1:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-2:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-3:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-4:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-5:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-6:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-7:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-8:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-9:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-10:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-11:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-12:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-13:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-14:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-15:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-16:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-17:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-18:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-19:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-20:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-21:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-22:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-23:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-24:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-25:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-26:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-27:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-28:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-29:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-30:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-31:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-32:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-33:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-34:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-35:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-36:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-37:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-38:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-39:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-40:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-41:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-42:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-43:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-44:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-45:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-46:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-47:nq2r7cbk7sk8@p.webshare.io:80",  
    "http://veqxkkot-AM-48:nq2r7cbk7sk8@p.webshare.io:80",  
]  

def reCaptcha():  
    # Retrieve API keys and other credentials from environment variables  
    api_key = os.getenv("API_KEY")  
    website_url = os.getenv("WEBSITE_URL")  
    website_key = os.getenv("WEBSITE_KEY")  
    username = os.getenv("USER_NAME")  
    password = os.getenv('PASSWORD')  
    proxy = random.choice(proxy_list)  
    proxies = {  
        "http": proxy,  
        "https": proxy,  
    }  
    try:  
        capsolver.api_key = api_key  

        solution = capsolver.solve({  
            "type": "ReCaptchaV2Task",  
            "websiteURL": website_url,  
            "websiteKey": website_key,
            "proxy": proxies["http"]  
        })  

        payload = {  
            "username": username,  
            "password": password,  
            "rgpd": "Y",  
            "language": "PT",  
            "captchaResponse": solution["gRecaptchaResponse"]  
        }  

        headers = {  
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",   
        }

        res = requests.post("https://pedidodevistos.mne.gov.pt/$J@5Yg0RAhCxKgAhgfwtTouVMlnWPHDd_ubZzU6uSScB8ZmN3SlXxLKGpc", headers=headers, data=payload, proxies=proxies)  

        if res.status_code == 200:
            cookies = res.cookies
            data = res.json()  
            print(data)  
        else:  
            print(f"Error: {res.status_code} - {res.text}")  

    except Exception as e:  
        print(f"We encountered an error: {e}")   

if __name__ == "__main__":  
    reCaptcha()