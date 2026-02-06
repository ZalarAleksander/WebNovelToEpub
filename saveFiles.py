from ebooklib import epub
import uuid
import os
import re

def saveToEpub(dataDict):
    sortedDict = [dataDict[i] for i in sorted(dataDict)]

    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    title = input("Input the title of the novel: ")
    book.set_title(title)
    book.set_language("en")
    book.add_author("RalazScrapes")

    chapterList = []
    for i, chapterData in enumerate(sortedDict):
        chapter = epub.EpubHtml(
            title = chapterData['title'],
            file_name=f'chapter-{i+1}.xhtml',
            lang='en'
        )
        htmlContent = f"<h1>{chapterData['title']}</h1>"
        for line in chapterData['content'].split('\n'):
            line = line.strip()
            if line:
                htmlContent += f"<p>{line}</p>"
        chapter.content = htmlContent
        book.add_item(chapter)
        chapterList.append(chapter)
    book.toc = tuple(chapterList)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapterList
    fileName = f"{title.replace(' ', '_')}.epub"
    epub.write_epub(fileName, book, {})
    print(f"Finished writing {fileName}")

def makeChapterHtml(chapterDict, folderName, title):
    htmlHead = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>{title} {chapterDict['title']}</title>
            <link rel="stylesheet" href="../chapterStyle.css">
            <script src="../chapterScript.js"></script>
        </head>
        <body>
        <header></header>
        <h2>{title}</h2>
        <div id='chContent'>"""
            
    htmlFoot = """
            \n</div>
            <footer></footer>
        </body>
    </html>"""
    paragraphHtml = [f"<p>{x}</p>" for x in chapterDict['content']]
    paragraphStr = f"\n<h3>{chapterDict['title']}</h3>" + "\n".join(paragraphHtml)
    fullHtml = htmlHead + paragraphStr + htmlFoot
    filePath = f"novelCollection/{folderName}/{chapterDict['title']}.html"
    with open(f"{filePath}", 'w', encoding = "utf-8") as file:
        file.write(fullHtml)

def makeHtmlNovelNav(dataDict, folderName, title):
    htmlHead = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Navigation {title}</title>
            <link rel="stylesheet" href="../navigationStyle.css">
            <script src="../navigationScript.js"></script>
        </head>
        <body>
            <header></header>
            <h1>Navigation {title}</h1>
            <ul>\n"""
    htmlFoot = """
            \n</ul>
            <footer></footer>
        </body>
    </html>"""
    hrefStr = ""
    for chapter in dataDict:
        hrefStr += f"<li><a href = '{chapter['title']}.html'>{chapter['title']}</a></li>"
    fullHtml = htmlHead + hrefStr + htmlFoot
    path = f"novelCollection/{folderName}/Navigation.html"
    with open(path, 'w', encoding="utf-8") as file:
        file.write(fullHtml)

def saveToHtml(dataDict):
    sortedDict = [dataDict[i] for i in sorted(dataDict)]
    title = input("Input the title of the novel: ")
    folderName = re.sub(r"[)':!?(,‘'’\"“”]", "", title.strip()).lower()
    folderName = folderName.replace(' ', '-')
    os.mkdir(f"NovelCollection/{folderName}")
    for singleDict in sortedDict:
        makeChapterHtml(singleDict, folderName, title)
    makeHtmlNovelNav(sortedDict, folderName, title)
    
    
        

