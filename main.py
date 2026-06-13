from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv(verbose=True)
load_dotenv(".env.local", override=True)


class State(TypedDict):
    input: str
    user_feedback: str


def first_step(state: State) -> None:
    print("First step")

def second_step(state: State) -> None:
    print("Second step")

def human_feedback(state: State) -> None:
    print("Human feedback")

def main():
    builder = StateGraph(State)
    builder.add_node('first_step', first_step)
    builder.add_node('second_step', second_step)
    builder.add_node('human_feedback', human_feedback)
    builder.add_edge(START, 'first_step')
    builder.add_edge('first_step', 'human_feedback')
    builder.add_edge('human_feedback', 'second_step')
    builder.add_edge('second_step', END)

    conn = sqlite3.connect('checkpoints.sqlite', check_sum_thread=False)
    # memory = MemorySaver()
    memory = SqliteSaver(conn)
    graph = builder.compile(checkpointer=memory, interrupt_before=['human_feedback'])

    graph.get_graph().draw_mermaid_png(output_file_path='graph.png')

    thread = {
        'configurable': {
            'thread_id': 'xx12yy32'
        }
    }
    user_input = {
        'input': 'Hello world!',
    }

    for event in graph.stream(user_input, thread, stream_mode='values'):
        print(event)

    print(graph.get_state(thread).next)

    user_feedback = str(input('Tell me how you want to update state? '))

    graph.update_state(thread, {'user_feedback': user_feedback}, as_node='human_feedback')

    print('Updated state: ')
    print(graph.get_state(thread))

if __name__ == "__main__":
    main()
