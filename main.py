# This file is needed only for bot-hosting.net !!!

import runpy
import sys

if "." not in sys.path:
    sys.path.insert(0, ".")

runpy.run_module("pixelazer", run_name="__main__")