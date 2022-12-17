# -*- coding: utf-8 -*-
import logging

from natasha import NewsEmbedding, Segmenter, NewsNERTagger, Doc, MorphVocab, NewsMorphTagger
from natasha.syntax import NewsSyntaxParser

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
    doc.ner.print()
    locs = []
    for span in doc.spans:
        if span.type == 'LOC':
            locs.append(span.normal)

    return ' '.join(locs)
