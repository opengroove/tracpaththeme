# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 OpenGroove,Inc.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from pkg_resources import parse_version, resource_filename

from trac import __version__ as trac_version
from trac.core import Component, TracError, implements
from trac.web.api import IRequestFilter
from trac.web.chrome import Chrome, ITemplateProvider, add_script, \
                            add_stylesheet

from themeengine.api import IThemeProvider


__all__ = ['TracpathTheme']


if parse_version(trac_version) < parse_version('1.0'):
    _stylesheets = ('tracpaththeme/base.css',
                    'tracpaththeme/color/%s/base.css')
else:
    _stylesheets = ('tracpaththeme/base.css',
                    'tracpaththeme/base_1_0.css',
                    'tracpaththeme/color/%s/base.css',
                    'tracpaththeme/color/%s/base_1_0.css')


class TracpathTheme(Component):

    implements(IRequestFilter, ITemplateProvider, IThemeProvider)

    css = False
    htdocs = True

    _tracpath_theme = None

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if template:
            theme = self._get_tracpath_theme()
            if theme:
                self._add_jquery_ui(req)
                for path in theme['stylesheets']:
                    add_stylesheet(req, path)
                add_script(req, 'tracpaththeme/base.js')
                req.chrome['theme'] = 'tracpath_theme.html'
        return template, data, content_type

    def get_htdocs_dirs(self):
        return [('tracpaththeme', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return [resource_filename(__name__, 'templates')]

    def get_theme_names(self):
        yield 'tracpath_blue'
        yield 'tracpath_green'
        yield 'tracpath_purple'
        yield 'tracpath_red'
        yield 'tracpath_yellow'

    def get_template_overrides(self, name):
        return ()

    def get_theme_info(self, name):
        if not name.startswith('tracpath_'):
            raise TracError('Internal Error')
        color = name[len('tracpath_'):]
        return {
            'description': '5 themes based on http://tracpath.com/.',
            'screenshot': 'htdocs/screenshot_%s.png' % color,
        }

    def _get_tracpath_theme(self):
        theme = self._tracpath_theme
        if theme is None:
            name = self.config.get('theme', 'theme', '')
            if name and name.startswith('tracpath_'):
                color = name[len('tracpath_'):]
                theme = {'name': name, 'color': color,
                         'stylesheets': list(self._get_stylesheets(color))}
            else:
                theme = {}
            self._tracpath_theme = theme
        return theme

    def _get_stylesheets(self, color):
        for path in _stylesheets:
            if '%s' in path:
                path = path % color
            yield path

    if hasattr(Chrome, 'add_jquery_ui'):
        def _add_jquery_ui(self, req):
            return Chrome(self.env).add_jquery_ui(req)
    else:
        def _add_jquery_ui(self, req):
            add_stylesheet(req, 'tracpaththeme/jquery-ui/jquery-ui.css')
