#! /usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os
import sys
import json

from packaging.version import Version
from xlifftool import xliff_language as xliff
from xml.etree import ElementTree

class release:
    def __init__(self, version, js):
        self.version = version
        self.json = js
        self.platforms = [x.lower() for x in js['platforms']]

    def matches(self, platform):
        return platform.lower() in self.platforms

    def xmllocalize(self, parent, tag, text, stringdb):
        item = ElementTree.SubElement(parent, tag)
        item.text = stringdb["en"][text]

        for locale in stringdb.keys():
            if locale == "en":
                continue

            item = ElementTree.SubElement(parent, tag, attrib={"xml:lang": locale})
            item.text = stringdb[locale][text]

    def description(self, stringdb):
        if stringdb is None:
            return None

        desc = ElementTree.Element('description')
        if "description" in self.json:
            self.xmllocalize(desc, 'p', self.json["description"], stringdb)

        bullets = ElementTree.Element('ul')
        for key in self.json.get("whatsnew", []):
            self.xmllocalize(desc, 'li', key, stringdb)

        if len(bullets) > 0:
            desc.append(bullets)

        if len(desc) == 0:
            return None

        return desc

    def toxml(self, stringdb=None):
        attrs = {
            'version': self.version,
            'date': self.json['date']
        }
        xml = ElementTree.Element('release', attrib=attrs)

        # Add the details URL which should point to github
        xurl = ElementTree.Element('url', attrib={'type': 'details'})
        xurl.text = f"https://github.com/mozilla-mobile/mozilla-vpn-client/releases/v{self.version}"
        xml.append(xurl)

        # Add release information, if possible
        desc = self.description(stringdb)
        if not desc is None:
            xml.append(desc)

        return xml

if __name__ == "__main__":
    ## Parse arguments to locate the input files and options.
    parser = argparse.ArgumentParser(
        description='Generate Appstream releases information from JSON')

    parser.add_argument('source', metavar='SOURCE', type=str, action='store',
        help='JSON releases file to parse')
    parser.add_argument('-i', '--i18n', metavar='DIR', type=str, action='store',
        help='Load localization data from DIR')
    parser.add_argument('--platform', metavar='PLATFORM', type=str,
        action='store', default='LINUX',
        help='Target platform for appstream releases')
    args = parser.parse_args()

    # Parse the JSON releases file
    with open(args.source, 'r') as fp:
        data = json.load(fp)

    # If a localization directory was provided, parse the addon XLIFF data too.
    stringdb = None
    if args.i18n:
        stringdb = {}
        for entry in os.scandir(args.i18n):
            if not entry.is_dir():
                continue
            
            filename = os.path.join(args.i18n, entry.name, 'addons', 'strings.xliff')
            if not os.path.exists(filename):
                continue

            xliffdata = xliff(entry.name)
            xliffdata.parse_xliff(filename)
            stringdb[xliffdata.locale] = xliffdata

    # Build the Appstream releases XML document.
    root = ElementTree.Element('releases')
    versions = list(data['releases'].keys())
    versions.sort(key=Version, reverse=True)
    for version in versions:
        info = release(version, data['releases'][version])
        if info.matches(args.platform):
            root.append(info.toxml(stringdb))

    # Dump the XML data to stdout
    ElementTree.indent(root, space="  ")
    ElementTree.dump(root)
