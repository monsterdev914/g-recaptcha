import os
from dotenv import load_dotenv  
import capsolver
import requests

load_dotenv()

api_key = os.getenv("API_KEY")
website_url = os.getenv("WEBSITE_URL")
website_key= os.getenv("WEBSITE_KEY")
print(f"API_KEY: {api_key}")
capsolver.api_key = api_key

solution = capsolver.solve({
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL":website_url,
            "websiteKey": website_key,
          })
print(solution["gRecaptchaResponse"])


# requests.post("https://pedidodevistos.mne.gov.pt/$J@5Yg0RAhCxKgAhgfwtTouVMlnWPHDd_ubZzU6uSScB8ZmN3SlXxLKGpc", {
    
# })
