from graphviz import Digraph
import xml.dom.minidom as dom
import os


class GUITree:
    def __init__(self, value):
        self.value = value
        self.color = "black"
        self.nodes = []
        self.handlers = []
        self.edges = []


def get_view_node(view_node):
    tree = GUITree(value=view_node)

    if view_node.attributes.__contains__("diff:delete"):
        tree.color = "red"
    elif view_node.attributes.__contains__("diff:insert"):
        tree.color = "green"

    if view_node.attributes.__contains__("allocMethod"):
        alloc_method = view_node.getAttribute("allocMethod")
        tree.edges.append(alloc_method.split(":")[1])

    for view_child in view_node.childNodes:
        child_views = []
        if 'Handler' in view_child.nodeName:
            tree.handlers.append(get_handler(view_child))
        for child_node in view_child.childNodes:
            if child_node.nodeName == 'View':
                child_views.append(get_view_node(child_node))
        for child_view in child_views:
            tree.nodes.append(child_view)
    return tree


def get_handler(node):
    handler_tree = GUITree(value=node)
    return handler_tree


def print_tree(tree):
    print(tree.value)
    for node in tree.nodes:
        print_tree(node)
    for handler in tree.handlers:
        print(handler)


def get_node_name(node_name):
    if node_name in node_names.keys():
        node_names[node_name] = node_names[node_name] + 1
        node_name = node_name + str(node_names[node_name])
    else:
        node_names[node_name] = 0
    return node_name


def get_label_name(node):
    return node.value.attributes['type'].value.split(".")[-1]


def get_handler_name(node):
    return node.value.nodeName


def paint_tree(tree, activity_name, graph):
    node_label = get_label_name(tree)
    node_name = get_node_name(node_label)
    graph.node(name=node_name, label=node_label, color=tree.color)
    graph.edge(activity_name, node_name)

    for edge in tree.edges:
        graph.edge(edge, node_name)

    for node in tree.nodes:
        add_view_node(node, graph, node_name)
    for handler in tree.handlers:
        add_handler_node(handler, graph, node_name)


def add_handler_node(node, graph, father_node_name):
    node_label = get_handler_name(node)
    node_name = get_node_name(node_label)
    graph.node(name=node_name, label=node_label)
    graph.edge(father_node_name, node_name)


def add_view_node(node, graph, father_node_name):
    node_label = get_label_name(node)
    node_name = get_node_name(node_label)
    graph.node(name=node_name, label=node_label, color=node.color)
    graph.edge(father_node_name, node_name)

    for child in node.nodes:
        add_view_node(child, graph, node_name)
    for handler in node.handlers:
        add_handler_node(handler, graph, node_name)


def create_view_graph(xml_path):
    dom_tree = dom.parse(xml_path)
    root = dom_tree.documentElement
    view_graph = Digraph(xml_path.split(".xml")[0])
    view_graph.node("root")
    return root, view_graph


def get_project_path():
    return "F:\\PyCharm 2021.2.2\\diff_apk"


if __name__ == "__main__":
    node_names = {}
    root, view_graph = create_view_graph(os.path.join(get_project_path(), "res\\diff_res.xml"))
    for child in root.childNodes:
        if child.attributes and child.hasAttribute("name"):
            child_node_name = child.getAttribute("name")
            print("name: %s" % child_node_name)
            view_graph.node(name=child_node_name)
            view_graph.edge("root", child_node_name)

        for view_child in child.childNodes:
            if view_child.nodeName == 'View':
                view_tree = get_view_node(view_child)
                paint_tree(view_tree, child_node_name, view_graph)
        print("------------------")
    view_graph.view()
