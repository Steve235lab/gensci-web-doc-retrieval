#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from time import sleep
import requests
import threading


def enable_undeadthread():
    cnt = 10
    while cnt:
        try:
            requests.get("http://42.192.44.52:8000/undeadthread/", )
        except Exception:
            cnt -= 1
            sleep(1)
        else:
            break


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
    execute_from_command_line(sys.argv)

    threading.Thread(target=enable_undeadthread, daemon=True).start()


if __name__ == '__main__':
    main()
