import re
import textwrap

def add_paragraphs(transcribed_text, sentences_per_paragraph=5, line_width=70):
    # normalize spaces
    transcribed_text = re.sub(r'\s+', ' ', transcribed_text).strip()
    
    # split the text into sentences, keeping the punctuation with the sentence
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
    sentences = sentence_endings.split(transcribed_text)

    paragraphs = []
    for i in range(0, len(sentences), sentences_per_paragraph):
        paragraph = ' '.join(sentences[i:i + sentences_per_paragraph]).strip()
        wrapped_paragraph = textwrap.fill(paragraph, width=line_width)
        paragraphs.append(wrapped_paragraph)

    formatted_text = '\n\n'.join(paragraphs)

    # ensure the last sentence has punctuation
    if not re.search(r'[.!?]$', formatted_text.strip()):
        formatted_text += '.'

    return formatted_text

with open('output.txt', 'r') as file:
    transcribed_text = file.read()

formatted_text = add_paragraphs(transcribed_text, sentences_per_paragraph=3, line_width=70)

with open('formatted_output.txt', 'w') as file:
    file.write(formatted_text)

print("Formatted text with paragraphs and line wrapping has been saved to 'formatted_output.txt'.")
