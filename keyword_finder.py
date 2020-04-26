import requests
import re


# checks if url is interesting
def find_words(words, url, common):
    r = requests.get(url)
    count = 0
    for w in words:
        if re.search(w, r.text):
            count += 1
    return count >= common
