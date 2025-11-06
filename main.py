import requests
import json

def create_word(part_of_speech):
    new_word = part_of_speech
    return new_word

def get_word_data(target_word):
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + str(target_word)


    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]
    else:
        return {
            "originalWord": "Nonsense entered",
            "partOfSpeech": "N/A",
            "word": "N/A"
        }

    og_word = data['word']
    part_of_speech = data['meanings'][0]['partOfSpeech']
    definition = data['meanings'][0]['definitions'][0]['definition']

    new_word = og_word + " " + part_of_speech
    return {
        "originalWord": og_word,
        "partOfSpeech": part_of_speech,
        "definition": definition,
        "word": new_word
    }

def add_to_data(new_word, data_path ):
    with open(data_path, 'r', encoding='utf-8') as f:
        words = json.load(f)

    if new_word in words:
        return

    new_word_data = get_word_data(new_word)
    words[new_word_data["originalWord"]] = new_word_data

    with open(data_path, 'w') as file:
        json.dump(words, file , indent=4)

if __name__ == '__main__':
    data_path = 'data.json'
    while True:
        add_to_data(input("Enter new word: "), data_path)
