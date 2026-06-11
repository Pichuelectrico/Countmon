# -*- coding: utf-8 -*-
#
# Countmon
# Author: Peter Ersts (ersts@amnh.org)
#
# --------------------------------------------------------------------------
#
# This file is part of the Countmon application.
# Countmon is built on DotDotGoose (https://github.com/persts/DotDotGoose), which was forked from Nenetic.
#
# Countmon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Countmon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with with this software.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------
from PyQt6 import QtCore, QtGui


def NavyModePalette():
    p = QtGui.QPalette()
    navy_dark = QtGui.QColor(12, 20, 45)
    navy_mid = QtGui.QColor(20, 35, 75)
    navy_btn = QtGui.QColor(28, 48, 100)
    highlight = QtGui.QColor(42, 130, 218)
    white = QtCore.Qt.GlobalColor.white

    p.setColor(QtGui.QPalette.ColorRole.Window, navy_dark)
    p.setColor(QtGui.QPalette.ColorRole.WindowText, white)
    p.setColor(QtGui.QPalette.ColorRole.Base, navy_mid)
    p.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(16, 28, 60))
    p.setColor(QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(140, 160, 200))
    p.setColor(QtGui.QPalette.ColorRole.Text, white)
    p.setColor(QtGui.QPalette.ColorRole.Button, navy_btn)
    p.setColor(QtGui.QPalette.ColorRole.ButtonText, white)
    p.setColor(QtGui.QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
    p.setColor(QtGui.QPalette.ColorRole.Highlight, highlight)
    p.setColor(QtGui.QPalette.ColorRole.HighlightedText, white)
    p.setColor(QtGui.QPalette.ColorRole.Link, highlight)
    p.setColor(QtGui.QPalette.ColorRole.Dark, QtGui.QColor(8, 14, 32))
    p.setColor(QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(4, 8, 18))

    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(80, 100, 140))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(80, 100, 140))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(80, 100, 140))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(30, 50, 90))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(80, 100, 140))

    p.setColor(QtGui.QPalette.ColorRole.ToolTipBase, navy_btn)
    p.setColor(QtGui.QPalette.ColorRole.ToolTipText, white)
    return p


def NatureGreenPalette():
    p = QtGui.QPalette()
    # Background tones — muted sage / forest greens
    window      = QtGui.QColor(42,  58,  46)   # dark sage
    base        = QtGui.QColor(52,  72,  56)   # slightly lighter sage
    alt_base    = QtGui.QColor(36,  50,  40)   # darker sage for alternating rows
    btn         = QtGui.QColor(60,  82,  64)   # button background
    highlight   = QtGui.QColor(102, 170, 102)  # pastel green selection
    text        = QtGui.QColor(220, 240, 220)  # near-white with green tint
    dim_text    = QtGui.QColor(140, 170, 140)  # muted for placeholders / disabled

    p.setColor(QtGui.QPalette.ColorRole.Window,           window)
    p.setColor(QtGui.QPalette.ColorRole.WindowText,       text)
    p.setColor(QtGui.QPalette.ColorRole.Base,             base)
    p.setColor(QtGui.QPalette.ColorRole.AlternateBase,    alt_base)
    p.setColor(QtGui.QPalette.ColorRole.PlaceholderText,  dim_text)
    p.setColor(QtGui.QPalette.ColorRole.Text,             text)
    p.setColor(QtGui.QPalette.ColorRole.Button,           btn)
    p.setColor(QtGui.QPalette.ColorRole.ButtonText,       text)
    p.setColor(QtGui.QPalette.ColorRole.BrightText,       QtGui.QColor(255, 120, 120))
    p.setColor(QtGui.QPalette.ColorRole.Highlight,        highlight)
    p.setColor(QtGui.QPalette.ColorRole.HighlightedText,  QtGui.QColor(20, 30, 20))
    p.setColor(QtGui.QPalette.ColorRole.Link,             QtGui.QColor(130, 200, 130))
    p.setColor(QtGui.QPalette.ColorRole.Dark,             QtGui.QColor(28, 40, 30))
    p.setColor(QtGui.QPalette.ColorRole.Shadow,           QtGui.QColor(16, 24, 18))
    p.setColor(QtGui.QPalette.ColorRole.ToolTipBase,      btn)
    p.setColor(QtGui.QPalette.ColorRole.ToolTipText,      text)

    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, dim_text)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text,       dim_text)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, dim_text)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight,  QtGui.QColor(60, 90, 60))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, dim_text)
    return p


def DarkModePalette():
    new_palette = QtGui.QPalette()
    new_palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))
    new_palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
    new_palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(42, 42, 42))
    new_palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(66, 66, 66))
    new_palette.setColor(QtGui.QPalette.ColorRole.PlaceholderText, QtCore.Qt.GlobalColor.white)
    new_palette.setColor(QtGui.QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)
    new_palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
    new_palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
    new_palette.setColor(QtGui.QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
    new_palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(42, 130, 218))
    new_palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.white)
    new_palette.setColor(QtGui.QPalette.ColorRole.Link, QtGui.QColor(42, 130, 218))
    new_palette.setColor(QtGui.QPalette.ColorRole.Dark, QtGui.QColor(35, 35, 35))
    new_palette.setColor(QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(20, 20, 20))

    new_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(127, 127, 127))
    new_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(127, 127, 127))
    new_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(127, 127, 127))
    new_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(80, 80, 80))
    new_palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(127, 127, 127))

    # These setting are not being applied for some reason in Qt6.5.3
    new_palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(127, 127, 127))
    new_palette.setColor(QtGui.QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.white)

    return new_palette
