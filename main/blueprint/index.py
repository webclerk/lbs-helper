#!/usr/bin/env python
#  -*- coding: utf-8 -*
from flask import Blueprint, render_template, jsonify, \
    request, session, redirect

blueprint_index = Blueprint("/", __name__)


@blueprint_index.route("/")
def route_index():
    return render_template("/index.html")
