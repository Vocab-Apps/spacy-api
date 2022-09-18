import unittest
import json
import tempfile
import datetime
import urllib.parse
import pprint
from app import app

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ApiTests, cls).setUpClass()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_languages(self):
        response = self.client.get('/v1/language_list')
        data = json.loads(response.data)
        self.assertIn('en', data)

    def test_tokenize_english(self):
        text = "I was reading today's paper."

        response = self.client.post('/v1/tokenize', json={'language': 'en', 'text': text})
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

        response = self.client.post('/v1/tokenize', json={'language': 'fr', 'text': text})
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


