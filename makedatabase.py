import json

with open("database/vietanh.txt", 'r') as file:
    content = file.read()

def get_word(dictionary_word):
    """Get word from dictionary word"""
    start = dictionary_word.find("@")
    end = dictionary_word.find("\n") if dictionary_word.find(" /") == -1 else dictionary_word.find(" /")
    word = dictionary_word[start+1:end]
    return word
def get_pronunciation(dictionary_word):
    """Get pronunciation from dictionary word"""
    start = dictionary_word.find(' /')
    if start == -1: return ""
    end = dictionary_word.find("\n")
    pronunciation = dictionary_word[start+2:end-1]
    return pronunciation
def get_definition(dictionary_word):
    """Get definition from dictionary word"""
    start = dictionary_word.find("\n")
    end = len(dictionary_word)
    definition = dictionary_word[start+1:end]
    return definition
def analyze(dictionary_word):
    """Analyze dictionary word and return a dictionary object"""
    data ={
        'word':get_word(dictionary_word),
        'pronunciation':get_pronunciation(dictionary_word),
        'definition':get_definition(dictionary_word)
    }
    # print(data)
    dictionary = dict()
    for key, value in data.items():
        dictionary[key] = value
    
    return dictionary
def create_database(content,start=0,end=1):
    """Create a dictionary object from dictionary content"""
    dictionary = list()
    while True:
        start = content.find("@",start)
        end = content.find("\n@",start+1)
        if end == -1 or start == -1 or end < 0:
            break
        # print(start,end)
        dictionary_word = content[start:end]
        # print(dictionary_word)
        dictionary.append(analyze(dictionary_word))
        # print(dictionary)
        start = end
    end = len(content)
    # print(start,end)
    dictionary_word = content[start:end]
    # print(dictionary_word)
    dictionary.append(analyze(dictionary_word))
    # print(dictionary)
    return dictionary

dictionary=create_database(content)
# print(dictionary)

with open("database/dbv-a.json",'w') as file:
    json.dump(dictionary,file)