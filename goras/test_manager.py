#! /usr/bin/python3

import time
from manager import GorasManager

with GorasManager() as manager:
    manager.configure()
    manager.run()
    try:
        while True:
            time.sleep(1)
    except:
        pass