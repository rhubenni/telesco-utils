from typing import Union
import requests
from .debug_info import debug_info


class DataHubEngine:

    @debug_info('DataHubEngine', 'initialization')
    def __init__(self, token, secret, flag1=None, flag2=None, flag3=None, verifyCert=True):
        self._token = token
        self._secret = secret
        self._settings = self._get_default_settings()
        self.flag1 = flag1
        self.flag2 = flag2
        self.flag3 = flag3
        self._verifyCert = verifyCert

    @staticmethod
    def _get_default_settings() -> dict:
        return {
            'url': 'http://localhost:5173/api/v2/datahub',
        }

    @debug_info('DataHubEngine', 'reading configuration')
    def _get_caller_settings(self, fn) -> None:
        self._settings = {
            **self._get_default_settings(),
            **fn.__globals__.get('__DATAHUB', self._settings),
        }

    @debug_info('DataHubEngine', 'fetching data')
    def _retrieve_data(self) -> Union[list, dict, str]:
        request_params = {
            'token': self._token,
            'secret': self._secret,
            'flag1': self.flag1,
            'flag2': self.flag2,
            'flag3': self.flag3,
        }
        info = None
        try:
            from urllib3.exceptions import InsecureRequestWarning

            if not self._verifyCert:
                requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

            data = requests.post(
                url=self._settings.get('url'),
                json=request_params,
                verify=self._verifyCert
            )
            info = data.json()
            return info
        except requests.exceptions.ConnectionError:
            print('\b'*32 + '!!! ConnectionError !!!'.ljust(32))
