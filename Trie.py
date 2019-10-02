import random

class TrieNode():
    def __init__(self, char: str):
        self.char = char
        self.children = []   # child nodes
        self.word_end = False    # if the word ends at this node
        self.words = set() # words in and below this node
        
def add(root, word: str):
    node = root
    for char in word:
        found = False
        for child in node.children:
            if child.char == char:
                child.words.add(word)
                node = child
                found = True
                break
                
        if not found:
            new_node = TrieNode(char)
            new_node.words.add(word)
            node.children.append(new_node)
            node = new_node
            
    node.word_end = True

def find_prefix(root, prefix: str):
    node = root
    
    if not root.children:
        return False, set()
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
        if char_not_found:
            return False, set()
    return True, node.words

def database_to_trie(database):
    root = TrieNode('*')
    for word in database:
        add(root, word)
    return root

def generate_name(n):
    name = ""
    for i in range(n):
        name += chr(random.randint(97,122))
    return name

def generate_database(N):
    database = []
    for i in range(N):
        database.append(generate_name(random.randint(4,8)))
    return database