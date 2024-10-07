from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path="5_document_loader/data/sample.csv", encoding="utf-8")
mydata = loader.load()

print(mydata)

for content in mydata:
    print("-------------------")
    print(content.page_content)
