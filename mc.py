import requests, json

url = "http://mcapi.de/api/server-query/mc.vanillahigh.net/25565"
result = requests.get(url)
results = result.content.decode()
data = json.loads(results)
print(data)