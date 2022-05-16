import pandas as pd
import re

def clean_text(sentence:str) -> str:
    new_sentence = re.sub('[^0-9ㄱ-ㅣ가-힣a-zA-Z.,?! ]', '', sentence)
    return new_sentence

def split_sentence(paragraph:str) -> list:
    sentences = re.split(r'[.!?]', paragraph)
    #sentences = pd.Series(sentences)
    return sentences

if __name__ == '__main__':
    df = pd.read_csv("./dataset/posts.csv", header=None)
    print(df.head(5))
    print(df.info())
    print("=========dropna==========")
    
    df = df.dropna()
    print(df.info())
    
    df['paragraph'] = df[1].apply(lambda x: clean_text(x))
    print(df.head())
    
    brunch_sentence = []
    print(split_sentence(""""""))
    for p in df['paragraph']:
        brunch_sentence.append(split_sentence(p))

    brunch_sentence = pd.Series(brunch_sentence)
    print(brunch_sentence.head())