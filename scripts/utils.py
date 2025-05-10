import subprocess

import uvicorn


def start() -> None:
    """Starts the Uvicorn server for the FastAPI application."""
    uvicorn.run("be_task_ca.app.main:app", host="0.0.0.0", port=8000, reload=True)


def auto_format() -> None:
    """Formats the code in the 'be_task_ca' directory using Black."""
    subprocess.call(["black", "be_task_ca"])


def run_linter() -> None:
    """Runs the Flake8 linter on the 'be_task_ca' directory."""
    subprocess.call(["flake8", "be_task_ca"])


def run_tests() -> None:
    """Runs Pytest to execute automated tests."""
    subprocess.call(["pytest"])


def create_dependency_graph() -> None:
    """Generates a dependency graph for the 'be_task_ca' package using Pydeps.

    The '--cluster' option groups related modules together in the graph.
    """
    subprocess.call(["pydeps", "be_task_ca", "--cluster"])


def check_types() -> None:
    """Runs MyPy to perform static type checking on the 'be_task_ca' directory."""
    subprocess.call(["mypy", "be_task_ca"])
