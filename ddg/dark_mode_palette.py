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
    # Levels bien separados: window → base → button tienen ~25-30 pts de diferencia
    window    = QtGui.QColor(22,  38,  72)   # navy medio — no tan oscuro
    base      = QtGui.QColor(30,  52,  95)   # panel/inputs — claramente más claro
    alt_base  = QtGui.QColor(26,  44,  82)   # filas alternas
    btn       = QtGui.QColor(42,  68, 118)   # botones — nivel superior visible
    highlight = QtGui.QColor(91, 160, 235)   # azul vivo para selección / foco
    text      = QtGui.QColor(220, 230, 255)  # blanco con tinte azul suave
    dim_text  = QtGui.QColor(120, 148, 195)  # texto deshabilitado / placeholder
    border    = QtGui.QColor(58,  84, 138)   # borde visible entre paneles

    p.setColor(QtGui.QPalette.ColorRole.Window,           window)
    p.setColor(QtGui.QPalette.ColorRole.WindowText,       text)
    p.setColor(QtGui.QPalette.ColorRole.Base,             base)
    p.setColor(QtGui.QPalette.ColorRole.AlternateBase,    alt_base)
    p.setColor(QtGui.QPalette.ColorRole.PlaceholderText,  dim_text)
    p.setColor(QtGui.QPalette.ColorRole.Text,             text)
    p.setColor(QtGui.QPalette.ColorRole.Button,           btn)
    p.setColor(QtGui.QPalette.ColorRole.ButtonText,       text)
    p.setColor(QtGui.QPalette.ColorRole.BrightText,       QtGui.QColor(255, 120, 100))
    p.setColor(QtGui.QPalette.ColorRole.Highlight,        highlight)
    p.setColor(QtGui.QPalette.ColorRole.HighlightedText,  QtGui.QColor(10, 20, 50))
    p.setColor(QtGui.QPalette.ColorRole.Link,             highlight)
    p.setColor(QtGui.QPalette.ColorRole.Mid,              border)
    p.setColor(QtGui.QPalette.ColorRole.Dark,             QtGui.QColor(14, 26, 52))
    p.setColor(QtGui.QPalette.ColorRole.Shadow,           QtGui.QColor(8,  15, 32))
    p.setColor(QtGui.QPalette.ColorRole.Midlight,         QtGui.QColor(52, 78, 130))
    p.setColor(QtGui.QPalette.ColorRole.ToolTipBase,      btn)
    p.setColor(QtGui.QPalette.ColorRole.ToolTipText,      text)

    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, dim_text)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text,       dim_text)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, dim_text)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight,  QtGui.QColor(40, 68, 110))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, dim_text)
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


def BiophilicLightPalette():
    p = QtGui.QPalette()
    cream        = QtGui.QColor(245, 240, 232)   # #F5F0E8 lino cálido
    panel        = QtGui.QColor(237, 232, 220)   # #EDE8DC arena suave
    alt_panel    = QtGui.QColor(228, 222, 208)   # ligeramente más oscuro
    btn          = QtGui.QColor(220, 213, 198)   # botones arena
    moss         = QtGui.QColor(90,  122,  74)   # #5A7A4A musgo bosque
    leaf         = QtGui.QColor(125, 171,  92)   # #7DAB5C verde hoja
    text_dark    = QtGui.QColor(44,  36,  22)    # #2C2416 marrón cálido
    text_mid     = QtGui.QColor(107,  92,  62)   # #6B5C3E tierra media
    border_sand  = QtGui.QColor(200, 186, 160)   # #C8BAA0 arena borde

    p.setColor(QtGui.QPalette.ColorRole.Window,           cream)
    p.setColor(QtGui.QPalette.ColorRole.WindowText,       text_dark)
    p.setColor(QtGui.QPalette.ColorRole.Base,             panel)
    p.setColor(QtGui.QPalette.ColorRole.AlternateBase,    alt_panel)
    p.setColor(QtGui.QPalette.ColorRole.PlaceholderText,  text_mid)
    p.setColor(QtGui.QPalette.ColorRole.Text,             text_dark)
    p.setColor(QtGui.QPalette.ColorRole.Button,           btn)
    p.setColor(QtGui.QPalette.ColorRole.ButtonText,       text_dark)
    p.setColor(QtGui.QPalette.ColorRole.BrightText,       QtGui.QColor(180, 60, 40))
    p.setColor(QtGui.QPalette.ColorRole.Highlight,        leaf)
    p.setColor(QtGui.QPalette.ColorRole.HighlightedText,  QtGui.QColor(255, 255, 255))
    p.setColor(QtGui.QPalette.ColorRole.Link,             moss)
    p.setColor(QtGui.QPalette.ColorRole.Dark,             border_sand)
    p.setColor(QtGui.QPalette.ColorRole.Shadow,           QtGui.QColor(160, 148, 128))
    p.setColor(QtGui.QPalette.ColorRole.Mid,              QtGui.QColor(210, 202, 186))
    p.setColor(QtGui.QPalette.ColorRole.Midlight,         QtGui.QColor(248, 244, 238))
    p.setColor(QtGui.QPalette.ColorRole.ToolTipBase,      QtGui.QColor(60, 50, 30))
    p.setColor(QtGui.QPalette.ColorRole.ToolTipText,      QtGui.QColor(230, 220, 200))

    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, text_mid)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text,       text_mid)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, text_mid)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight,  QtGui.QColor(180, 200, 160))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, text_mid)
    return p


def BiophilicDarkPalette():
    p = QtGui.QPalette()
    forest_night = QtGui.QColor(30,  35,  24)    # #1E2318 bosque noche
    earth_shadow = QtGui.QColor(37,  43,  30)    # #252B1E tierra sombra
    alt_dark     = QtGui.QColor(28,  34,  22)    # filas alternas
    btn_dark     = QtGui.QColor(48,  56,  38)    # botones oscuros
    leaf         = QtGui.QColor(125, 171,  92)   # #7DAB5C verde hoja
    fresh        = QtGui.QColor(168, 200, 128)   # #A8C880 verde fresco
    linen        = QtGui.QColor(232, 224, 208)   # #E8E0D0 lino claro
    muted_linen  = QtGui.QColor(160, 150, 130)   # texto secundario
    moss_border  = QtGui.QColor(61,  74,  50)    # #3D4A32 musgo oscuro

    p.setColor(QtGui.QPalette.ColorRole.Window,           forest_night)
    p.setColor(QtGui.QPalette.ColorRole.WindowText,       linen)
    p.setColor(QtGui.QPalette.ColorRole.Base,             earth_shadow)
    p.setColor(QtGui.QPalette.ColorRole.AlternateBase,    alt_dark)
    p.setColor(QtGui.QPalette.ColorRole.PlaceholderText,  muted_linen)
    p.setColor(QtGui.QPalette.ColorRole.Text,             linen)
    p.setColor(QtGui.QPalette.ColorRole.Button,           btn_dark)
    p.setColor(QtGui.QPalette.ColorRole.ButtonText,       linen)
    p.setColor(QtGui.QPalette.ColorRole.BrightText,       QtGui.QColor(255, 120, 100))
    p.setColor(QtGui.QPalette.ColorRole.Highlight,        leaf)
    p.setColor(QtGui.QPalette.ColorRole.HighlightedText,  QtGui.QColor(20, 28, 14))
    p.setColor(QtGui.QPalette.ColorRole.Link,             fresh)
    p.setColor(QtGui.QPalette.ColorRole.Dark,             QtGui.QColor(18, 22, 14))
    p.setColor(QtGui.QPalette.ColorRole.Shadow,           QtGui.QColor(10, 12, 8))
    p.setColor(QtGui.QPalette.ColorRole.Mid,              QtGui.QColor(42, 50, 34))
    p.setColor(QtGui.QPalette.ColorRole.Midlight,         QtGui.QColor(50, 60, 40))
    p.setColor(QtGui.QPalette.ColorRole.ToolTipBase,      btn_dark)
    p.setColor(QtGui.QPalette.ColorRole.ToolTipText,      linen)

    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, muted_linen)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text,       muted_linen)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, muted_linen)
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight,  QtGui.QColor(60, 80, 45))
    p.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, muted_linen)
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
