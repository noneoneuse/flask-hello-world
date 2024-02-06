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

    # Rest of your code goes here
    # ...

    return jsonify({"transactionSetupId": tenant_id})

if __name__ == '__main__':
    app.run(debug=True)
