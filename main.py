#!/usr/bin/python3
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
import os
import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from ddg import ExceptionHandler, MainWindow
from ddg.main_window import apply_theme

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if getattr(sys, "frozen", False):
        QtCore.QDir.addSearchPath("icons", os.path.join(sys._MEIPASS, "icons"))
        QtCore.QDir.addSearchPath("i18n", os.path.join(sys._MEIPASS, "i18n"))
    else:
        QtCore.QDir.addSearchPath("icons", "./icons/")
        QtCore.QDir.addSearchPath("i18n", "./i18n/")

    app.setStyle("fusion")

    # Modern font — prefer Inter, fall back to platform system fonts
    _font_families = ["Inter", "Segoe UI", "SF Pro Text", "Helvetica Neue", "Arial"]
    _font = QtGui.QFont()
    for _family in _font_families:
        _font.setFamily(_family)
        if (
            QtGui.QFontInfo(_font)
            .family()
            .lower()
            .startswith(_family.split()[0].lower())
        ):
            break
    _font.setPointSize(12)
    _font.setHintingPreference(QtGui.QFont.HintingPreference.PreferFullHinting)
    app.setFont(_font)

    settings = QtCore.QSettings("Countmon", "Countmon")
    apply_theme(settings.value("theme", "system"), app)

    translator = QtCore.QTranslator()
    if settings.value("locale"):
        if translator.load(
            QtCore.QLocale(settings.value("locale")), "ddg", "_", "i18n:/"
        ):
            QtCore.QCoreApplication.installTranslator(translator)
    else:
        if translator.load(QtCore.QLocale(), "ddg", "_", "i18n:/"):
            QtCore.QCoreApplication.installTranslator(translator)

    main = MainWindow()
    handler = ExceptionHandler()
    handler.exception.connect(main.display_exception)
    main.show()
    screen = app.primaryScreen()
    for s in app.screens():
        if screen.geometry().width() < s.geometry().width():
            screen = s
    main.windowHandle().setScreen(screen)
    w = int(screen.geometry().width() * 0.70)
    h = int(screen.geometry().height() * 0.77)
    main.resize(w, h)
    main.move(
        screen.geometry().x() + (screen.geometry().width() - w) // 2,
        screen.geometry().y() + ((screen.geometry().height() - h) // 2) - 25,
    )

    sys.exit(app.exec())
