import requests, json

response = requests.get(
    "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
)

# print question titles from https://stackoverflow.com/
for data in response.json()["items"]:
    # E.g, you can extract only those questions from stackoverflow for which you could possibly known the answer
    if data["answer_count"] == 0:
        print(data["title"])
        print(data["link"])
    else:
        print("skipped")
