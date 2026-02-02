import cloudscraper
import random
import time
import prettifyHtml

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    },
    interpreter='nodejs', 
    delay=5,               
    debug=False
)
def updateAvaliableEasternNovelList():
    try:
        response = scraper.get("https://freewebnovel.com/sitemap.xml", timeout=30)
        if response.status_code == 200 and len(response.text) > 2000:
            html = response.text
            novelList = prettifyHtml.saveEasternNovelNames(html)
            if novelList:
                print("Successfully updated!")
                return novelList
            else:
                return False
            
    except Exception as exc:
        print(f"error - {exc}, check connection")
        return False


def scrapeChaptersNovelBin(url):  # add #tab-chapters-title
    url = url + "#tab-chapters-title"
    response = scraper.get(url, timeout=30)
    html = response.text
    chapterUrlArr = prettifyHtml.extractChapterList(html)
    
    return chapterUrlArr

def autoSearchNovel(name):
    name = name.replace(" ", "-")
    baseUrlArr = [
        "https://freewebnovel.com/novel/",
        "https://novelfire.net/book/",
        "https://novelbin.me/novel-book/"
    ]
    for index, base in enumerate(baseUrlArr):
        url = base + name
        try:
            response = scraper.get(url, timeout=30) 
        except Exception as exc:
            print(f"error - {exc}, check connection")
            return False
        if index == 2:
            if response.status_code == 404:
                print("Novel not found on NovelBin")
            else:
                chapterUrlArr = scrapeChaptersNovelBin(url)
                return chapterUrlArr
        else:
            if not response.status_code == 404:
                if index == 1:
                    lastChapter = int(prettifyHtml.findLastChapterNovelFire(response.text)) + 1
                    print("Collected the chapters from NovelFire")
                elif index == 0:
                    lastChapter = int(prettifyHtml.findLastChapterFreeWebNovel(response.text)) + 1
                    print("Collected the chapters from FreeWebNovel")

                chapterUrlArr = []    
                for i in range(1,lastChapter):
                    chapterUrlArr.append(f"{url}/chapter-{i}")
                print(f"Novel found on: {base}")
                return chapterUrlArr
            else:
                print(f"Novel not found on: {base}")
    print("Novel not found!")
    return False

def scrapeChapters(chapterUrlArr): 
    failedChapters = []
    bookData = {}
    estimatedTime = len(chapterUrlArr) * 4.5
    print(f"Estimated collection time: {int(estimatedTime)}s")
    startTime = time.perf_counter()
    for index, chapterUrl in enumerate(chapterUrlArr):
        success = False
        retries = 0
        while not success and retries < 5:
            try:
                response = scraper.get(chapterUrl, timeout=30)
                if response.status_code == 200:
                    if len(response.text) > 2000:
                        textHTML = response.text
                        success = True
                    else:
                        print(f"Didnt get content from {chapterUrl}")
                        retries += 1
                elif response.status_code == 429:
                    wait = (2 ** retries) * 2 + random.uniform(0, 5)
                    print(f"329 Too fast {wait:.1f}")
                    time.sleep(wait)
                    retries += 1
                elif response.status_code == 403:
                    print(f"403 Forbidden IP or fingerprint flagged {chapterUrl}")
                    retries += 1
                    time.sleep(random.uniform(10, 20))
                else:
                    print(f"Unexpected Error {response.status_code} on {chapterUrl}")
                    retries += 1
                    time.sleep(5)
            except Exception as exc:
                print(f"error - {exc}")
                time.sleep(15)
                retries += 1
        if success:
            cleanHTML = prettifyHtml.cleanText(textHTML)
            bookData[index] = {
                'title': f"Chapter {index + 1}",
                'content': cleanHTML
            }
            del textHTML
            print(f"found chapter waiting for ~4s")
            time.sleep(random.uniform(2, 6))
            
        else:
            failedChapters.append(chapterUrl)
    endTime = time.perf_counter()
    actuaTime = endTime - startTime
    print(f"Estimated time: {int(estimatedTime)}s vs actual time: {int(actuaTime)}s taken!")
    return bookData, failedChapters
