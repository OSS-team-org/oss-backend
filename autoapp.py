# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
import logging
logging.basicConfig(level=logging.DEBUG)

from mentor.app import create_app
from mentor.settings import ProdConfig

CONFIG = ProdConfig

app = create_app(CONFIG)