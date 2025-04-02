
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)


def analyze_text(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    return {
        'lemmas': [token.lemma for token in doc.tokens],
        'pos_tags': [token.pos for token in doc.tokens]
    }


def generate_bot_response(text):
    analysis = analyze_text(text)

    if 'VERB' in analysis['pos_tags']:
        return "Расскажите подробнее о вашем действии."

    ...