import re

def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")          # non-breaking space
    text = re.sub(r'\n{2,}', '\n', text)      # remove extra newlines
    text = re.sub(r'[•●▪■]', '-', text)       # normalize bullets
    text = re.sub(r'\s+', ' ', text)          # normalize spaces
    return text.strip()
