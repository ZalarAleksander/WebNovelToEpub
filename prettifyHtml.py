import re
from bs4 import BeautifulSoup

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


