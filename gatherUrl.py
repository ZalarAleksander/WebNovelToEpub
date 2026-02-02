import collectChapters
import saveEpub
import re

def selectWebsite():
    print("\n1 - Eastern novels")
    print("2 - Western novels -- DOESNT WORK YET")
    
    selection = int(input("\nWhich kind are you searching for: "))
    return selection

def projectGutenbergSearch():
    print("jes")

def manualLinkInput():
    print("For now only search on novelfire.net and freewebnovel.com")
    novelUrl = input("Input the url to the novel: ")
    lastChapter = int(input("Input the last chapter number: "))
    chapterUrlArr = []
    i = 1
    while i <= lastChapter:
        currChapterUrl = novelUrl + "/chapter-" + str(i)
        chapterUrlArr.append(currChapterUrl)
        i = i + 1
    return chapterUrlArr

def findEasternNovel():
    novelName = input("Input the novel you want to find format('this novel name'):")
    novelName = novelName.strip()
    novelName = re.sub(r"[)':!?(,‘'’\"“”]", "", novelName)
    novelName = novelName.replace(" ", "-")
    novelName = novelName.lower()
    
    autoCheckResult = collectChapters.autoSearchNovel(novelName)
    if autoCheckResult == False:
        print("Manual link only works from NovelFire and NovelBin")
        decision = input("\nDo you want to input the link to the first chapter manually? y/n")
        if not decision == "y":
            print("Goodbye!")
            return False 
        else:
            chapterUrlArr = manualLinkInput()
            return chapterUrlArr
    else:
        return autoCheckResult
    
def findWesternNovel():
    print("ok")    

def selectNovelType(): 
    checkSelection = False
    while checkSelection == False:
        selection = selectWebsite()
        if selection in [1,2]:
            checkSelection = True
    match selection:
        case 1:
            chapterUrlArr = findEasternNovel()
            if chapterUrlArr == False:
                return False
        case 2:
            return False
            findWesternNovel()
    
    data, fail = collectChapters.scrapeChapters(chapterUrlArr)
    if fail:
        data2, fail2 = collectChapters.scrapeChapters(fail)
        data.update(data2)
        if fail2:
            data3, fail3 = collectChapters.scrapeChapters(fail2)
            data.update(data3)
            for fails in fail3:
                print(f"Failed: {fails}")
    saveEpub.saveToEpub(data)