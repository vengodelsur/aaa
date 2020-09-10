import json

from typeguard import typechecked


@typechecked
class DialogNode:
    def __init__(self, header_message: str):
        self.header_message = header_message
        self.transition_messages = []  # List[str]
        self.transition_nodes = []  # List['DialogNode']

    def add_transition(self, message: str, node: 'DialogNode'):
        self.transition_messages.append(message)
        self.transition_nodes.append(node)

    def get_choice_message(self) -> str:
        options = "\n".join(f"{i}) {message}" for i, message in enumerate(self.transition_messages))
        return f"{self.header_message}\n{options}"

    def get_transition_node(self, i: int):
        return self.transition_nodes[i]  # TODO: error handling


@typechecked
class DialogGraph:
    def __init__(self):
        self.nodes_dictionary = {}  # Dict[str, 'DialogNode']

    @classmethod
    def from_json(cls, filepath: str) -> 'DialogGraph':
        graph = cls()
        with open(filepath) as f:
            json_dialog_info = json.load(f)
        # read nodes
        for node_info in json_dialog_info:
            node = DialogNode(node_info["header_message"])
            # TODO: check if node exists
            # TODO: function for node adding
            graph.nodes_dictionary[node_info["node_id"]] = node
        # read transitions
        for node_info in json_dialog_info:
            # TODO: node getting
            node = graph.nodes_dictionary[node_info["node_id"]]
            for transition in node_info["transitions"]:
                target_node = graph.nodes_dictionary[transition["target_node_id"]]
                node.add_transition(transition["message"], target_node)
        return graph

    def to_img(self):
        pass


# TODO: read user input


if __name__ == '__main__':
    graph = DialogGraph.from_json('scenario.json')
    # TODO: may be switch to storing transitions in graph in terms of ids?
    # print([(node_id, node.transition_nodes) for node_id, node in graph.nodes_dictionary.items()])
