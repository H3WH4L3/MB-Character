from pypdf import PdfReader

reader = PdfReader("test.pdf")
page = reader.pages[0]
print(page.mediabox)