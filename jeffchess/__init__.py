#!/usr/bin/env python3

import logging
import argparse
import sys
from util import Util

name = "jeffchess"
__all__ = ["main", "util"]
with open('jeffchess/version.py') as f:
    exec(f.read())
