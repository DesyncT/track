import socketio
import models.functions as functions
import requests
sio = socketio.Client()

headers = {
    "Origin": "https://www.bloxybet.com",
    "Referer": "https://www.bloxybet.com/",
    "User-Agent": "Mozilla/5.0"
}

@sio.event
def connect():
    print("✅ Connected, Loading")
    
    

@sio.event
def disconnect():
    print("❌ reconnecting")

@sio.event
def connect_error(data):
    print("❌ Connection failed:", data)

@sio.on("*")
def catch_all(event, data):
    if event == "tip_sent":
        receiver = functions.get_username(data['to_userid'])
        sender = data['from_username']
        itemlist = ""
        value = 0
        for i in data['items']:
            itemlist += f"{i['display_name']} ({i['value']})\n"
            value += int(i['value'])

        embed = {
            "title": "tips | alert",
            "description": f"A tip of **{value}** has been sent!",
            "color": 0x0cfc94,
            "fields": [
                {"name": "from", "value": f"```{sender}```", "inline": True},
                {"name": "to", "value": f"```{receiver}```", "inline": False},
                {"name": f"items ({value})", "value": f"```{itemlist}```", "inline": False}
            ],
        }

        payload = {
            "username": "tips",
            "content": "<@&1372756572803170385>",
            "embeds": [embed]
        }

        requests.post("https://discord.com/api/webhooks/1373462186302898368/bCkpfpvPa29-Y_bbSvM7Kl7xE7WVqDKYa93Z1yYrz0E3SuZ7D1iABVdV7J0hEDp4zV81", json=payload)
    if event == "game_created":
        value = 0
        itemlist = ""
        mentions = ""
        if value > 5000:
            mentions += "<@&1372756426509779074> "
        if value > 10000:
            mentions += "<@&1372756476820721816> "
        if value > 20000:
            mentions += "<@&1372756516117020702> "

        for i in data['starter']['items']:
            itemlist += f"{i['display_name']} ({i['value']})\n"
            value += int(i['value'])

        embed = {
            "title": "game creation | alert",
            "description": f"A game of **{value}** was created",
            "color": 0x0cfc94,
            "fields": [
                {"name": f"Starter Items ({value})", "value": f"```{itemlist}```", "inline": False},
                {"name": "Starter", "value": f"```{data['starter']['username']}```", "inline": False},
            ],
        }

        payload = {
            "username": "games",
            "content": mentions,
            "embeds": [embed]
        }

        requests.post("https://discord.com/api/webhooks/1373462186302898368/bCkpfpvPa29-Y_bbSvM7Kl7xE7WVqDKYa93Z1yYrz0E3SuZ7D1iABVdV7J0hEDp4zV81", json=payload)
    if event == "game_updated":
        startervalue = 0
        starteritems = ""

        joinervalue = 0
        joineritems = ""

        

        mentions = " "
        

        for i in data['starter']['items']:
            starteritems += f"{i['display_name']} ({i['value']})\n"
            startervalue += int(i['value'])

        for i in data['joiner']['items']:
            joineritems += f"{i['display_name']} ({i['value']})\n"
            joinervalue += int(i['value'])
        total = joinervalue + startervalue
        if total > 5000:
            mentions += "<@&1372756426509779074> "
        if total > 10000:
            mentions += "<@&1372756476820721816> "
        if total > 20000:
            mentions += "<@&1372756516117020702> "
        if data['winner'] == data['starter']['side']:
            winner = data['starter']['username']
            loser = data['joiner']['username']
        else:
            loser = data['starter']['username']
            winner = data['joiner']['username']

        embed = {
            "title": "game played | alert",
            "description": f"A game of **{total}** was just played",
            "color": 0x0cfc94,
            "fields": [
                {"name": f"Starter Items ({startervalue})", "value": f"```{starteritems}```", "inline": False},
                {"name":f"Joiner Items ({joinervalue})", "value": f"```{joineritems}```", "inline": False},
                {"name":f"Winner", "value": f"```{winner}```", "inline": False},
                {"name":f"loser", "value": f"```{loser}```", "inline": False}
            ],
        }

        payload = {
            "username": "games",
            "content": mentions,
            "embeds": [embed]
        }

        requests.post("https://discord.com/api/webhooks/1373462186302898368/bCkpfpvPa29-Y_bbSvM7Kl7xE7WVqDKYa93Z1yYrz0E3SuZ7D1iABVdV7J0hEDp4zV81", json=payload)

sio.connect(
    "https://api.bloxybet.com",
    headers=headers,
    transports=["websocket"],
    socketio_path="/socket.io"
)

sio.wait()
