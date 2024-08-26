#! /usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os
import sys
import json

from packaging.version import Version
from xml.etree import ElementTree

class release:
    def __init__(self, version, js):
        self.version = version
        self.json = js
        self.platforms = [x.lower() for x in js['platforms']]

    def matches(self, platform):
        return platform.lower() in self.platforms

    def toxml(self):
        attrs = {
            'version': self.version,
            'date': self.json['date']
        }
        xml = ElementTree.Element('release', attrib=attrs)

        # Add the details URL which should point to github
        xurl = ElementTree.Element('url', attrib={'type': 'details'})
        xurl.text = f"https://github.com/mozilla-mobile/mozilla-vpn-client/releases/v{self.version}"
        xml.append(xurl)

        # TODO: It is recommended to include a release description in the Appstream
        # manifest too. We could fetch this from the Github releases API, but they
        # aren't very well formatted for this purpose.

        return xml

if __name__ == "__main__":
    ## Parse arguments to locate the input files and options.
    parser = argparse.ArgumentParser(
        description='Generate Appstream releases information from JSON')

    parser.add_argument('source', metavar='SOURCE', type=str, action='store',
        help='JSON releases file to parse')
    parser.add_argument('--platform', metavar='PLATFORM', type=str,
        action='store', default='LINUX',
        help='Target platform for appstream releases')
    args = parser.parse_args()

    # Parse the JSON releases file
    with open(args.source, 'r') as fp:
        data = json.load(fp)

    # Build the Appstream releases XML document.
    root = ElementTree.Element('releases')
    versions = list(data['releases'].keys())
    versions.sort(key=Version, reverse=True)
    for version in versions:
        info = release(version, data['releases'][version])
        if info.matches(args.platform):
            root.append(info.toxml())

    # Dump the XML data to stdout
    ElementTree.indent(root, space="  ")
    ElementTree.dump(root)
