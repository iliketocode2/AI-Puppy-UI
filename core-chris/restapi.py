from pyscript import fetch
import json

headers = {
    "Accept": "*/*",
}

def get(url):
    try:
        response = await fetch(url, method='GET', headers = headers)
        if response.ok:
            data = await response.text()
            return data
        else:
            print(f"HTTP Error: {response.status}")
    except Exception as e:
        print(f"Fetch error: {e}")
        return None   


def post(url, headers, body):
    try:
        response = await fetch(
            url, 
            method="POST", 
            headers=headers,
            body=json.dumps(body),
        )
        if response.ok:
            data = await response.json()
            return data
        else:
            print(f"HTTP Error: {response.status}")
    except Exception as e:
        print(f"Fetch error: {e}")
        return None
