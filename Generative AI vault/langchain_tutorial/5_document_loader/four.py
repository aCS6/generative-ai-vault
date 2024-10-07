# install pypdf

from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader(file_path="5_document_loader/data/sample.pdf", extract_images=False)
mydata = loader.load()

print(mydata)
print(mydata[0].page_content)