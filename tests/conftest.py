"""Configuration for the pytest test suite."""

import os


def get_fake_script(name: str) -> str:
    """Get path to a fake script.

    Parameters:
        name: The script name.

    Returns:
        The fake script path.
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakescripts", name)
