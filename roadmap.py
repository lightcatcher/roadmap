# -*- coding: utf-8 -*-

import re

class Roadmap(dict):

    def default(self):
        pass

    def destination(self, reg_str, pass_obj=True):
        regex = re.compile(reg_str)

        def decorator(func):
            self[regex] = {'func': func, 'pass_obj': pass_obj}
            return func

        return decorator

    def handle_match(self, match, obj):
        groups = match.groups()
        groupdict = match.groupdict()

        if groupdict:
            if len(groupdict) == len(groups):
                return self.process_pair(match.re, obj, **groupdict)
            else:
                exclusives = [s for s in groups if s not in groupdict.values()]
                return self.process_pair(match.re, obj, *exclusives, **groupdict)
        else:
            return self.process_pair(match.re, obj, *groups)

    def process_pair(self, regex, obj, *args, **kwargs):
        if self[regex]['pass_obj']:
            if hasattr(obj, '__iter__'):
                objects = [o for o in obj]
                objects.extend(args)
                return self[regex]['func'](*objects, **kwargs)
            else:
                return self[regex]['func'](obj, *args, **kwargs)
        else:
            return self[regex]['func'](*args, **kwargs)

    def route(self, obj, key=None):
        if key:
            string = key
        else:
            string = obj

        for regex in self.keys():
            match = regex.match(string)
            if match:
                return self.handle_match(match, obj)
        return self.default()