import api.models as models
from api import secrets

import api.twitter as twitter


class FollowFeed(object):
    """
    Object that tracks a specific user's second degree network
    """
    def __init__(self):
        self.api = twitter.user_auth(secrets.current_user_token, secrets.current_user_token_secret)
        self.screen_name = secrets.current_user_screen_name
        self.following_list = []

        cachename = '{}_follow_feed_cache.json'.format(self.screen_name)
        self.network = models.Network(file_name=cachename)

    def list_following(self) -> list:
        """
        Show a list of who you're following
        """
        return [u.screen_name for u in self.following_list]

    def create_snapshot(self):
        """
        Create a snapshot of the current 2nd degree network
        """
        following = twitter.get_following(self.api, self.screen_name)
        raw_user_objects = twitter.get_user_objects(self.api, following)
        self.following_list = models.User.create_from_list(self.api, raw_user_objects)

        second_degrees = [{u.screen_name: u.following} for u in self.following_list]
        self.network.add_snapshot(second_degrees)

    def get_captures(self):
        """
        List all the available captures in the cache
        """
        return self.network.snapshots.keys()

    def get_follow_feed(self):
        """
        Dump the cache to string format to see who followed who
        """
        return str(self.network.snapshots)

    def show_specific_users_follows(self, user):
        """
        Get the cache for a specific user
        :param user: Twitter user to show the cache for
        """
        result = {}
        for date, snapshot in self.network.snapshots.items():
            if user in snapshot:
                result[date] = snapshot[user]
        return result

    def show_capture_date(self, date):
        """
        Show the diff from the given date of capture
        """
        snaps = self.network.snapshots
        return self.network.get_diff(snaps[date], snaps[sorted(snaps.keys())[0]])

    def record_snapshot(self):
        """
        Save a snapshot of your current network
        """
        self.create_snapshot()
