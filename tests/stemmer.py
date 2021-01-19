import unittest

from mpstemmer import MPStemmer

class StemmerTest(unittest.TestCase):
    def setUp(self):
        self.stemmer = MPStemmer()

    def test_rule1(self):
        # rule 1: berV --> ber-V | be-rV
        self.assertEqual(self.stemmer.stem('berapi'), 'api')
        self.assertEqual(self.stemmer.stem('berambut'), 'rambut')

if __name__ == '__main__':
    unittest.main()