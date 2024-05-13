from flask import render_template, Flask, request
import json
from trietree import PrefixTree

app = Flask(__name__, static_folder="statics")

dictionarya_v = {}
dictionaryv_a = {}


def Opendictionary(files):
    """Open dictionary file and return a dictionary object"""
    dictionary = dict()
    with open(f"database/{files}.json", "r") as file:
        dictionary = json.load(file)
    return dictionary


def Setup(trie, dictionary):
    """Setup trie tree from dictionary file"""
    for item in dictionary:
        word_i = item["word"]
        pronunciation = item["pronunciation"]
        definition = item["definition"]
        trie.insert(word_i, pronunciation, definition)


# Khai bao cac endpoint
@app.route("/")
@app.route("/home")
def home():
    """Home page"""
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    """Handle search request, using trie tree to find words"""
    if request.method == "POST":
        txt = request.form["txt"]
        translation_option = request.form["translation_option"]
    elif request.method == "GET":
        txt = request.args.get("txt")
        translation_option = request.args.get("translation_option")
    if translation_option == "anh-viet":
        word, pronunciation, definition = triea_v.find(txt)
    elif translation_option == "viet-anh":
        word, pronunciation, definition = triev_a.find(txt)
    else:
        word, pronunciation, definition = "Not found", "", ""

    print(word, pronunciation, definition)
    definition = definition.replace("\n", "<br>")
    pronunciation = "/" + pronunciation + "/" if pronunciation != "" else ""
    return render_template(
        "find.html",
        word=word,
        pronunciation=pronunciation,
        definition=definition,
        translation_option=translation_option,
    )


@app.route("/suggestion", methods=["GET"])
def suggestion():
    """Handle suggestion request, using trie tree to suggest words"""
    word = request.args.get("word").lower()
    translation_option = request.args.get("translation_option")
    if translation_option == "anh-viet":
        data = triea_v.starts_with(word)
    elif translation_option == "viet-anh":
        data = triev_a.starts_with(word)
    return data[0:10]


if __name__ == "__main__":
    """Main function"""
    dictionaryv_a = Opendictionary("dbv-a")
    dictionarya_v = Opendictionary("dba-v")
    triea_v = PrefixTree()
    triev_a = PrefixTree()
    Setup(triea_v, dictionarya_v)
    Setup(triev_a, dictionaryv_a)
    # print(trie.starts_with('Yu'))
    app.run(host="0.0.0.0", port=1337)
