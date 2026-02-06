import re
from bs4 import BeautifulSoup
from datetime import datetime

# https://freewebnovel.com/novel/saving-system-calm-down-my-fleeing-host

def getEasternNovelNames():
    try:
        with open("novelList.txt", 'r') as file:
            firstLine = file.readline()
            if firstLine:
                novelNameArr = [line.strip() for line in file]
                return novelNameArr
        return False        
    except Exception as exc:
        print(f"There was an error in getEasternNovelNames! - {exc}")
        return False

def saveEasternNovelNames(html):
    try:
        with open("novelList.txt", 'w', encoding="utf-8") as file:
            dateNow = datetime.now()
            cuteDate = dateNow.strftime("%d %B %Y")
            file.write(f"{cuteDate}\n")
            soup = BeautifulSoup(html, 'xml')
            novelList = []
            for url in soup.find_all('loc'):
                tempUrl = url.text
                match = re.search(r"novel/(.+)", tempUrl)
                if match:
                    finalName = match.group(1)
                    finalName = re.sub('-', " ", finalName)
                    file.write(f"{finalName}\n")
                    novelList.append(finalName)
            return novelList
    except Exception as exc:
        print(f"There was an error in saveEasternNovelNames! - {exc}")
    

def extractChapterList(html):
    soup = BeautifulSoup(html, 'html.parser')
    inDiv = soup.find('div', id='chapter-archive')
    chapterUrlArr = []
    for link in inDiv.find_all('a', href=True):
        chapterUrlArr.append(link['href'])
    return chapterUrlArr

def findLastChapterNovelFire(html):
    soup = BeautifulSoup(html, 'html.parser')
    classHeaderStats = soup.find('div', class_='header-stats')
    strongContent = classHeaderStats.find('strong').get_text(strip=True)
    lastChapter = int(strongContent)
    return lastChapter

def findLastChapterFreeWebNovel(html):
    soup = BeautifulSoup(html, 'html.parser')
    latestChapters = soup.find('div', class_='m-newest1')
    lastChapterA = latestChapters.find('a', href=True)
    lastChapterUrl = lastChapterA['href']
    findNum = re.search(r"chapter-(.+)", lastChapterUrl)
    lastChapter = findNum.group(1)
    return lastChapter

def cleanText(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = (
        soup.find('div', id='chr-content') or # for NovelBin
        soup.find('div', class_='txt') or # for FreeWebNovel
        soup.find('div', id='content') # for NovelFire
    )
    if content:
        for script in content(["script", "style"]):
            script.decompose()
    final = content.get_text(separator='\n\n', strip=True)
    return final


