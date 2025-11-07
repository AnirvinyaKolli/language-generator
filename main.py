import random
import string
import requests
import json
import time


def create_word(word, part_of_speech, rules_path):

    with open(rules_path, 'r', encoding='utf-8') as f:
        rules = json.load(f)

    if part_of_speech not in rules['suffixes']:
        print(part_of_speech)
        return word

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
    elif response.status_code == 429:
        time.sleep(0.3)
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
        "word": create_word(og_word, part_of_speech, "saved_data/word_rules.json")
    }

def add_to_data(add_word, data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    words = data['englishToNew']
    key = data['newToEnglish']

    if add_word in words:
        return

    new_word_data = get_word_data(add_word)

    words[new_word_data["originalWord"]] = new_word_data
    key[new_word_data["word"]] = new_word_data["originalWord"]

    with open(data_path, 'w') as file:
        json.dump(data, file , indent=4)

    
def add_to_data_bulk(add_words, data_path , data):

    print (add_words)
    words = data['englishToNew']
    key = data['newToEnglish']

    for add_word in add_words:
        if add_word in words:
            continue
        new_word_data = get_word_data(add_word)
        words[new_word_data["originalWord"]] = new_word_data
        key[new_word_data["word"]] = new_word_data["originalWord"]

    with open(data_path, 'w') as file:
        json.dump(data, file , indent=4)


def convert(t, data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        key = data['englishToNew']
        
    t = clean_string(t)
    words = t.split(" ")

    add_to_data_bulk(words, data_path, data)

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        key = data['englishToNew']
    
    for i in range(0, len(words)):
        if words[i] in key:
            words[i] = key[words[i]]['word']


    return " ".join(words)

def reverse(t, data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        key = data['newToEnglish']
    t = clean_string(t)
    words = t.split(" ")
    for i in range(0, len(words)):
        if words[i] in key:
            words[i] = key[words[i]]
        else:
            words[i] = words[i]

    return " ".join(words)

def clean_string(t):
    t = t.lower()
    translator = str.maketrans('', '', string.punctuation + string.digits)
    t = t.translate(translator)
    return t

if __name__ == '__main__':
    dp = 'saved_data/data.json'
    text = input("Enter the text : ").strip('\n')
    start = time.time()
    print (convert(text, dp))
    end = time.time()
    print(f"Execution time: {end - start:.4f} seconds")