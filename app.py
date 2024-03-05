import spacy
from spacy.matcher import Matcher

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()
with open('example/uiux.pdf', 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

value = output_string.getvalue()

def extract_names(text):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    return names

def create_titles():
    nlp = spacy.load("en_core_web_lg")
    matcher = Matcher(nlp.vocab)

    job_title_patterns = [
        [{"LOWER":"software"}, {"LOWER":"engineer"}],
        [{"LOWER":"project"}, {"LOWER":"manager"}],
    ]

    matcher.add("JOB_TITLE", job_title_patterns)
    doc = nlp(value) 
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id] 
        span = doc[start:end] 
        print(string_id, span.text)

names = extract_names(value)
print("Names found in the pdf:")
for name in names:
    print(name)