import requests, base64, gzip, json

def get_game_preview(gameid, server='uncivserver.xyz'):
    resp = requests.get(f'http://{server}/files/{gameid}_Preview')
    data = json.loads(
        gzip.decompress(base64.b64decode(resp.content)).decode("utf-8")
    )
    return  data

def get_game_data(gameid, server='uncivserver.xyz'):
    resp = requests.get(f'http://{server}/files/{gameid}')
    data = json.loads(
        gzip.decompress(base64.b64decode(resp.content)).decode("utf-8")
    )
    return data

def get_civs(gameid, server='uncivserver.xyz'):
    data = get_game_preview(gameid=gameid, server=server)
    civs = []
    for civ in data["civilizations"]:
        # otherwise it is city-state
        if "playerId" in civ:
            civs.append(civ["civName"])
    return civs


def get_notifications(gameid: str, server='uncivserver.xyz', sanitize: bool = True) -> dict[str, list]:
    data = get_game_data(gameid=gameid, server=server)
    # data = eval(open('test.txt').read())
    civs = data['civilizations']
    notifications: dict[str, list] = {}
    for civ in civs:
        if civ['civName'] == 'Barbarians':
            continue
        current_civ_notifications: list[str] = []
        # then it is AI
        if 'notifications' not in civ:
            continue
        for idx, notification in enumerate(civ['notifications']):
            text: str = notification["text"]
            if sanitize:
                text = text.translate(
                    {
                    ord("["): "",
                    ord("]"): "",}
                )
                text = f"{idx + 1}: {text}"
            current_civ_notifications.append(text)
        notifications[civ['civName']] = current_civ_notifications
    return notifications