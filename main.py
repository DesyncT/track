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
            "embeds": [embed]
        }

        requests.post("https://discord.com/api/webhooks/1378537059609874472/tYedgfzoQwbG14yokj5K3cn3yQBd8fC0my87QbCnZkxzuhHkWYShNx_oWXZtP6IvcizV", json=payload)

sio.connect(
    "https://api.bloxybet.com",
    headers=headers,
    transports=["websocket"],
    socketio_path="/socket.io"
)

sio.wait()
