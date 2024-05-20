import json

with open("vietanh.txt", 'r') as file:
    content = file.read()

def get_word(dictionary_word):
    """
    Extract the word from the dictionary entry.

    Args:
        dictionary_word (str): A string representing a dictionary entry.

    Returns:
        str: The word extracted from the dictionary entry.
    """
    start = dictionary_word.find("@")
    end = dictionary_word.find("\n") if dictionary_word.find(" /") == -1 else dictionary_word.find(" /")
    word = dictionary_word[start+1:end]
    return word

def get_pronunciation(dictionary_word):
    """
    Extract the pronunciation from the dictionary entry.

    Args:
        dictionary_word (str): A string representing a dictionary entry.

    Returns:
        str: The pronunciation extracted from the dictionary entry, or an empty string if not found.
    """
    start = dictionary_word.find(' /')
    if start == -1:
        return ""
    end = dictionary_word.find("\n")
    pronunciation = dictionary_word[start+2:end-1]
    return pronunciation

def get_definition(dictionary_word):
    """
    Extract the definition from the dictionary entry.

    Args:
        dictionary_word (str): A string representing a dictionary entry.

    Returns:
        str: The definition extracted from the dictionary entry.
    """
    start = dictionary_word.find("\n")
    end = len(dictionary_word)
    definition = dictionary_word[start+1:end]
    return definition

def analyze(dictionary_word):
    """
    Analyze the dictionary entry and return a dictionary object.

    Args:
        dictionary_word (str): A string representing a dictionary entry.

    Returns:
        dict: A dictionary containing the word, pronunciation, and definition.
    """
    data = {
        'word': get_word(dictionary_word),
        'pronunciation': get_pronunciation(dictionary_word),
        'definition': get_definition(dictionary_word)
    }
    return data

def create_database(content):
    """
    Create a list of dictionary objects from the dictionary content.

    Args:
        content (str): A string representing the entire content of the dictionary file.

    Returns:
        list: A list of dictionaries, each containing the word, pronunciation, and definition.
    """
    dictionary = []
    start = 0
    while True:
        start = content.find("@", start)
        end = content.find("\n@", start + 1)
        if end == -1 or start == -1 or end < 0:
            break
        dictionary_word = content[start:end]
        dictionary.append(analyze(dictionary_word))
        start = end
    end = len(content)
    dictionary_word = content[start:end]
    dictionary.append(analyze(dictionary_word))
    return dictionary

dictionary = create_database(content)

with open("dbv-a.json", 'w') as file:
    json.dump(dictionary, file)
