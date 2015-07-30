# -*- coding: utf-8 -*-

import re
import pycorpora

# limited to parsing tags which have capital letter for 
# word with abbreviation to start with
def parse_hashtag(text):
    words = []
    text = text[1:]
    if not text[0].isupper() or text.isupper(): return text
    caps_pos = []
    for i in range(0, len(text)):
        if text[i].isupper():
            caps_pos.append(i)  # save positions of capital letters
        lst_len = len(caps_pos)
    for i in range(0, lst_len):
        if i != lst_len - 1:
            words.append(text[caps_pos[i]:caps_pos[i + 1]])
        elif i == lst_len - 1:
            words.append(text[caps_pos[i]:])
    return " ".join(words)

# @param texts <type="list">
# remove punctuation marks, urls, hyphens and parse hashtags
# @return list of text where each item is a list of words in the text
def purify_texts(texts, strip_html_entities=True, strip_html=False):
    to_del_ptrn = re.compile("http:\/\/|https:\/\/|www|@|\$|%|[0-9]{1,}")
    pure_texts = []
    # list contains only strings
    for j in range(0, len(texts)):
        # here each string becomes a list
        cp_text = texts[j]
        if strip_html: 
            cp_text = re.sub(r'<.*?>', " ", texts[j])
            cp_text = re.sub("\s{1,}", " ", cp_text)
        word_list = cp_text.strip().split(" ")
        pure_texts.append([]) 
        # iterate through words
        for i in range(0, len(word_list)): 
            if not to_del_ptrn.search(word_list[i]):
                if strip_html_entities:
                    pure_word = re.sub("[&#[a-zA-Z]{1,};|&#[a-zA-Z0-9]{1,};", " ", word_list[i])
                pure_word = re.sub("[!?,\"()\]\[\*]", "", pure_word)
                pure_word = re.sub("[-\+;…:~\.}{/\\\\]", " ", pure_word)                
                pure_word = re.sub("\s{1,}", " ", pure_word) 
                if len(pure_word) == 0: continue
                if pure_word[0] == " " or pure_word[-1] == " ": pure_word = pure_word.strip()
                if len(pure_word) == 0: continue
                if pure_word[0] == "#" and len(pure_word) > 1: pure_word = parse_hashtag(pure_word)
                if len(pure_word) > 2: 
                    pure_texts[j].append(pure_word.lower())
    return pure_texts 

# @param texts <type="list"> 
# where each element is a string
def concat_texts(texts):
    joined_text = ""
    for text in texts:
        joined_text += " ".join(text) 
        joined_text += " "
    return joined_text

'''
@tyshkev: for future machine learning extensibility
it may be better to count number of occurrences
for any word
'''
# @param text <type="str"> 
def count_word_frequency(text, target_keywords):
    word_freq_dict = {}
    text_list = text.split()
    for word in target_keywords:
        # exact match
        count = text_list.count(word)
        if count > 0: word_freq_dict[word] = count
    return word_freq_dict
  
def recursive_set_extend(items):
    new_tokens_set = set()
    for item in items:
        if "name" in item: 
            new_tokens_set.add(item["name"])
        if "categories" in item:
            new_tokens_set = new_tokens_set.union(recursive_set_extend(item["categories"]))
    return new_tokens_set

def extend_keywords_set_with_corpora(tokens_set, corps_names=None):
    if not corps_names: corps_names = ["rooms", "countries", "oceans", "seas",
            "rivers", "us_cities", "us_states", "canada_provinces",
            "canada_territories", "english_cities", "english_towns", "venues"]
    new_tokens_set = set().union(tokens_set)
    for corpus in corps_names:
        if corpus == "rooms":
            new_tokens_set = new_tokens_set.union(set(pycorpora.architecture.rooms["rooms"]))
        elif corpus == "countries":
            new_tokens_set = new_tokens_set.union(set(pycorpora.geography.countries["countries"]))
        elif corpus == "oceans":
            for desc in pycorpora.geography.oceans["oceans"]:
                new_tokens_set.add(desc["name"])
        elif corpus == "seas":
            for desc in pycorpora.geography.oceans["seas"]:
                new_tokens_set.add(desc["name"])
        elif corpus == "rivers":
            for desc in pycorpora.geography.rivers["rivers"]:
                new_tokens_set.add(desc["name"])
        elif corpus == "us_cities":
            for desc in pycorpora.geography.us_cities["cities"]:
                new_tokens_set.add(desc["city"])
        elif corpus == "us_states":
            for desc in pycorpora.geography.us_cities["cities"]:
                new_tokens_set.add(desc["state"])
        elif corpus == "canada_provinces":
            for item in pycorpora.geography.canada_provinces_and_territories["provinces"]:
                new_tokens_set.add(item)
        elif corpus == "canada_territories":
            for item in pycorpora.geography.canada_provinces_and_territories["territories"]:
                new_tokens_set.add(item)
        elif corpus == "english_cities":
             for item in pycorpora.geography.english_towns_cities["cities"]:
                new_tokens_set.add(item)
        elif corpus == "english_towns":
             for item in pycorpora.geography.english_towns_cities["towns"]:
                new_tokens_set.add(item)
        elif corpus == "venues":
           for item in pycorpora.geography.venues["categories"]:
               if "name" in item: new_tokens_set.add(item["name"])
               if "categories" in item:
                   new_tokens_set = new_tokens_set.union(recursive_set_extend(item["categories"]))
    # enforce utf8 encoding for words
    new_tokens_set = map(lambda x: x.encode('utf8'), new_tokens_set)
    return new_tokens_set
