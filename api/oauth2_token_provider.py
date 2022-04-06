import time
from threading import Thread

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from reader.arg import ArgReader


class Oauth2TokenProvider(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.__token = self.retrieve_token(first_time=True)
        self.start()

    def retrieve_token(self, first_time=False):
        """
        interact with the OAuth2 token endpoint.

        :return: the OAuth2 token
        """
        token = None if first_time else self.__token
        client = BackendApplicationClient(
            client_id=ArgReader.db.auth.client_id)
        oauth = OAuth2Session(client=client,
                              token=token,
                              auto_refresh_url=ArgReader.db.auth.token_uri)
        return oauth.fetch_token(token_url=ArgReader.db.auth.token_uri,
                                 client_id=ArgReader.auth.client_id,
                                 client_secret=ArgReader.auth.client_secret,
                                 verify=ArgReader.auth.verify)

    def token(self):
        """
        the interface specified by the ABC
        :return:  the access token. Note that this will explode if there's no
                  token available.
        """
        return self.__token['access_token']

    def run(self):
        while True:
            print(
                f'Token will expire in {self.__token["expires_in"]} seconds.')
            time.sleep(self.__token['expires_in'] - 55)  # one minute early
            self.__token = self.retrieve_token()
