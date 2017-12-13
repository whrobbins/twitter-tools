import unittest
from unittest import TestCase

from api import secrets

import src.api.twitter as twit


class TestTwitter(TestCase):

    def setUp(self):
        self.app = twit.application_auth()
        self.user = twit.user_auth(secrets.whrobbins_access_token, secrets.whrobbins_access_token_secret)

    def test_integration(self):
        # print out followers
        followers = twit.get_followers(self.app, 'whrobbins')
        print(followers)
        users = twit.get_user_objects(self.app, followers[:50])
        for item in users:
            print(item)

        # print out pizza tweets
        r = self.app.request('search/tweets', {'q':'machine learning'})
        print(r.status_code)
        for item in r.get_iterator():
            print(item['user']['screen_name'], item['text'])
            print('\n\n')

        # print a stream of tweets with the given filter
        # for item in twit.continuous_stream(self.user, {'track': '#ai'}):
        #     print(item)

    def test_chunk_list(self):
        list_ = [1, 2, 3, 4, 5, 6, 7]
        chunker = twit.chunk_list(list_, chunk_size=3)
        self.assertEqual(chunker[0], [1, 2, 3])
        self.assertEqual(chunker[1], [4, 5, 6])
        self.assertEqual(chunker[2], [7])

    def test_get_timeline(self):
        r = self.app.request('search/tweets', {'q':'machine learning'})

    def test_get_paged_timeline(self):
        r = self.app.request('search/tweets', {'q':'machine learning'})

    def test_delete_tweet(self):
        pass  # don't want to live-delete. Will be tested in future weeks.

    def test_send_text_tweet(self):
        pass  # don't want to live-tweet. Will be tested in future weeks.

    def test_send_image_tweet(self):
        pass  # don't want to live-tweet. Will be tested in future weeks.

    def test_get_followers(self):
        followers = twit.get_followers(self.app, 'whrobbins')
        self.assertIn('3259639626', str(followers))
        self.assertIn('21294240', str(followers))
        self.assertIn('4358642832', str(followers))

    def test_get_following(self):
        followers = twit.get_following(self.app, 'whrobbins')

    def test_get_user_objects(self):
        pass  # covered in setUp


if __name__ == '__main__':
    unittest.main()
