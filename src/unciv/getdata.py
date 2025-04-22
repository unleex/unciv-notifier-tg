import requests, base64, gzip, json

def get_civs(gameid, server='uncivserver.xyz'):
    resp = requests.get(f'http://{server}/files/{gameid}_Preview')
    open('in', 'w').write(resp.text)
    base64.decode(open('in', 'r'), open('out', 'wb'))
    f = open('out', 'rb').read()
    data = json.loads(gzip.decompress(f).decode())
    civs = []
    for civ in data["civilizations"]:
        # otherwise it is city-state
        if "playerId" in civ:
            civs.append(civ["civName"])
    return civs
