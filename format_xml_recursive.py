import logging
from lxml import etree
import os


def get_project_path():
    return "D:\\PyCharm\\code\\diff_apk"


def get_result_path(path):
    return path[:-4] + "_format.xml"


class XMLFormatter:
    def __init__(self, unsorted_file, sorted_file):
        self.unsorted_file = unsorted_file
        self.sorted_file = sorted_file
        self.format_file_path(self.sorted_file)

    @staticmethod
    def format_file_path(file_path):
        file_path = file_path.replace(file_path.split("\\")[-1], "")
        if not os.path.exists(file_path):
            os.mkdir(file_path)

    @staticmethod
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

    def sort_children(self, node, attr=None):
        """ Sort children along tag and given attribute.
        if attr is None, sort along all attributes"""
        if not isinstance(node.tag, str):  # PYTHON 2: use basestring instead
            # not a TAG, it is comment or DATA
            # no need to sort
            return
        # sort child along attr
        node[:] = sorted(node, key=lambda child: self.get_node_key(child, attr))
        # and recurse
        for child in node:
            self.sort_children(child, attr)

    def sort(self, attr=None):
        """Sort unsorted xml file and save to sorted_file"""
        tree = etree.parse(self.unsorted_file)
        root = tree.getroot()
        self.sort_children(root, attr)

        sorted_unicode = etree.tostring(root,
                                        pretty_print=True,
                                        encoding='unicode')
        with open(self.sorted_file, 'w') as output_fp:
            output_fp.write('%s' % sorted_unicode)
            logging.info('written sorted file %s', sorted_unicode)


if __name__ == "__main__":
    xml_path = os.path.join(get_project_path(), "res\\apk.xml")
    formatter = XMLFormatter(xml_path, get_result_path(xml_path))
    formatter.sort()
