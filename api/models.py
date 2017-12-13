# Path hack.
import json
import os
import sys
import TwitterAPI

sys.path.insert(0, os.path.abspath('..'))

from api.twitter import get_following, get_followers, get_user_objects


class Tweet(object):
    """
    Object representing a single Tweet
    """
    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.id = raw_json['id']
        self.screen_name = raw_json['user']['screen_name']
        self.text = raw_json['text']
        self.hashtags = raw_json['entities']['hashtags']
        self.users_mentioned = [u['screen_name'] for u in raw_json['entities']['user_mentions']]
        self.favorite_count = raw_json['favorite_count']
        self.retweet_count = raw_json['retweet_count']
        self.engagement = self.favorite_count + self.retweet_count

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'screen_name: {}, hashtags: {}, mentions: {}, text: {}'.format(self.screen_name,
                                                                              self.text,
                                                                              self.hashtags,
                                                                              self.users_mentioned)

    @staticmethod
    def create_from_list(tweets: list) -> list:
        return [Tweet(t) for t in tweets]


class User(object):
    """
    Object representing a User
    """
    def __init__(self, raw_json: dict, api: TwitterAPI):
        self.screen_name = raw_json['screen_name']
        self.id_str = raw_json['id_str']
        self.url = raw_json['url']
        self.following = []
        self.followers = []
        if api:
            ids = get_following(api, self.screen_name)
            user_objects = get_user_objects(api, ids)
            self.following = [u['screen_name'] for u in user_objects]
            ids = get_followers(api, self.screen_name)
            user_objects = get_user_objects(api, ids)
            self.followers = [u['screen_name'] for u in user_objects]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{} - {} - {}\n{}'.format(self.screen_name, self.id_str, self.url, self.following)

    @staticmethod
    def create_from_list(api: TwitterAPI, users: list) -> list:
        return [User(u, api) for u in users]


class Network(object):
    """
    Object representing a cache of your second-degree network over time

    Example structure (snapshots stores state):
    {
        '10-31-2017': [
            'whrobbins': [
                'lpolovets',
                'jmj',
                'juliagalef'
            ],
            'niraj': [
                'wileycjw',
                'whrobbins',
                'naval'
            ]
        ],
        '1-2-1997': [
            'whrobbins': [
                'lpolovets',
                'jmj'
            ],
            'niraj': [
                'wileycjw',
                'whrobbins'
            ]
        ]
    }
    """
    def __init__(self, file_name=None):
        self.snapshots = {}
        self.file_name = file_name
        if self.file_name:
            self.load_cache()

    def load_cache(self):
        """
        Load cache from file
        """
        with open(self.file_name, 'r', encoding='utf-8') as json_data:
            try:
                data = json.load(json_data)
                self.snapshots = data
            except Exception as e:
                self.snapshots = {}

    def save_cache(self):
        """
        Save cache to file
        """
        with open(self.file_name, 'w') as file_:
            try:
                json.dump(self.snapshots, file_, indent=4)
            except Exception as e:
                return False

    def add_snapshot(self, snapshot: list):
        """
        Adds one snapshot to this network cache
        """
        import datetime as dt
        date_str = '{}-{}-{}'.format(dt.date.month, dt.date.day, dt.date.year)
        self.snapshots[date_str] = snapshot
        self.save_cache()

    def get_diff(self, old: dict, new: dict) -> list:
        """
        Show the difference between two snapshots
        :param old: older snapshot to compare
        :param new: newer snapshot to compare
        """
        result = []  # list of tuples (person_you_follow, person_they_followed_recently)
        old_keys = list(old.keys())
        for user, users_follows in new.items():
            if user not in old_keys:
                continue

            for second_degree_follow in users_follows:
                if second_degree_follow not in old[user]:
                    result.append((user, second_degree_follow))

        return result
