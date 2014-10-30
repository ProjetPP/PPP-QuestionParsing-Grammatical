"""Configuration module."""

import os
import json
import logging
from ppp_core.exceptions import InvalidConfig


class Config:
    __slots__ = ('corenlp_server')
    def __init__(self, data=None):
        if not data:
            try:
                with open(self.get_config_path()) as fd:
                    data = json.load(fd)
            except ValueError as exc:
                raise InvalidConfig(*exc.args)
        self.corenlp_server = data['corenlp_server']

    @staticmethod
    def get_config_path():
        path = os.environ.get('PPP_NLP_CLASSICAL_CONFIG', '')
        if not path:
            raise InvalidConfig('Could not find config file, please set '
                                'environment variable $PPP_NLP_CLASSICAL_CONFIG.')
        return path
