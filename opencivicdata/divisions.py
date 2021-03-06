#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import io
if sys.version_info[0:2] == (2, 7):
    from backports import csv
    from urllib2 import urlopen
    FileNotFoundError = IOError
else:
    import csv
    from urllib.request import urlopen

PWD = os.path.abspath(os.path.dirname(__file__))
OCD_DIVISION_CSV = os.environ.get('OCD_DIVISION_CSV',
                                  os.path.join(PWD, 'division-ids/identifiers/country-{}.csv'))
OCD_REMOTE_URL = ('https://raw.githubusercontent.com/opencivicdata/ocd-division-ids/master/'
                  'identifiers/country-{}.csv')


class Division(object):
    _cache = {}

    @classmethod
    def all(self, country, from_csv=None):

        file_handle = None

        # check for environment variable
        if not from_csv and 'OCD_DIVISION_CSV' in os.environ:
            from_csv = os.environ.get('OCD_DIVISION_CSV').format(country)
            try:
                file_handle = io.open(from_csv, encoding='utf8')
            except FileNotFoundError:
                raise ValueError("Unknown country in OCD ID")

        # going to the remote URL
        if not file_handle:
            file_handle = io.StringIO(urlopen(OCD_REMOTE_URL.format(country)
                                              ).read().decode('utf-8'))

        for row in csv.DictReader(file_handle):
            yield Division(**row)

    @classmethod
    def get(self, division, from_csv=None):
        if division not in self._cache:
            # figure out the source
            if not from_csv:
                if not re.match(r"ocd-division/country:\w{2}", division):
                    raise ValueError("Invalid OCD format.")
                country = re.findall(r'country:(\w{2})', division)[0]

            # just load all divisions into cache
            for d in self.all(country, from_csv):
                pass

            if division not in self._cache:
                raise ValueError("Division not found: {}".format(division))

        return self._cache[division]

    def __init__(self, id, name, **kwargs):
        self._cache[id] = self
        self.id = id
        self.name = name
        self.sameAs = kwargs.pop('sameAs', None)
        valid_through = kwargs.pop('validThrough', None)
        if valid_through:
            self.valid_through = valid_through

        # set parent and _type
        parent, own_id = id.rsplit('/', 1)
        if parent == 'ocd-division':
            self.parent = None
        else:
            self.parent = self._cache.get(parent)
            if self.parent:
                self.parent._children.append(self)
            else:
                # TODO: keep a list of unassigned parents for later reconciliation
                pass

        self._type = own_id.split(':')[0]

        # other attrs
        self.attrs = kwargs
        self.names = []
        self._children = []

    def children(self, _type=None, duplicates=True, levels=1):
        for d in self._children:
            if (not _type or d._type == _type) and (duplicates or not d.sameAs):
                yield d
                if levels > 1:
                    for c in d.children(_type, duplicates, levels - 1):
                        yield c

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)
