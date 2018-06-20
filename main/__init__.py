#!/usr/bin/env python
#  -*- coding: utf-8 -*
from flask import Flask
from flask_cors import CORS
from main.helper.common_helper import JsonEncoder, build_current_path_by_file
from main.helper.toml_helper import TomlHelper
from main.blueprint.index import blueprint_index
import logging


def create_app(toml_config_file):
    server_toml_helper = TomlHelper(
        toml_file_name=build_current_path_by_file(__file__, toml_config_file))

    logging.basicConfig(format='[%(asctime)s] %(message)s',
                        level=server_toml_helper.get_option_by_section(
                            'app', 'log_level').upper())
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.json_encoder = JsonEncoder
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = server_toml_helper.get_option_by_section(
        'app', 'secret_key')

    app.config['baidu'] = \
        server_toml_helper.get_options_by_section('baidu')

    app.register_blueprint(blueprint_index, url_prefix="/")

    return app