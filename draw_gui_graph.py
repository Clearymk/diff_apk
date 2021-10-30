from graphviz import Digraph
import xml.dom.minidom as dom

DOMTree = dom.parse("res/base_apk.xml")
collection = DOMTree.documentElement

activities = collection.getElementsByTagName("Activity")
node_names = {}
view_graph = Digraph('base_apk')


class GUITree:
    def __init__(self, value):
        self.value = value
        self.nodes = []


def get_view_node(view_node):
    tree = GUITree(value=view_node)

    for view_child in view_node.childNodes:
        child_views = []
        for child_node in view_child.childNodes:
            if child_node.nodeName == 'View':
                child_views.append(get_view_node(child_node))
        for child_view in child_views:
            tree.nodes.append(child_view)
    return tree


def print_tree(tree):
    print(tree.value)
    for node in tree.nodes:
        print_tree(node)


def get_node_name(node_name):
    if node_name in node_names.keys():
        node_names[node_name] = node_names[node_name] + 1
        node_name = node_name + str(node_names[node_name])
    else:
        node_names[node_name] = 0
    return node_name


def paint_view_node(view_tree, activity_name):
    node_label = view_tree.value.attributes['type'].value.split(".")[-1]
    node_name = get_node_name(node_label)
    view_graph.node(name=node_name, label=node_label)
    view_graph.edge(activity_name, node_name)

    for node in view_tree.nodes:
        add_view_node(node, view_graph, node_name)


def add_view_node(node, view_graph, father_node_name):
    node_label = node.value.attributes['type'].value.split(".")[-1]
    node_name = get_node_name(node_label)
    view_graph.node(name=node_name, label=node_label)
    view_graph.edge(father_node_name, node_name)

    for child in node.nodes:
        add_view_node(child, view_graph, node_name)


if __name__ == "__main__":
    view_graph.node("root")
    for activity in activities:
        if activity.hasAttribute("name"):
            activity_node_name = activity.getAttribute("name")
            print("name: %s" % activity_node_name)

            view_graph.node(name=activity_node_name)
            view_graph.edge("root", activity_node_name)

        for activity_child in activity.childNodes:
            if activity_child.nodeName == 'View':
                view_tree = get_view_node(activity_child)
                paint_view_node(view_tree, activity_node_name)
        print("------------------")
    view_graph.view()
