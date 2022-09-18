#!/usr/bin/env python3

from flask import Flask, request
import flask_restful
import logging
import spacy

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y%m%d-%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = flask_restful.Api(app)

class SpacyManager():
    def __init__(self):
        self.engines = {}

        logger.info('loading engines')

        import en_core_web_trf
        self.engines['en'] = en_core_web_trf.load()
        import fr_dep_news_trf
        self.engines['fr'] = fr_dep_news_trf.load()
        # chinese models
        import spacy.lang.zh
        self.engines['zh_char'] = spacy.lang.zh.Chinese()
        self.engines['zh_jieba'] = spacy.lang.zh.Chinese.from_config({"nlp": {"tokenizer": {"segmenter": "jieba"}}})
        self.engines['zh_pkuseg'] = spacy.lang.zh.Chinese.from_config({"nlp": {"tokenizer": {"segmenter": "pkuseg"}}})

        logger.info('finished loading engines')

    def language_list(self):
        return list(self.engines.keys())

    def tokenize(self, language, text):
        nlp_engine = self.engines[language]

        doc = nlp_engine(text)
        result = []
        for token in doc:
            lemma = token.lemma_
            if len(lemma) == 0:
                lemma = str(token)
            pos_description = spacy.explain(token.tag_)
            entry = {
                'token': str(token),
                'lemma': lemma,
                'can_translate': token.is_alpha,
                'can_transliterate': token.is_alpha
            }
            if pos_description != None:
                entry['pos_description'] = pos_description
            result.append(entry)
        return result        


manager = SpacyManager()

class Tokenize(flask_restful.Resource):
    def post(self):
        data = request.json
        return manager.tokenize(data['language'], data['text'])

class LanguageList(flask_restful.Resource):
    def get(self):
        return manager.language_list()


api.add_resource(Tokenize, '/v1/tokenize')
api.add_resource(LanguageList, '/v1/language_list')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')