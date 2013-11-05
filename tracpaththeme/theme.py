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
from trac.core import TracError, implements
from trac.web.api import IRequestFilter
from trac.web.chrome import Chrome, ITemplateProvider, add_script, \
                            add_stylesheet

from themeengine.api import ThemeBase


__all__ = ['TracpathTheme']


_version = ('1_0', '0_12')[parse_version(trac_version) < parse_version('1.0')]


class TracpathTheme(ThemeBase):
    """5 themes based on http://tracpath.com."""

    implements(IRequestFilter, ITemplateProvider)

    htdocs = True

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if template and self.is_active_theme:
            self._add_jquery_ui(req)
            add_script(req, 'tracpaththeme/base.js')
        return template, data, content_type

    def get_htdocs_dirs(self):
        return [('tracpaththeme', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return ()

    def get_theme_names(self):
        yield 'tracpath_blue'
        yield 'tracpath_green'
        yield 'tracpath_purple'
        yield 'tracpath_red'
        yield 'tracpath_yellow'

    def get_theme_info(self, name):
        if not name.startswith('tracpath_'):
            raise TracError('Internal Error')
        info = super(self.__class__, self).get_theme_info(name)
        color = name[len('tracpath_'):]
        info['css'] = 'tracpath_%s_%s.css' % (color, _version)
        info['template'] = 'templates/tracpath_theme.html'
        info['screenshot'] = 'htdocs/screenshot_%s.png' % color

        return info

    if hasattr(Chrome, 'add_jquery_ui'):
        def _add_jquery_ui(self, req):
            return Chrome(self.env).add_jquery_ui(req)
    else:
        def _add_jquery_ui(self, req):
            add_stylesheet(req, 'tracpaththeme/jquery-ui/jquery-ui.css')
