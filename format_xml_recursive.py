from __future__ import print_function

import logging
from lxml import etree
import os


def get_node_key(node, attr=None):
    """Return the sorting key of an xml node
    using tag and attributes
    """
    if attr is None:
        return '%s' % node.tag + ':'.join([node.get(attr)
                                           for attr in sorted(node.attrib)])
    if attr in node.attrib:
        return '%s:%s' % (node.tag, node.get(attr))
    return '%s' % node.tag


def sort_children(node, attr=None):
    """ Sort children along tag and given attribute.
    if attr is None, sort along all attributes"""
    if not isinstance(node.tag, str):  # PYTHON 2: use basestring instead
        # not a TAG, it is comment or DATA
        # no need to sort
        return
    # sort child along attr
    node[:] = sorted(node, key=lambda child: get_node_key(child, attr))
    # and recurse
    for child in node:
        sort_children(child, attr)


def sort(unsorted_file, sorted_file, attr=None):
    """Sort unsorted xml file and save to sorted_file"""
    tree = etree.parse(unsorted_file)
    root = tree.getroot()
    sort_children(root, attr)

    sorted_unicode = etree.tostring(root,
                                    pretty_print=True,
                                    encoding='unicode')
    with open(sorted_file, 'w') as output_fp:
        output_fp.write('%s' % sorted_unicode)
        logging.info('written sorted file %s', sorted_unicode)


def get_project_path():
    return "F:\\PyCharm 2021.2.2\\diff_apk"


def get_result_path(xml_path):
    return xml_path[:-4] + "_format.xml"


if __name__ == "__main__":
    xml_path = os.path.join(get_project_path(), "res\\apk.xml")
    sort(xml_path, get_result_path(xml_path))
