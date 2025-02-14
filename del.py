import requests

sample = "adi narayana "

documents = [
    "This is the first document",
    "This document is the second document",
    "And this is the third one ",
    "Is this the first document adi",
]
    # Process query and return response
url = "http://127.0.0.1:8001/tf-idf/"

response = requests.post(url, json={"corpus": documents, "query": sample})
if response.status_code == 200:
    res = response.json()
    print(res)
else:
    res = {"response": "Error occurred when processing the request to url "  + url+ " "+ response.json()}