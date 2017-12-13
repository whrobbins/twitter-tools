import api.secrets as secrets
from TwitterAPI import TwitterAPI, TwitterRestPager

'''
Wrapper around TwitterAPI to allow access to tweet data and enable easy auth and api calling.

Written as a module to provide singleton-like behavior.
'''


def application_auth() -> TwitterAPI:
    """
    Returns an api object with read access. Cannot edit specific user tweets or data
    """
    return TwitterAPI(secrets.consumer_key,
                      secrets.consumer_secret,
                      auth_type='oAuth2')


def user_auth(access_token, access_secret) -> TwitterAPI:
    """
    Returns a api object tied to a specific user. Can edit user data and tweet
    """
    return TwitterAPI(secrets.consumer_key,
                      secrets.consumer_secret,
                      access_token,
                      access_secret, )


def chunk_list(payload: str, chunk_size: int=300) -> list:
    """
    Chunks up a list of tweets or screen_names to avoid API limits
    :param payload: list to chunk up
    :param chunk_size: size of each chucnk
    """
    chunks = []
    for i in range(0, len(payload), chunk_size):
        chunks.append(payload[i:min(i + chunk_size, len(payload))])
    return chunks


def get_timeline(api: TwitterAPI, count: int=50) -> list:
    """
    Returns an iterator of timeline tweets for the given user.
    :param api: Must be a User auth'd TwitterAPI.
    :param count: number of tweets to display
    :return: the list of tweets
    """
    r = api.request('statuses/home_timeline', {'count': count})
    return list(r.get_iterator())


def get_paged_timeline(api: TwitterAPI, count: int=500):
    """
    Returns an iterator of pages of the timeline. The iterator has higher capacity and scrolls.
    :param api: Must be a User auth'd TwitterAPI.
    :param count: number of tweets to display
    :return: the iterator of timeline tweets
    """
    timeline = TwitterRestPager(api, 'status/home_timeline', {'count': count})
    return timeline.get_iterator()


def delete_tweet(api: TwitterAPI, tweet_id: int) -> bool:
    """
    Deletes a tweet given the relevant tweet_id
    :param api: A User-Auth'd TwitterAPI
    :param tweet_id: id to delete
    :return: success boolean
    """
    r = api.request('statuses/destroy/{}'.format(tweet_id))
    return True if r.status_code == 200 else False


def fav_tweet(api: TwitterAPI, tweet) -> bool:
    """
    Follows the specified user
    :param api: A User-Auth'd TwitterAPI
    :param tweet: tweet to fav
    :return: success
    """
    r = api.request('favorites/create', {'id': tweet.id})

    if r.status_code != 200:
        return False

    return True


def send_text_tweet(api: TwitterAPI, payload: str) -> bool:
    """
    Sends a text-only tweet
    :param api: A User-Auth'd TwitterAPI
    :param payload: The content of the string to tweet
    :return: success boolean
    """
    r = api.request('statuses/update', {'status': payload})
    return True if r.status_code == 200 else False


def send_image_tweet(api: TwitterAPI, filename: str, text=None) -> bool:
    """
    Sends a multimedia tweet
    :param api: A User-Auth'd TwitterAPI
    :param filename: name of the image to upload/tweet
    :param text: text to include along with the multimedia (optional)
    :return: success boolean
    """
    with open(filename, 'rb') as f:
        r = api.request('media/upload', None, {'media': f.read()})

    if r.status_code != 200:
        print('Error: media failed to upload!')
        return False

    if not text:
        text = ''
    payload = {'media_id': r.json()['media_id'], 'status': text}
    r = api.request('statuses/update', payload)
    return True if r.status_code == 200 else False


def get_followers(api: TwitterAPI, username: str) -> list:
    """
    Gets a list of follower user-objects
    :param api: A User-Auth'd TwitterAPI
    :param username: username to get followers for
    :return: list of user-objects
    """
    r = api.request('followers/ids', {'screen_name': username})
    return list(r.get_iterator())


def get_following(api: TwitterAPI, username: str) -> list:
    """
    Gets a list of following user-objects
    :param api: A User-Auth'd TwitterAPI
    :param username: username to get friends for
    :return: list of user-objects
    """
    r = api.request('friends/ids', {'screen_name': username})
    return list(r.get_iterator())


def get_user_objects(api: TwitterAPI, id_list: list) -> list:
    """
    Given a list of user_ids, get the associated user_objects
    :param api: A User-Auth'd TwitterAPI
    :param id_list: list of ids to convert
    :return: list of ids
    """
    id_list = [str(id_) for id_ in id_list]
    result_list = []

    for chunk in chunk_list(id_list, chunk_size=50):
        request_string = ','.join(chunk)
        r = api.request('users/lookup', {'user_id': request_string})
        result_list.extend(list(r.get_iterator()))

    return result_list


def continuous_stream(api: TwitterAPI, filter_: dict):
    """
    Given a filter, get a stream of all public tweets fitting the given filters
    :param api: A User-Auth'd TwitterAPI
    :param filter_: params to search for
    """
    r = api.request('statuses/filter', filter_)

    if r.status_code != 200:
        print(r.text)
        return []

    stream = r.get_iterator()
    for item in stream:
        yield item


def follow_user(api: TwitterAPI, user) -> bool:
    """
    Follows the specified user
    :param api: A User-Auth'd TwitterAPI
    :param screen_name: user to follow
    :return: success
    """
    r = api.request('friendships/create', {'screen_name': user.screen_name})

    if not (r.status_code == 200 or r.status_code == 403):
        return False
    return True


def get_follower_suggestions(api: TwitterAPI, category: str='business') -> list:
    """
    Get's follow suggestions from the Twitter api for the logged-in user
    :param api: a TwitterAPI object logged into the user to suggest for
    :return: list of users
    """
    api_path = 'users/suggestions/:{}/members'.format(category)
    r = api.request(api_path)
    return list(r.get_iterator())


if __name__ == '__main__':
    import pprint
    app = application_auth()
    user = user_auth(secrets.current_user_token, secrets.current_user_token_secret)

    # # print out followers
    # followers = get_followers(app, 'whrobbins')
    # print(followers)
    # users = get_user_objects(app, followers[:50])
    # for item in users:
    #     pprint.pprint(item)
    #
    # # print out ml related tweets
    # r = app.request('search/tweets', {'q':'machine learning'})
    # print(r.status_code)
    # for item in r.get_iterator():
    #     pprint.pprint(item['user']['screen_name'], item['text'])
    #     print('\n\n')
    #
    # print a stream of tweets with the given filter
    # for item in continuous_stream(user, {'track': '#ai'}):
    #     pprint.pprint(item)

    for item in get_follower_suggestions(user):
        pprint.pprint(item)
