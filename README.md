# LangGraph | Persistence

A small example project demonstrating **state persistence in an AI agent** built with [LangGraph](https://langchain-ai.github.io/langgraph/).

## What it's about

This project shows how a graph-based agent can **persist its conversation/state across steps** using a checkpointer, and how to **pause for human feedback** mid-execution and resume later.

Key concepts illustrated:

- **Checkpointing** — agent state is saved to a SQLite database (`SqliteSaver`) so it survives between runs. A `MemorySaver` (in-memory) alternative is also shown.
- **Threads** — each conversation is tracked by a `thread_id`, allowing the same agent to maintain separate, resumable histories.
- **Human-in-the-loop** — the graph interrupts before the `human_feedback` node (`interrupt_before`), lets a user inspect and update the state, then continues.

## Graph structure

```
START → first_step → human_feedback → second_step → END
```

The compiled graph is also exported as a diagram to `graph.png`.

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Setup

```bash
uv sync
```

Create a `.env` (or `.env.local`) file for any required environment variables.

## Run

```bash
uv run main.py
```

The script streams through the graph, pauses for your feedback, updates the persisted state, and prints the result. State is stored in `checkpoints.sqlite`.

## Tech stack

- LangGraph
- LangChain Community
- SQLite checkpointing (`langgraph-checkpoint-sqlite`)
- python-dotenv
