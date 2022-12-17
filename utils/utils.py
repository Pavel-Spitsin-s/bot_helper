# -*- coding: utf-8 -*-
import datetime

from natasha import NewsEmbedding, Segmenter, NewsNERTagger, Doc, MorphVocab, NewsMorphTagger
from natasha.syntax import NewsSyntaxParser
from dateparser.search import search_dates

_embedding = NewsEmbedding()
_segmenter = Segmenter()
_morph_tagger = NewsMorphTagger(_embedding)
_ner_tagger = NewsNERTagger(_embedding)
_morph_vocab = MorphVocab()
_syntax_parser = NewsSyntaxParser(_embedding)


def text2doc(text):
    doc = Doc(text)
    doc.segment(_segmenter)
    doc.tag_morph(_morph_tagger)
    doc.tag_ner(_ner_tagger)
    doc.parse_syntax(_syntax_parser)

    for span in doc.spans:
        span.normalize(_morph_vocab)

    return doc


def get_loc_from_doc(doc):
    locs = []
    for span in doc.spans:
        if span.type == 'LOC':
            locs.append(span.normal)

    return ' '.join(locs)


def get_date_diff_from_message(message):
    dates = search_dates(message)
    today = datetime.date.today()
    if dates:
        date = dates[0][1].date()
        dt = (date - today).days
        if dt < 0 or dt > 6:
            return -1
        return dt
    return 0
