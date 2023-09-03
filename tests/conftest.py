"""Configuration for the pytest test suite."""

import os


def get_fake_script(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakescripts", name)
