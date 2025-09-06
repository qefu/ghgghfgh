import requests
import time

usernames = []

with open('names.txt', 'r') as file:
    usernames = file.read().splitlines()

API_ENDPOINT = "https://users.roblox.com/v1/usernames/users"


def getUserId(username):
    requestPayload = {"usernames": [username], "excludeBannedUsers": False}

    while True:
        responseData = requests.post(API_ENDPOINT, json=requestPayload)

        if responseData.status_code == 200:
            data = responseData.json()["data"]
            if data:
                userId = data[0]["id"]
                result = f"{userId}-{username}"
                print(result)
                with open("ids.txt", "a") as output_file:
                    output_file.write(result + "\n")
                return userId
            else:
                print(f"Username Not Used: {username}")
                with open("inexistant.txt", "a") as inexistant_file:
                    inexistant_file.write(username + "\n")
            return None
        elif responseData.status_code == 429:
            print("Rate limited. Waiting for 0.5 seconds...")
            time.sleep(0.5)
        else:
            print(f"Error: Received status code {responseData.status_code}")
            break


for username in usernames:
    getUserId(username)
    time.sleep(0.01)
