import pandas as pd
from collections import defaultdict

def preprocess(path):
    file = open(path, encoding="utf8")
    return [line for line in file if line != '\n']

def get_dict(corpus):
    data = defaultdict(list)
    for line in corpus:
        line = line[:-1]
        tokens = line.split(" ", 1)
        data[tokens[0]].append(tokens[1])
    return data

def predict(input):
    ''' Prediction words
    We check if the input contains a key(verb) of the dictionary.
    Then check if the input is contained in an element of the value list of the key.
    Return the most used prediction.
    '''
    tokens = input.split(" ", -1)

    # get the last verb index and the rest of input phrase
    verb = ""
    remain = ""
    for i in reversed(range(len(tokens))):
        if (tokens[i] in dict_data):
            verb = tokens[i]
        if (verb != ""):
            remain = input.split(verb, -1)[-1]
            remain = remain[1:]
    
    if (verb == ""):
        return []

    # calculate preds checking if remain is in line
    preds = {}
    values = dict_data.get(verb)
    for line in values:
        if (remain in line):
            pred = line.split(remain, 1)[1]
            pred = pred[1:]
            preds[pred] = preds[pred]+1 if pred in preds else 1
    
    return sorted(preds.items(), key=lambda x: x[1], reverse=True)

def print_dict(n, dict_data):
    dict_n = {k: dict_data[k] for k in list(dict_data)[:n]}
    print(dict_n)

corpus = preprocess("server/model/data/sentences_vision.txt")
dict_data = get_dict(corpus)

# prediction = predict("view for")
# print(prediction)

# def main():
#     corpus = preprocess("server/model/data/sentences_vision.txt")
#     dict_data = get_dict(corpus)
#     print_dict(2, dict_data)

# if __name__ == "__main__":
#     main()