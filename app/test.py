import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "namedata/tim")
print(response.json())

response = requests.put(BASE + "video/1", {"name": "Tim", "views": 5000, "likes": 10})
print(response.json())

response = requests.get(BASE + "video/1")
print(response.json())

response = requests.get(BASE + "video/6")
print(response.json())


data = [{"name": "Time", "views": 5000, "likes": 10},
        {"name": "Endless", "views": 10000, "likes": 23},
        {"name": "Gladiator", "views": 6000, "likes": 1016},
        {"name": "Space", "views": 3000, "likes": 1016}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())


response = requests.delete(BASE + "video/0")
print(response)



########################


data = [{"name": "Time", "views": 5000, "rating": 10},
        {"name": "Endless", "views": 10000, "rating": 23},
        {"name": "Gladiator", "views": 6000, "rating": 1016},
        {"name": "Space", "views": 3000, "rating": 1016}
]

for i in range(len(data)):
    response = requests.put(BASE + "movie/" + str(i), data[i])
    print(response.json())

response = requests.get(BASE + "movie/0")
print(response.json())

response = requests.patch(BASE + "movie/0", {"views": 0})
print(response.json())

response = requests.get(BASE + "movie/0")
print(response.json())