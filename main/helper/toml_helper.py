#!/usr/bin/env python
#  -*- coding: utf-8 -*
import os.path
import toml
from .common_helper import build_current_path_by_file


class TomlHelper(object):
    def __init__(self, toml_file_name='app.toml'):
        self.config = {}
        if not os.path.isabs(toml_file_name):
            toml_file_name = build_current_path_by_file(__file__, toml_file_name)
        self.toml_file_name = toml_file_name
        # 默认配置文件名称
        self.__load_options()

    def __load_options(self):
        config_data = toml.load(self.toml_file_name)
        for section_key, section_value in config_data.items():
            self.config[section_key] = {}
            for item_key, item_value in section_value.items():
                self.config[section_key][item_key] = item_value

    def section_existed(self, section_name):
        return section_name in self.config

    def get_options_by_section(self, section_name):
        if section_name in self.config:
            return self.config[section_name]
        else:
            return {}

    def get_option_by_section(self, section_name, key, fallback=None):
        section_info = self.config[section_name]
        if key in section_info:
            return section_info[key]
        else:
            return fallback
