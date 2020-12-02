from bs4 import BeautifulSoup
import requests

# create urls
urls = []

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
years = ["2019", "2020"]

for m in months:
    url = "https://spellingbeeanswers.com/spelling-bee-%s-" % m
    for d in range(1, 32):
        url += "%d-" % d
        for y in years:
            url += "%s-answers" % y
            urls.append(url)
            url = url[:-12]
        if d < 10: url = url[:-2]
        else: url = url[:-3]
    url = url[:-len(m)]

all_words = []

# if slow, just do ~100 words at a time and remove duplicates
for url in urls:
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        answers = soup.find_all(class_="aanswer")
        for word in answers:
            if word not in all_words:
                all_words.append(word.get_text())
    else: continue

f = open("wordlist.txt", "w")
for word in all_words:
    f.write(word + '\n')
f.close()


