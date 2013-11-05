#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 OpenGroove,Inc.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import os
from setuptools import setup

setup(
    name = 'TracpathTheme',
    version = '1.0',
    description = '5 themes for Trac and ThemeEnginePlugin based on http://tracpath.com.',
    url = 'http://trac-hacks.org/wiki/TracpathTheme',
    keywords = 'trac plugin theme',
    classifiers = ['Framework :: Trac'],

    author = 'OpenGroove,Inc.',
    author_email = 'trac@opengroove.com',
    license = 'BSD',  # the same as Trac
    maintainer='Jun Omae',
    maintainer_email='jun66j5@gmail.com',

    packages = ['tracpaththeme'],
    package_data = {
        'tracpaththeme': [
            'templates/*.html',
            'htdocs/*.js',
            'htdocs/*.css',
            'htdocs/*.png',
            'htdocs/color/*/*.css',
            'htdocs/color/*/*.png',
            'htdocs/jquery-ui/*.css',
            'htdocs/jquery-ui/images/*.png',
        ]},
    install_requires = ['TracThemeEngine'],
    entry_points = {
        'trac.plugins': [
            'tracpaththeme.theme = tracpaththeme.theme',
        ]
    },
)
