"""Configuration module."""

import os
import json
import logging
from ppp_libmodule.config import Config as BaseConfig
from ppp_libmodule.exceptions import InvalidConfig


class Config(BaseConfig):
    __slots__ = ('corenlp_server', 'cache_size')
    config_path_variable = 'PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'
    def parse_config(self, data):
        self.corenlp_server = data['corenlp_server']
        self.cache_size = data.get('cache_size', 0)
