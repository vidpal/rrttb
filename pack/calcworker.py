# -*- coding: utf8 -*-

def get_words_local_scores(words_freq_dict, rank):
    return {key: words_freq_dict[key] * rank for key in words_freq_dict}

def get_words_global_scores(local_scores):
    global_words_set = set()
    global_words_scores = {}
    for local in local_scores:
        # use sets to avoid repetition
        global_words_set = global_words_set.union(set(local.keys()))
    global_words_scores = {word: 0 for word in global_words_set}
    for word in global_words_scores:
        for local in local_scores:
            if word not in local:
                continue
            else:
                global_words_scores[word] += local[word]
    return global_words_scores

def get_document_score(words_frequencies, words_scores):
    total_score = 0
    match_count = 0
    matched_words = []
    # if document didn't contain any target keywords
    if len(words_frequencies) == 0: return (0, 0, [])
    for word in words_scores:
        if word in words_frequencies:
            total_score += words_frequencies[word] * words_scores[word]
            match_count += words_frequencies[word] 
            matched_words.append(word)
    return (total_score, match_count, matched_words)

def get_users_ranks(users_stats):
    users_total_scores = [] 
    max_score = 0
    leader = ""
    for user in users_stats:
        if not user: continue
        users_total_scores.append({"screen_name": user["screen_name"], 
            "score": (user["followers_count"] * 0.7 + user["list_count"] * 0.2 
            + user["retweet_count"] * 1)})
        if users_total_scores[-1]["score"] > max_score:
            leader = user["screen_name"]
            max_score = users_total_scores[-1]["score"] 
    users_ranks = {leader: 5.0}
    for i in range(0, len(users_total_scores)):
        if users_total_scores[i]["screen_name"] == leader: continue
        users_ranks[users_total_scores[i]["screen_name"]] = ((users_total_scores[i]["score"] * 5.0) / max_score) 
    return users_ranks



