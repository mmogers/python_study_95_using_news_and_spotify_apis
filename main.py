import os, requests, json
from requests.auth import HTTPBasicAuth

max = 5

news = os.environ['newsapi']
organization = os.environ['organizationid']
api_key = os.environ['openai']


country = "gb"
url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={news}" 

result = requests.get(url)
data = result.json()

responses = []

counter = 0
for article in data['articles']:
  counter += 1
  if counter > max:
    break
  response = (article['title'].strip())
  responses.append(response)


clientId= os.environ['CLIENT_ID']
clientSecret= os.environ['CLIENT_SECRET']
url = "https://accounts.spotify.com/api/token/"
data = {"grant_type":"client_credentials"}
auth = HTTPBasicAuth(clientId, clientSecret)
response = requests.post(url, data = data, auth=auth)
accessToken = response.json()['access_token']


headers = {
    "Authorization": f"Bearer {accessToken}"
}

params = {
    "q": " ".join(responses),
    "type": "track",
    "limit": 5
}

songs = []

for response in responses:
  headline = response.replace(" ", "%20")
  search = f"?q={headline}&type=track"
  url = "https://api.spotify.com/v1/search"
  fullUrl = f"{url}{search}"
  #print(fullUrl)
  response = requests.get(fullUrl, headers = headers)
  data = response.json()
  #print(json.dumps(data, indent=2))
  try:
    songs.append(data['tracks']['items'][0])
  except:
    songs.append({"name":None, "preview_url":None})
    
for i in range(max):
  if songs[i]["name"] != None and songs[i]["preview_url"] != None:
    print(i+1, " News: ", responses[i])
    print("Song: ", songs[i]['name'])
    print("URL: ", songs[i]['preview_url'])
    print()


