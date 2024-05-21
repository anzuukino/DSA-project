from flask import render_template, Flask, request
import json
from trietree import PrefixTree

app = Flask(__name__, static_folder="statics")

dictionarya_v = {}
dictionaryv_a = {}

def Opendictionary(files):
    """
    Open a dictionary file and return its content as a dictionary object.

    Args:
        files (str): The name of the dictionary file (without extension).

    Returns:
        dict: A dictionary object containing the dictionary data.
    """
    dictionary = {}
    with open(f"database/{files}.json", "r") as file:
        dictionary = json.load(file)
    return dictionary

def Setup(trie, dictionary):
    """
    Set up a trie tree from a dictionary object.

    Args:
        trie (PrefixTree): The trie tree to populate.
        dictionary (dict): The dictionary object containing words, pronunciations, and definitions.

    Returns:
        None
    """
    for item in dictionary:
        word_i = item["word"]
        pronunciation = item["pronunciation"]
        definition = item["definition"]
        trie.insert(word_i, pronunciation, definition)

@app.route("/")
@app.route("/home")
def home():
    """
    Render the home page.

    Returns:
        str: The rendered HTML of the home page.
    """
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Handle search requests, using trie trees to find words.

    Returns:
        str: The rendered HTML of the search results page.
    """
    if request.method == "POST":
        txt = request.form["txt"].strip()
        translation_option = request.form["translation_option"]
    elif request.method == "GET":
        txt = request.args.get("txt").strip()
        translation_option = request.args.get("translation_option")

    if translation_option == "anh-viet":
        word, pronunciation, definition = triea_v.find(txt)
    elif translation_option == "viet-anh":
        word, pronunciation, definition = triev_a.find(txt)
    else:
        word, pronunciation, definition = "Not found", "", ""

    definition = definition.replace("\n", "<br>")
    pronunciation = f"/{pronunciation}/" if pronunciation else ""
    return render_template(
        "find.html",
        word=word,
        pronunciation=pronunciation,
        definition=definition,
        translation_option=translation_option,
    )

@app.route("/suggestion", methods=["GET"])
def suggestion():
    """
    Handle suggestion requests, using trie trees to suggest words.

    Returns:
        list: A list of suggested words.
    """
    word = request.args.get("word").lower().strip()
    translation_option = request.args.get("translation_option")
    if translation_option == "anh-viet":
        data = triea_v.starts_with(word)
    elif translation_option == "viet-anh":
        data = triev_a.starts_with(word)
    return data[0:10]

if __name__ == "__main__":
    """
    Main function to initialize the dictionaries and trie trees, and run the Flask app.
    """
    dictionaryv_a = Opendictionary("dbv-a")
    dictionarya_v = Opendictionary("dba-v")
    triea_v = PrefixTree()
    triev_a = PrefixTree()
    Setup(triea_v, dictionarya_v)
    Setup(triev_a, dictionaryv_a)
    app.run(host="0.0.0.0", port=1337)
