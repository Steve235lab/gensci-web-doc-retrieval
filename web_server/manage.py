#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from time import sleep
import requests
import threading

from controller import CONTROLLER


def enable_undeadthread():
    sleep(5)
    requests.get("http://" + CONTROLLER.public_ip + "/undeadthread/")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    threading.Thread(target=enable_undeadthread, daemon=True).start()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
