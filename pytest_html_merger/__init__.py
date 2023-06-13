import os
import sys

CUR_PATH = "{0}/".format(os.path.dirname(__file__))

sys.path.append(CUR_PATH)

import pytest_html_merger.version as version_mod

__version__ = version_mod.version
