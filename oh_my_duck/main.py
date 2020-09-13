import json

from typeguard import typechecked


@typechecked
class DialogGraph:
    @typechecked
    class Node:
        def __init__(self, node_id: str, header_message: str):
            self.node_id = node_id  # str
            self.header_message = header_message  # str
            self.transition_messages = []  # List[str]
            self.transition_nodes = []  # List[str]

        def add_transition(self, message: str, node_id: str):
            self.transition_messages.append(message)
            self.transition_nodes.append(node_id)

        def get_choice_message(self) -> str:
            options = "\n".join(
                f"{i}) {message}" for i, message in enumerate(self.transition_messages))
            return f"{self.header_message}\n{options}"

        def get_transition_node_id(self, i: int) -> str:
            return self.transition_nodes[i]  # TODO: error handling

        def __bool__(self):
            return bool(self.transition_nodes)

    def __init__(self, root_node_id: str = 'start'):
        self.nodes_dictionary = {}  # Dict[str, 'DialogNode']
        self.root_node_id = root_node_id

    @classmethod
    def from_json(cls, filepath: str, root_node_id: str = 'start') -> 'DialogGraph':
        graph = cls(root_node_id)
        with open(filepath) as f:
            json_dialog_info = json.load(f)
        # read nodes
        for node_info in json_dialog_info:
            node = cls.Node(node_id=node_info["node_id"],
                            header_message=node_info["header_message"])
            # TODO: check if node exists
            # TODO: function for node adding
            graph.nodes_dictionary[node_info["node_id"]] = node
        # read transitions
        for node_info in json_dialog_info:
            node = graph.get_node(node_info["node_id"])
            for transition in node_info["transitions"]:
                node.add_transition(transition["message"], transition["target_node_id"])
        return graph

    def get_node(self, node_id: str) -> Node:
        return self.nodes_dictionary[node_id]

    def to_img(self):
        pass


class DialogManager:
    def __init__(self, graph: DialogGraph):
        self.graph = graph
        self.current_node_id = graph.root_node_id

    def read_user_input(self):
        current_node = self.graph.get_node(self.current_node_id)
        print(current_node.get_choice_message())
        # TODO: handling incorrect input
        chosen_option = int(input())
        self.current_node_id = current_node.get_transition_node_id(chosen_option)

    def run(self):
        while self.graph.get_node(self.current_node_id):
            self.read_user_input()
        print("GAME OVER")


if __name__ == '__main__':
    graph = DialogGraph.from_json('scenario.json')
    # TODO: get rid of the dictionary?
    # print([(node_id, node.transition_nodes) for node_id, node in graph.nodes_dictionary.items()])
    manager = DialogManager(graph)
    manager.run()
