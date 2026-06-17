# -*- coding: utf-8 -*-
import os
import sys


def ui_bundle_dir():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "ddg")
    return os.path.dirname(__file__)
