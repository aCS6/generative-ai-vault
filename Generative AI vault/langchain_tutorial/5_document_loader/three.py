

# install beautifulsoup4, lxml

from langchain_community.document_loaders import BSHTMLLoader


loader = BSHTMLLoader(file_path="5_document_loader/data/sample.html")
mydata = loader.load()

# print(mydata)
print(mydata[0].page_content.replace('\n', ' '))