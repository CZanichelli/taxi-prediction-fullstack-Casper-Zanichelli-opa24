import requests 
from urllib.parse import urljoin

def read_api_endpoint(endpoint = "/data", base_url = "http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.get(url)
    
    return response

def read_api_endpoint_predict(endpoint = "/predict", base_url = "http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.get(url)

    return response