import re
from bs4 import BeautifulSoup


def contains_url(string):
    pattern = r"[http[s]?://]?[www\.]?[a-zA-Z|0-9]{3,30}[\.][a-z]{3,20}[(/a-z)]?"
    match = re.search(pattern, string)
    return bool(match)


def getTags(htmlContent):
    if htmlContent.find("<body") != 0:
        soup = BeautifulSoup(htmlContent, "html.parser")
        htmlContent = str(soup.find_all("body")[0])
        
    soup = BeautifulSoup(htmlContent, "html.parser")
    tags = soup.find_all()
    tags = list(map(str, tags))
    return tags


def getWords(s):
    words = re.sub("<\\//.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words


def parseAnswerTextSpacing(s):
    # Lowercase version
    words = re.sub("-", " ", s.lower().strip())
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words