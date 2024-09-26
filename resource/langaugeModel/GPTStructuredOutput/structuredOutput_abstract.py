from pydantic import BaseModel
from openai import OpenAI
import fitz  # PyMuPDF

# YOUR_API_KEY
client = OpenAI(api_key="YOUR_API_KEY")

class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

pdf_path = "./resource/langaugeModel/GPTStructuredOutput/researchPaper.pdf"
pdf_text = extract_text_from_pdf(pdf_path)

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
        {"role": "user", "content": pdf_text}
    ],
    response_format=ResearchPaperExtraction,
)

research_paper = completion.choices[0].message.parsed

# Print each field of the research paper on a new line
print(f"Title: {research_paper.title}")
print(f"Authors: {', '.join(research_paper.authors)}")
print(f"Abstract: {research_paper.abstract}")
print(f"Keywords: {', '.join(research_paper.keywords)}")