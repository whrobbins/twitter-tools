import unittest
from unittest import TestCase

import src.api.analytics as analytics


class TestAnalytics(TestCase):
    def setUp(self):
        self.corpus = """Jargon.ai is the first intelligent video calling platform for busy professionals. 
                    Jargon transcribes, records and analyzes your important conversations, helping you
                     identify highlights and find hidden insights. No more note-taking, no more guessing
                     . We use the power of artificial intelligence, machine learning and affective 
                     science to read..."""
        self.list1 = ['artificial', 'intelligence', 'machine', 'learning']
        self.list2 = ['data', 'science', 'philosophy']


    def test_add_tweet_to_seen_words(self):
        analytics.add_tweet_to_seen_words("testing method")
        self.assertEqual(analytics.word_bank['testing'], 1)
        self.assertEqual(analytics.word_bank['method'], 1)
        self.assertEqual(analytics.word_bank['absent'], 0)

    def test_compare_topic_sets(self):
        result = analytics.compare_topic_sets(self.list1, self.list2)
        print(result)
        self.assertEqual(result, [None,
                                  None,
                                  None,
                                  0.36363636363636365,
                                  0.5714285714285714,
                                  0.6153846153846154,
                                  0.15384615384615385,
                                  0.125,
                                  0.13333333333333333,
                                  0.3333333333333333,
                                  0.5333333333333333,
                                  0.5714285714285714])

    def test_get_max_topic_similarity(self):
        result = analytics.get_max_topic_similarity(self.list1, self.list2)
        print(result)
        self.assertEqual(result, 0.6153846153846154)

    def test_get_avg_topic_similarity(self):
        result = analytics.get_avg_topic_similarity(self.list1, self.list2)
        print(result)
        self.assertEqual(result, 0.37785825285825286)

    def test_similarity_score(self):
        result = analytics.similarity_score(self.list1, self.list2)
        print(result)
        self.assertEqual(result, 2.5046758796758795)

    def test_show_wordcloud(self):
        pass  # do visual manual test


if __name__ == '__main__':
    unittest.main()
