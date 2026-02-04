from ebooklib import epub
import uuid

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

