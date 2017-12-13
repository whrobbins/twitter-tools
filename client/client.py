import time
from collections import defaultdict

import api.models as models
import nltk
from api.json_io import JsonIO
from api.twitter import *
from client import preferences

import api.analytics as analytics


class TwitterClient(object):
    def __init__(self):
        self.api = user_auth(secrets.current_user_token, secrets.current_user_token_secret)
        self.fav_log = JsonIO('{}_fav_log'.format(secrets.current_user_screen_name))
        self.follow_log = JsonIO('{}_follow_log'.format(secrets.current_user_screen_name))

    def find_high_engagement_topics(self, timeline_count=20) -> list:
        # get a list of Tweet objects from the timeline
        timeline = get_timeline(self.api, count=timeline_count)
        tweets = models.Tweet.create_from_list(timeline)

        # add tweet content to analytics cache
        for t in tweets:
            analytics.add_tweet_to_seen_words(t.text)

        # get frequency list
        most_common_words = analytics.retreive_seen_cache()

        # build engagement mapping
        tweet_text = defaultdict(int)
        for t in tweets:
            for word in nltk.word_tokenize(t.text):
                tweet_text[word] += t.engagement

        # normalize for frequency
        for word, freq in most_common_words:
            tweet_text[word] /= freq

        return sorted(tweet_text.items(), key=(lambda x: x[1]), reverse=True)

    def auto_fav(self, content: list) -> list:
        # find tweets based on content
        tweets = get_timeline(self.api)
        faved = []
        for t in tweets:
            for phrase in content:
                if phrase in tweets.text:
                    fav_tweet(self.api, t)
                    faved.append(t)
                    time.sleep(preferences.ACTION_DELAY)

                    # log tweets that were faved
                    self.fav_log.append(t.id)

                    break

            if len(faved) > preferences.NUM_FAVES_ALLOWED:
                break

        return [t.text for t in faved]

    def auto_follow(self, content: list) -> list:
        # find tweets based on content
        tweets = get_timeline(self.api)
        followed = []

        for t in tweets:
            for phrase in content:
                if phrase in t.text:
                    follow_user(self.api, t.screen_name)
                    followed.append(t)
                    time.sleep(preferences.ACTION_DELAY)

                    # log tweets that were faved
                    self.follow_log.append(t.screen)

                    break

            if len(followed) > preferences.NUM_FOLLOWS_ALLOWEDF:
                break

        return [t.screen_name for t in followed]

    def follow_suggestions(self, category='business') -> list:
        suggestions = get_follower_suggestions(self.api, category)
        users = [models.User(u, self.api) for u in suggestions]
        return users


if __name__ == '__main__':
    client = TwitterClient()

    # print(client.find_high_engagement_topics())

    # print(client.follow_suggestions())

    # client.auto_fav(['blockchain'])

    # client.auto_follow(['AI'])
