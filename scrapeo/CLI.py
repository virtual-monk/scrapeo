"""The CLI Module
=============

This module provides the CLI class, responsible for handling parsed
command line arguments and sending messages to the Scrapeo object.
"""

from .core import Scrapeo
from .utils import web_scraper


class CLI(object):

    def __init__(self, cl_args, dom_interface=None):
        self.cl_args = cl_args
        self.dom_interface = dom_interface
        self.searches = []
        self.dispatch = {'meta': self.prepare_queries,
                        'content': self.prepare_queries}
        self.shortcuts = {'meta_description': ['meta', {'name': 'description'}],
                          'robots_meta': ['meta', {'name': 'robots'}],
                          'title_tag': ['title', {}],
                          'canonical': ['link', {'rel': 'canonical', 'seo_attr': 'href'}]}

    def dispatch_commands(self):
        return self.dispatch[self.cl_args.command]()

    def run_search(self, query):
        element = query[0]
        search_params = query[1]
        return self.dom_interface.find_tag(element, **search_params)

    def scrape_text(self, element):
        seo_attr = self.cl_args.seo_attr
        return self.dom_interface.get_text(element, seo_attr=seo_attr)

    def prepare_queries(self):
        # default element is a meta tag
        if self.cl_args.metatag_attr or self.cl_args.metatag_val:
            element = 'meta'
            # --attr, --val
            search_params = {}
            # --val only
            if self.cl_args.metatag_val and not self.cl_args.metatag_attr:
                search_params['search_val'] = self.cl_args.metatag_val
            # --attr only
            elif self.cl_args.metatag_attr and not self.cl_args.metatag_val:
                search_params[self.cl_args.metatag_attr] = re.compile('.*')
            # --attr and --val
            else:
                search_params[self.cl_args.metatag_attr] = self.cl_args.metatag_val
            self.prepare_query(element, search_params)
        self.prepare_shortcut_queries()

    def prepare_shortcut_queries(self):
        shortcuts = self.get_shortcuts()
        for shortcut in shortcuts:
            element = self.shortcuts[shortcut][0]
            search_params = self.shortcuts[shortcut][1]
            self.prepare_query(element, search_params)

    def prepare_query(self, element, search_params):
        self.searches.append([element, search_params])

    def get_shortcuts(self):
        shortcut_keys = self.shortcuts.keys()
        shortcuts = []
        for shortcut in shortcut_keys:
            args_dict = vars(self.cl_args)
            if args_dict[shortcut]:
                shortcuts.append(shortcut)
        return shortcuts