import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from __init__ import app

manager = Manager(app)


manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='127.0.0.1',
    port='4800'
    )
)


if __name__ == "__main__":
    manager.run()