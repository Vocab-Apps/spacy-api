import os
import unittest
import json
import pprint
import requests
from api import app

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ApiTests, cls).setUpClass()
        
        external_url = os.environ.get('SPACY_API_EXTERNAL_URL', None)
        if external_url == None:
            cls.client = app.test_client()
            cls.external_url = None
        else:
            cls.external_url = external_url

    @classmethod
    def tearDownClass(cls):
        pass

    def get_query(self, path):
        if self.external_url != None:
            return requests.get(self.external_url + path)
        else:
            return self.client.get(path)

    def post_query(self, path, data):
        if self.external_url != None:
            return requests.post(self.external_url + path, data=data)
        else:
            return self.client.post(path, json=data)

    def test_languages(self):
        response = self.get_query('/v1/language_list')
        data = json.loads(response.data)
        self.assertIn('en', data)

    def test_tokenize_english(self):
        text = "I was reading today's paper."

        response = self.post_query('/v1/tokenize', {'language': 'en', 'text': text})
        data = json.loads(response.data)        

        pprint.pprint(data)
        
        expected_result = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': 'I',
            'pos_description': 'pronoun, personal',
            'token': 'I'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'be',
            'pos_description': 'verb, past tense',
            'token': 'was'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'read',
            'pos_description': 'verb, gerund or present participle',
            'token': 'reading'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'today',
            'pos_description': 'noun, singular or mass',
            'token': 'today'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': "'s",
            'pos_description': 'possessive ending',
            'token': "'s"},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'paper',
            'pos_description': 'noun, singular or mass',
            'token': 'paper'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': '.',
            'pos_description': 'punctuation mark, sentence closer',
            'token': '.'}]
        
        self.assertEqual(data, expected_result)        

    def test_tokenize_french(self):
        text = "Le nouveau plan d’investissement du gouvernement."

        response = self.post_query('/v1/tokenize', data={'language': 'fr', 'text': text})
        data = json.loads(response.data)        

        pprint.pprint(data)
        
        expected_result = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': 'le',
            'pos_description': 'determiner',
            'token': 'Le'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'nouveau',
            'pos_description': 'adjective',
            'token': 'nouveau'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'plan',
            'pos_description': 'noun',
            'token': 'plan'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': 'd’',
            'pos_description': 'adposition',
            'token': 'd’'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'investissement',
            'pos_description': 'noun',
            'token': 'investissement'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'de',
            'pos_description': 'adposition',
            'token': 'du'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'gouvernement',
            'pos_description': 'noun',
            'token': 'gouvernement'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': '.',
            'pos_description': 'punctuation',
            'token': '.'}]
        
        self.assertEqual(data, expected_result)                

    def test_tokenize_chinese_chars(self):
        text = "送外卖的人"

        response = self.post_query('/v1/tokenize', data={'language': 'zh_char', 'text': text})
        data = json.loads(response.data)        

        expected_result_chars = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': '送',
            'token': '送'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '外',
            'token': '外'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '卖',
            'token': '卖'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '的',
            'token': '的'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '人',
            'token': '人'}]
        
        self.assertEqual(data, expected_result_chars)                


    def test_tokenize_chinese_words(self):
        text = "送外卖的人"

        response = self.post_query('/v1/tokenize', data={'language': 'zh_jieba', 'text': text})
        data = json.loads(response.data)        

        expected_result_words = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': '送',
            'token': '送'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '外卖',
            'token': '外卖'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '的',
            'token': '的'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '人',
            'token': '人'}]

        self.assertEqual(data, expected_result_words)