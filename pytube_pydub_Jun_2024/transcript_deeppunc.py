import sys
import warnings

# pip install spacy
# python -m spacy download en_core_web_sm
# python -m spacy download en_core_web_md
# python -m spacy download en_core_web_lg
import spacy

# https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large
from deepmultilingualpunctuation import PunctuationModel

warnings.filterwarnings(
	"ignore", 
	category=UserWarning, 
	message="`grouped_entities` is deprecated and will be removed in version v5.0.0, defaulted to `aggregation_strategy=\"none\"` instead."
)

nlp = spacy.load("en_core_web_lg")

def capitalize_sentences(text):
    sentences = text.split('. ')
    capitalized_sentences = [sentence.capitalize() if sentence else '' for sentence in sentences]
    capitalized_text = '. '.join(capitalized_sentences)
    return capitalized_text

def capitalize_proper_nouns(text):
    doc = nlp(text)
    entity_labels = {
        "WORK_OF_ART", "PERSON", "PER", "CARDINAL", "DATE", "EVENT", "FAC", 
        "GPE", "LANGUAGE", "LOC", "MONEY", "NORP", "ORDINAL", "ORG", "PERCENT",
        "PRODUCT", "QUANTITY", "TIME", "MISC", "LAW"
    }
    for ent in doc.ents:
        if ent.label_ in entity_labels:
            text = text.replace(ent.text, ' '.join([w.capitalize() for w in ent.text.split()]))
    return text

def insert_paragraph_breaks(text, sentences_per_paragraph=4):
    sentences = text.split('. ')
    paragraphs = []
    paragraph = []
    for i, sentence in enumerate(sentences, start=1):
        paragraph.append(sentence)
        if i % sentences_per_paragraph == 0:
            paragraphs.append('. '.join(paragraph) + '.')
            paragraph = []
    if paragraph:
        paragraphs.append('. '.join(paragraph) + '.')
    return '\n\n'.join(paragraphs)

def uppercase_i_variations(text):
    words = text.split()
    modified_words = [word.capitalize() if word.lower() in {"i", "i'm", "i'd", "i've", "i'll"} else word for word in words]
    modified_text = ' '.join(modified_words)
    return modified_text


model = PunctuationModel()
with open('cls_trans.txt', 'r') as file:
    text = file.read()

punctuated_text = model.restore_punctuation(text)
capitalized_sentences_text = capitalize_sentences(punctuated_text)
text_with_proper_nouns = capitalize_proper_nouns(capitalized_sentences_text)
text_with_uppercase_i = uppercase_i_variations(text_with_proper_nouns)
final_text_with_paragraphs = insert_paragraph_breaks(text_with_uppercase_i)
print(final_text_with_paragraphs)

