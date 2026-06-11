# -*- coding: utf-8 -*-
#
# DotDotGoose
# Author: Peter Ersts (ersts@amnh.org)
#
# --------------------------------------------------------------------------
#
# This file is part of the DotDotGoose application.
# DotDotGoose was forked from the Neural Network Image Classifier (Nenetic).
#
# DotDotGoose is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DotDotGoose is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with with this software.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------
from ddg.central_widget import CentralWidget
from PyQt6 import QtWidgets, QtCore, QtGui
from ddg.about_dialog import AboutDialog
from ddg import __version__
from ddg.dark_mode_palette import DarkModePalette, NavyModePalette, NatureGreenPalette


def apply_theme(name, app=None):
    """Apply a named theme to the application palette."""
    if app is None:
        app = QtWidgets.QApplication.instance()
    tooltip_dark = "QToolTip { color: #ffffff; background-color: #000000; border: 0px; padding: 2px}"
    tooltip_navy = "QToolTip { color: #ffffff; background-color: #0c1430; border: 0px; padding: 2px}"
    tooltip_light = ""

    if name == 'dark':
        app.setPalette(DarkModePalette())
        app.setStyleSheet(tooltip_dark)
    elif name == 'navy':
        app.setPalette(NavyModePalette())
        app.setStyleSheet(tooltip_navy)
    elif name == 'nature':
        app.setPalette(NatureGreenPalette())
        app.setStyleSheet(
            "QToolTip { color: #dcf0dc; background-color: #2a3a2e; border: 0px; padding: 2px}")
    elif name == 'light':
        app.setPalette(QtGui.QPalette())
        app.setStyleSheet(tooltip_light)
    else:
        # system: restore palette and let OS decide
        app.setPalette(QtGui.QPalette())
        app.setStyleSheet(tooltip_light)
        if app.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Dark:
            app.setPalette(DarkModePalette())
            app.setStyleSheet(tooltip_dark)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle('DotDotGoose [v {}]'.format(__version__))
        self.setWindowIcon(QtGui.QIcon("icons:ddg.png"))
        self.setCentralWidget(CentralWidget())
        self.about_dialog = AboutDialog(self)

        self.error_widget = QtWidgets.QTextBrowser()
        self.error_widget.setWindowTitle(self.tr('EXCEPTION DETECTED'))
        self.error_widget.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.error_widget.resize(900, 500)

        self.setMenuBar(QtWidgets.QMenuBar())
        self.menuBar().setNativeMenuBar(False)

        # File
        menu = self.menuBar().addMenu(self.tr('File'))
        menu.setObjectName('File')
        menu.addAction(self.tr('Quit'), self.quit)

        # Language
        menu = self.menuBar().addMenu(self.tr('Language'))
        menu.setObjectName('Language')
        menu.addAction(self.tr('Chinese (Mandarin)'), self.zh_Hans_CN)
        menu.addAction(self.tr('English'), self.en_US)
        menu.addAction(self.tr('French'), self.fr_FR)
        menu.addAction(self.tr('Hungarian'), self.hu_HU)
        menu.addAction(self.tr('Spanish'), self.es_CO)
        menu.addAction(self.tr('Vietnamese'), self.vi_VN)

        # Appearance
        appear_menu = self.menuBar().addMenu(self.tr('Appearance'))
        appear_menu.setObjectName('Appearance')
        theme_group = QtGui.QActionGroup(self)
        theme_group.setExclusive(True)

        themes = [
            ('system', self.tr('System (default)')),
            ('light',  self.tr('Light')),
            ('dark',   self.tr('Dark')),
            ('navy',   self.tr('Navy Blue')),
            ('nature', self.tr('Nature Green')),
        ]
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        current_theme = settings.value('theme', 'system')

        for key, label in themes:
            action = QtGui.QAction(label, self)
            action.setCheckable(True)
            action.setChecked(key == current_theme)
            action.setData(key)
            action.triggered.connect(lambda checked, k=key: self._set_theme(k))
            theme_group.addAction(action)
            appear_menu.addAction(action)

        self.menuBar().addSeparator()
        self.menuBar().addAction(self.tr('About'), self.about_dialog.show)

        # ── Panel toggle buttons in menu bar right corner ──────────────────
        corner = QtWidgets.QWidget()
        corner_layout = QtWidgets.QHBoxLayout(corner)
        corner_layout.setContentsMargins(0, 2, 6, 2)
        corner_layout.setSpacing(4)

        btn_css = (
            "QPushButton {"
            "  border: 1px solid #888; border-radius: 3px;"
            "  padding: 2px 8px; font-size: 12px;"
            "  min-width: 28px;"
            "}"
            "QPushButton:checked {"
            "  background: rgba(42,130,218,160); border-color: #2a82da;"
            "}"
            "QPushButton:hover { background: rgba(128,128,128,60); }"
        )

        self._btn_left_panel = QtWidgets.QPushButton('◀  ' + self.tr('Left Panel'))
        self._btn_left_panel.setCheckable(True)
        self._btn_left_panel.setStyleSheet(btn_css)
        self._btn_left_panel.setToolTip(self.tr('Hide / show left panel  [←]'))
        self._btn_left_panel.toggled.connect(self._toggle_left_panel)

        self._btn_right_panel = QtWidgets.QPushButton(self.tr('Right Panel') + '  ▶')
        self._btn_right_panel.setCheckable(True)
        self._btn_right_panel.setStyleSheet(btn_css)
        self._btn_right_panel.setToolTip(self.tr('Hide / show right panel  [→]'))
        self._btn_right_panel.toggled.connect(self._toggle_right_panel)

        corner_layout.addWidget(self._btn_left_panel)
        corner_layout.addWidget(self._btn_right_panel)
        self.menuBar().setCornerWidget(corner, QtCore.Qt.Corner.TopRightCorner)

    def _toggle_left_panel(self, checked):
        self._btn_left_panel.setText(('▶  ' if checked else '◀  ') + self.tr('Left Panel'))
        self.centralWidget().toggle_left_panel(checked)

    def _toggle_right_panel(self, checked):
        self._btn_right_panel.setText(self.tr('Right Panel') + ('  ◀' if checked else '  ▶'))
        self.centralWidget().toggle_right_panel(checked)

    def _set_theme(self, name):
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        settings.setValue('theme', name)
        apply_theme(name)

    def closeEvent(self, event):
        if self.centralWidget().canvas.dirty_data_check():
            event.accept()
        else:
            event.ignore()

    def display_exception(self, error):
        self.error_widget.clear()
        for line in error:
            self.error_widget.append(line)
        self.error_widget.show()

    def en_US(self):
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        settings.setValue('locale', 'en_US')
        self.restart_message()

    def es_CO(self):
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        settings.setValue('locale', 'es_CO')
        self.restart_message()

    def fr_FR(self):
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        settings.setValue('locale', 'fr')
        self.restart_message()

    def hu_HU(self):
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        settings.setValue('locale', 'hu')
        self.restart_message()

    def vi_VN(self):
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        settings.setValue('locale', 'vi_VN')
        self.restart_message()

    def zh_Hans_CN(self):
        settings = QtCore.QSettings("AMNH", "DotDotGoose")
        settings.setValue('locale', 'zh_Hans_CN')
        self.restart_message()

    def restart_message(self):
        QtWidgets.QMessageBox.warning(self, self.tr('Restart Required'),
                                      self.tr('You must restart the application for the language setting to be applied.'),
                                      QtWidgets.QMessageBox.StandardButton.Ok)

    def quit(self):
        self.close()
