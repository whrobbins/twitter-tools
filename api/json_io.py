import datetime
import json
import logging


class JsonIO(object):
    """
    Wrapper around json library to enable logged reading and writing of json data (derived from assignment2)
    """
    def __init__(self, filename):
        self.filename = filename
        self.logger = logging.getLogger('readwrite')
        if not getattr(self.logger, 'handler_set', None):
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate = False

    @staticmethod
    def compress_user_object(users):
        """
        Converts a list of user objects to a list of (screen_name, time-stamp) tuples
        :return: tuple (screen_name, time_stamp)
        """
        names = []
        for user in users:
            if 'user' in user and 'screen_name' in user['user']:
                names.append((user['user']['screen_name'], datetime.date.today()))
        return names

    def save_to_file(self, data):
        """
        Write the given dict to a json file
        :param data: data to write
        """
        with open(self.filename, 'w') as file_:
            self.logger.info('Writing data to file')
            try:
                json.dump(data, file_, indent=4)
            except Exception as e:
                self.logger.error('Failed to write data to file: {}'.format(e))

    def read_from_file(self):
        """
        Read json data from this file and return a dict
        """
        with open(self.filename, 'r', encoding='utf-8') as json_data:
            self.logger.info('Reading data from file')
            try:
                data = json.load(json_data)
                return data
            except Exception as e:
                self.logger.error('Failed to read data from file: {}'.format(e))
                return None

    def append(self, data):
        with open(self.filename, 'a') as file_:
            self.logger.info('Appending data to file')
            try:
                json.dump(data, file_, indent=4)
            except Exception as e:
                self.logger.error('Failed to write data to file: {}'.format(e))

