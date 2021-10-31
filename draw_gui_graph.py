from graphviz import Digraph
import xml.dom.minidom as dom
import os


class Edge:
    def __init__(self, value, color='black'):
        self.value = value
        self.color = color


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
            tree.edges.append(Edge(alloc_method.split(":")[1]))

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
    def get_handler_data(handler_data, handler_tree, color, data_type):
        if "FakeName" not in handler_data:
            activity_name = handler_data.split(":")[data_type]
            if "$" in activity_name:
                activity_name = activity_name.split("$")[0]
            activity_name = activity_name.removeprefix("<")
            edge = Edge(activity_name, color=color)
            handler_tree.edges.append(edge)

    def get_handler(self, node):
        handler_tree = GUITree(value=node)
        # 如果有变化 优先处理变化
        if node.attributes.__contains__("diff:update-attr"):
            update_attr_data = node.getAttribute("diff:update-attr")
            update_attr_data = update_attr_data.split(";")

            past_attr_data = ""
            if node.attributes.__contains__("realHandler"):
                past_attr_data = node.getAttribute("realHandler")
            elif node.attributes.__contains__("handler"):
                past_attr_data = node.getAttribute("handler")

            for data in update_attr_data:
                self.get_handler_data(data, handler_tree, "green", 1)

            if past_attr_data:
                self.get_handler_data(past_attr_data, handler_tree, "red", 0)
        # 否则就连接handler
        elif node.attributes.__contains__("realHandler"):
            handler_data = node.getAttribute("realHandler")
            self.get_handler_data(handler_data, handler_tree, "black", 0)
        elif node.attributes.__contains__("handler"):
            handler_data = node.getAttribute("handler")
            self.get_handler_data(handler_data, handler_tree, "black", 0)
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

    def add_handler_node(self, node, graph, father_node_name):
        node_label = self.get_handler_name(node)
        node_name = self.get_node_name(node_label)
        graph.node(name=node_name, label=node_label)
        graph.edge(father_node_name, node_name)

        for edge in node.edges:
            graph.edge(node_name, edge.value, color=edge.color)

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
        view_graph.node("APP")
        return root, view_graph

    def paint_view_tree(self, tree, activity_name, graph):
        node_label = self.get_label_name(tree)
        node_name = self.get_node_name(node_label)
        graph.node(name=node_name, label=node_label, color=tree.color)
        graph.edge(activity_name, node_name)

        for edge in tree.edges:
            graph.edge(node_name, edge.value, color=edge.color)

        for node in tree.nodes:
            self.add_view_node(node, graph, node_name)
        for handler in tree.handlers:
            self.add_handler_node(handler, graph, node_name)

    @staticmethod
    def paint_child(child_node, view_graph):
        if child_node.attributes and child_node.hasAttribute("name"):
            color = 'black'
            # 若有变化，改变不同颜色
            if child_node.attributes.__contains__("diff:delete"):
                color = 'red'
            elif child_node.attributes.__contains__("diff:insert"):
                color = 'green'

            child_node_name = child_node.getAttribute("name")
            view_graph.node(name=child_node_name, color=color)
            view_graph.edge("APP", child_node_name)
            return child_node_name

    def start_draw(self):
        root, view_graph = self.create_view_graph()
        for child in root.childNodes:
            # 处理Activity和Dialog
            child_node_name = self.paint_child(child, view_graph)
            # 处理Activity下的View
            for view_child in child.childNodes:
                if view_child.nodeName == 'View':
                    view_tree = self.get_view_node(view_child)
                    self.paint_view_tree(view_tree, child_node_name, view_graph)
        view_graph.view(directory=self.result_path, filename="gui_diff")


def get_project_path():
    return "D:\\PyCharm\\code\\diff_apk"


if __name__ == "__main__":
    draw = DrawGUIGraph(os.path.join(get_project_path(), "res\\res.xml"), os.path.join(get_project_path(), "res"))
    draw.start_draw()
