from langchain_community.document_loaders import TextLoader

loader = TextLoader("5_document_loader/data/sample.txt", encoding="utf-8")
mydata = loader.load()

print(mydata)
print(mydata[0].page_content)
