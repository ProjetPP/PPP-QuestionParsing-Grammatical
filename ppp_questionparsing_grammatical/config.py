"""Configuration module."""

import os
import json
import logging
from ppp_libmodule.config import Config as BaseConfig
from ppp_libmodule.exceptions import InvalidConfig


class Config(BaseConfig):
    __slots__ = ('corenlp_servers',
            'memcached_servers', 'memcached_timeout', 'memcached_salt')
    config_path_variable = 'PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'
    def parse_config(self, data):
        self.corenlp_servers = data['corenlp_servers']
        self.memcached_servers = data['memcached']['servers']
        self.memcached_timeout = data['memcached']['timeout']
        self.memcached_salt = data['memcached']['salt']
