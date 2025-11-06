import random
import string

import requests
import json

def create_word(word, part_of_speech, rules_path):
    if part_of_speech not in ['noun', 'adjective', 'adverb', 'verb']:
        return word
    with open(rules_path, 'r', encoding='utf-8') as f:
        rules = json.load(f)

    pattern  =  random.choice(rules["root"])

    root = ''
    for i in range(0, random.randint(1,3) ):
        for c in pattern:
            if c == 'c':
                root += random.choice(rules['consonants'])
            else:
                root += random.choice(rules['vowels'])


    return root + rules["suffixes"][part_of_speech]

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
        "word": create_word(og_word, part_of_speech, "word_rules.json")
    }

def add_to_data(add_word, data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    words = data['englishToNew']
    key = data['newToEnglish']

    if add_word in words:
        return words[add_word]['word']

    new_word_data = get_word_data(add_word)

    words[new_word_data["originalWord"]] = new_word_data
    key[new_word_data["word"]] = new_word_data["originalWord"]

    with open(data_path, 'w') as file:
        json.dump(data, file , indent=4)

    if add_word in words:
        return words[add_word]['word']
    else:
        return '!'

def convert(text, data_path):
    t = clean_string(text)
    words = t.split(" ")
    for i in range(0, len(words)):
        words[i] = add_to_data(words[i], data_path).lower()

    return " ".join(words)

def reverse(text, data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        key = data['newToEnglish']
    t = clean_string(text)
    words = t.split(" ")
    print(words)
    for i in range(0, len(words)):
        if words[i] in key:
            words[i] = key[words[i]]
        else:
            words[i] = '!'

    return " ".join(words)

def clean_string(text):
    t = text.lower()
    translator = str.maketrans('', '', string.punctuation)
    t = t.translate(translator)
    return t

if __name__ == '__main__':
    data_path = 'data.json'
    # while True:
    #     text = input("Enter a word: ")
    #     add_to_data(text, data_path)
    text = input("Enter the text : ").strip('\n')
    print (convert(text, data_path), end = '')
    print('\n')
    text = input("Enter the text : ").strip('\n')
    print(reverse(text, data_path))