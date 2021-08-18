import json
import urllib.request
import time
import ssl
from threading import Thread,Lock

finished_count = 0

def count_letters(url, frequency,mutex):
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    mutex.acquire()
    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1
    global finished_count
    finished_count +=1
    mutex.release()

# 14 98 03 01 93 74

def main():
    frequency = {}
    mutex = Lock()
    start = time.time()
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    for i in range(1000, 1020):
        Thread(target=count_letters,args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency,mutex)).start()

    while True:
        mutex.acquire()
        if finished_count == 20:
            break
        mutex.release()
        time.sleep(0.5)
    end = time.time()
    print(start,end)
    print(json.dumps(frequency, indent=4))
    print("Done, time token", end - start)

main()