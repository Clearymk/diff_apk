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

    def print_tree(self):
        print(self.value)
        for node in self.nodes:
            node.print_tree()
        for handler in self.handlers:
            print(handler)


class DrawGUIGraph:
    def __init__(self, xml_path, result_path):
        self.xml_path = xml_path
        self.node_names = {}
        self.result_path = result_path
        self.get_result_path()

    def get_result_path(self):
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

    def get_view_node(self, view_node):
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
                tree.handlers.append(self.get_handler(view_child))
            for child_node in view_child.childNodes:
                if child_node.nodeName == 'View':
                    child_views.append(self.get_view_node(child_node))
            for child_view in child_views:
                tree.nodes.append(child_view)
        return tree

    @staticmethod
    def get_handler(node):
        handler_tree = GUITree(value=node)
        return handler_tree

    def get_node_name(self, node_name):
        if node_name in self.node_names.keys():
            self.node_names[node_name] = self.node_names[node_name] + 1
            node_name = node_name + str(self.node_names[node_name])
        else:
            self.node_names[node_name] = 0
        return node_name

    @staticmethod
    def get_label_name(node):
        return node.value.attributes['type'].value.split(".")[-1]

    @staticmethod
    def get_handler_name(node):
        return node.value.nodeName

    def paint_tree(self, tree, activity_name, graph):
        node_label = self.get_label_name(tree)
        node_name = self.get_node_name(node_label)
        graph.node(name=node_name, label=node_label, color=tree.color)
        graph.edge(activity_name, node_name)

        for edge in tree.edges:
            graph.edge(edge, node_name)

        for node in tree.nodes:
            self.add_view_node(node, graph, node_name)
        for handler in tree.handlers:
            self.add_handler_node(handler, graph, node_name)

    def add_handler_node(self, node, graph, father_node_name):
        node_label = self.get_handler_name(node)
        node_name = self.get_node_name(node_label)
        graph.node(name=node_name, label=node_label)
        graph.edge(father_node_name, node_name)

    def add_view_node(self, node, graph, father_node_name):
        node_label = self.get_label_name(node)
        node_name = self.get_node_name(node_label)
        graph.node(name=node_name, label=node_label, color=node.color)
        graph.edge(father_node_name, node_name)

        for child in node.nodes:
            self.add_view_node(child, graph, node_name)
        for handler in node.handlers:
            self.add_handler_node(handler, graph, node_name)

    def create_view_graph(self):
        dom_tree = dom.parse(self.xml_path)
        root = dom_tree.documentElement
        view_graph = Digraph(self.xml_path.split(".xml")[0], format="png")
        view_graph.node("root")
        return root, view_graph

    def start_draw(self):
        root, view_graph = self.create_view_graph()
        for child in root.childNodes:
            if child.attributes and child.hasAttribute("name"):
                child_node_name = child.getAttribute("name")
                view_graph.node(name=child_node_name)
                view_graph.edge("root", child_node_name)

            for view_child in child.childNodes:
                if view_child.nodeName == 'View':
                    view_tree = self.get_view_node(view_child)
                    self.paint_tree(view_tree, child_node_name, view_graph)
        view_graph.view(directory=self.result_path, filename="gui_diff")


def get_project_path():
    return "D:\\PyCharm\\code\\diff_apk"


if __name__ == "__main__":
    draw = DrawGUIGraph(os.path.join(get_project_path(), "res\\res.xml"), "res")
    draw.start_draw()
