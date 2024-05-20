class TrieNode:
    def __init__(self, text='', pronunciation='', definition=''):
        """
        Initialize a TrieNode object.

        Args:
            text (str): The text of the node, default is an empty string.
            pronunciation (str): The pronunciation of the word at this node, default is an empty string.
            definition (str): The definition of the word at this node, default is an empty string.
        """
        self.text = text
        self.pronunciation = pronunciation
        self.definition = definition
        self.children = dict()
        self.iscomplete = False

class PrefixTree:
    def __init__(self):
        """
        Initialize a PrefixTree object.
        """
        self.root = TrieNode()

    def insert(self, word, pronunciation, definition):
        """
        Insert a word into the trie tree.

        Args:
            word (str): The word to be inserted.
            pronunciation (str): The pronunciation of the word.
            definition (str): The definition of the word.
        """
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
        """
        Find a word in the trie tree.

        Args:
            word (str): The word to be found.

        Returns:
            tuple: A tuple containing the word, its pronunciation, and its definition.
                   If the word is not found, returns ("Not found", "", "").
        """
        current = self.root
        for char in word:
            if char not in current.children:
                return "Not found", "", ""
            current = current.children[char]
        if current.iscomplete:
            return current.text, current.pronunciation, current.definition
        else:
            return "Not found", "", ""

    def child_words(self, node, words):
        """
        Get all words from a node in the trie tree.

        Args:
            node (TrieNode): The starting node.
            words (list): The list to collect words.

        Returns:
            None
        """
        if node.iscomplete:
            words.append(node.text)
        for letter in node.children:
            self.child_words(node.children[letter], words)

    def starts_with(self, prefix):
        """
        Get all words that start with a prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            list: A list of words that start with the given prefix.
        """
        words = []
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        self.child_words(current, words)
        return words