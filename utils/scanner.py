import requests

def test_payload(url, param, payload):
    test_url = url + payload
    r = requests.get(test_url, timeout=10)
    return payload in r.text
