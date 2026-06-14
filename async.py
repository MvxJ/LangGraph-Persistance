import operator

from dotenv import load_dotenv
from typing import Annotated, Any, Sequence
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


load_dotenv(verbose=True)
load_dotenv('.env.local', override=True)


class State(TypedDict):
    aggregate: Annotated[list, operator.add]
    which: str


class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State) -> Any:
        print(f'adding {self._value} to {state.get("aggregate")}')

        return {'aggregate': [self._value]}


def route_bc_or_cd(state: State) -> Sequence[str]:
    if state.get('which') == 'cd':
        return ['c', 'd']

    return ['b', 'c']

if __name__ == '__main__':
    print('Hello from async flow')

    builder = StateGraph(State)
    builder.add_node('a', ReturnNodeValue('I\'m node A'))
    builder.add_node('b', ReturnNodeValue('I\'m node B'))
    builder.add_node('c', ReturnNodeValue('I\'m node C'))
    builder.add_node('d', ReturnNodeValue('I\'m node D'))
    builder.add_node('e', ReturnNodeValue('I\'m node E'))
    builder.add_edge(START, 'a')
    builder.add_conditional_edges(
        'a',
        route_bc_or_cd,
        ['b', 'c', 'd']

    )

    for node in ['b','c','d']:
        builder.add_edge(node, 'e')

    builder.add_edge('e', END)

    graph = builder.compile()
    graph.get_graph().draw_mermaid_png(output_file_path='async.png')

    graph.invoke(
        {
            'aggregate': [],
            'which': 'cd',
        },
        {
            'configurable': {
                'thread_id': 'xx1144xx'
            }
        }
    )