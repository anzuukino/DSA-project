class TrieNode:
    def __init__(self,text = '',pronunciation='',definition=''):
        """Initialize a TrieNode object"""
        self.text = text
        self.pronunciation = pronunciation
        self.definition = definition
        self.children = dict()
        self.iscomplete = False
class PrefixTree:
    def __init__(self):
        """Initialize a PrefixTree object"""
        self.root = TrieNode()
    def insert(self, word, pronunciation, definition):
        """Insert a word into the trie tree"""
        current = self.root
        for i, char in enumerate(word):
            if char not in current.children:
                prefix = word[0:i+1]
                current.children[char] = TrieNode(prefix)
            current = current.children[char]
        current.iscomplete = True
        current.pronunciation = pronunciation
        current.definition = definition
    def find(self, word):
        """Find a word in the trie tree"""
        current = self.root
        for char in word:
            if char not in current.children:
                return "Not found","",""
            current = current.children[char]
        if current.iscomplete:
            return current.text, current.pronunciation, current.definition
        else:
            return "Not found","",""

    def child_words(self, node, words):
        """Get all words from a node in the trie tree"""
        if node.iscomplete:
            words.append(node.text)
        for letter in node.children:
            self.child_words(node.children[letter],words)
    def starts_with(self, prefix):
        """Get all words that start with a prefix"""
        words = list()
        current = self.root
        for char in prefix:
            if char not in current.children:
                return list()
            current = current.children[char]
        self.child_words(current, words)
        return words