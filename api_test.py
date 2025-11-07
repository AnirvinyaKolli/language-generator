import requests
import time

target_word = "hello"
url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + str(target_word)
fail = False


while True:
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]
        print(response.status_code)
        if fail:
            end = time.time()
            print(f"speed : {end - start:.4f} seconds")
            break
    else:
        start = time.time()
        fail = True
        print(response.status_code)

