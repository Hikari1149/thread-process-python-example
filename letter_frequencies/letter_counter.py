import json
import urllib.request
import time
import ssl
from threading import Lock


def count_letters(url, frequency):
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    print(response,txt)
    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1


def main():
    frequency = {}

    start = time.time()
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    print(start)
    for i in range(1000, 1020):
        count_letters(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency)

    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("Done, time token", end - start)

main()