import json
import random
import sys


def read_misspellings(filename):
    # read in a list of {"src": "trickz", "tgt": "tricks"} objects and
    # output a ditionary of {"tricks": ["trickz"]} objects
    dict = {}
    with open(filename) as f:
        for line in f:
            obj = json.loads(line)
            if obj["tgt"] not in dict:
                dict[obj["tgt"]] = []
            dict[obj["tgt"]].append(obj["src"])
    return dict


def tokenize_sentence(sentence):
    # split at punctuation and spaces
    # return a list of tokens
    tokens = []
    token = ""
    for c in sentence:
        if c.isalpha():
            token += c
        else:
            if token != "":
                tokens.append(token)
                token = ""
            tokens.append(c)
    if token != "":
        tokens.append(token)
    return tokens


def extract_and_misspell(sentence, dict):
    # extract words from sentence and misspell them
    words = tokenize_sentence(sentence)  # sentence.split()
    # print(words)
    new_words = []
    for word in words:
        if word in dict:
            new_words.append(random.choice(dict[word]))
        else:
            new_words.append(word)
    return "".join(new_words)


def main():
    dict = read_misspellings("misspellings.jsonl")
    # read lines from stdin
    for line in sys.stdin:
        sentence = line.strip()
        print(extract_and_misspell(sentence, dict))


if __name__ == "__main__":
    main()
