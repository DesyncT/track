import requests

def get_username(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['name']
    else:
        return "UNKNOWN"
