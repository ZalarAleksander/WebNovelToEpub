import collectChapters
import saveFiles
import prettifyHtml
import re
from datetime import datetime

def selectWebsite():
    print("\n1 - Eastern novels")
    print("2 - Western novels -- DOESNT WORK YET")
    selection = int(input("\nWhich kind are you searching for: "))
    return selection

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
    try:
        with open("novelList.txt", 'r') as file:
            option = input(f"Last update: {file.readline().strip()}, do you wish to update the file list? (y,n): ")
            if option == 'y':
                avaliableNovelList = collectChapters.updateAvaliableEasternNovelList()    
            else:
                avaliableNovelList = prettifyHtml.getEasternNovelNames()
    except Exception as exc:
        print("The file doesnt exist. Making it now!")
        avaliableNovelList = collectChapters.updateAvaliableEasternNovelList()
    
    novelName = input("Input the novel you want to find, format:'this novel name': ")
    novelName = re.sub(r"[)':!?(,‘'’\"“”]", "", novelName.strip()).lower()
    if avaliableNovelList:
        possibleNovelList = [name for name in avaliableNovelList if novelName in name]
        for index, possibleNovel in enumerate(possibleNovelList):
            print(f"{possibleNovel} - {index + 1}")
        choice = int(input("Select the novel you want by typing in the number: "))
        if choice == int(choice) and choice <= len(possibleNovelList):
            novelName = possibleNovelList[choice - 1]
    else:
        print("Couldn't access the novel list")
    autoCheckResult = collectChapters.autoSearchNovel(novelName)
    if autoCheckResult == False:
        print("Manual link only works from NovelFire and NovelBin")
        decision = input("\nDo you want to input the link to the first chapter manually? y/n: ")
        if not decision == "y":
            print("Goodbye!")
            return False 
        else:
            chapterUrlArr = manualLinkInput()
            return chapterUrlArr
    else:
        return autoCheckResult

def selectSaveType():
    print("\n1 - Save to HTML - WebApp")
    print("2 - Save to Epub - Local")
    selection = int(input("\nWhat kind do you want to save: "))
    return selection

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
    
    
    checkSelection = False
    title = input("Input the novel name: ")
    while checkSelection == False:
        selection = selectSaveType()
        if selection in [1,2]:
            checkSelection = True
    data, fail = collectChapters.scrapeChapters(chapterUrlArr)
    if fail:
        data2, fail2 = collectChapters.scrapeChapters(fail)
        data.update(data2)
        if fail2:
            data3, fail3 = collectChapters.scrapeChapters(fail2)
            data.update(data3)
            for fails in fail3:
                print(f"Failed: {fails}")
    if selection == 1:
        saveFiles.saveToHtml(data, title)
    else:
        saveFiles.saveToEpub(data, title)