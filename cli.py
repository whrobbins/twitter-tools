import click
from api import secrets

from client import followfeed


class FollowingCLI(object):
    """
    CLI tool for seeing who your followers went out and followed
    """
    def __init__(self, token, token_secret, screen_name):
        self.feed = followfeed.FollowFeed()
        m = 'Logging in with {}. Change secrets.py to use a different account!'.format(self.feed.screen_name)
        click.echo(m)

    @click.command()
    @click.option('--user', default='',
                  help='User to show diff for. Use your screen_name to show all diffs')
    @click.option('--date', default='',
                    help='Shows the diff for a specific date')
    @click.option('--update',
                  help='Create a new snapshot and store it')
    def run(self, user, date, update):
        """
        Main method for CLI
        """
        click.echo(user)
        click.echo(date)

        if user == self.feed.screen_name:
            self.get_follow_feed()
        elif user:
            self.show_specific_users_follows(user)
        elif date:
            self.show_capture_date(date)
        elif update:
            self.record_snapshot()

    def get_follow_feed(self):
        """
        Get the list of diffs (who followed who)
        """
        click.echo(self.feed.get_follow_feed())

    def show_specific_users_follows(self, user):
        """
        Look at the following activity of a specific user
        """
        click.echo(self.feed.show_specific_users_follows(user))

    def show_capture_date(self, date):
        """
        List the log dates
        """
        click.echo(self.show_capture_date())

    def record_snapshot(self):
        """
        Save a snapshot of your 2nd degree network
        """
        self.feed.create_snapshot()


if __name__ == '__main__':
    cli = FollowingCLI(secrets.current_user_token,
                       secrets.current_user_token_secret,
                       secrets.current_user_screen_name)
    cli.run()
