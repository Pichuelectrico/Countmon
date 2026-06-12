# -*- coding: utf-8 -*-
#
# Dot Target Counter
# Author: Peter Ersts (ersts@amnh.org)
#
# --------------------------------------------------------------------------
#
# This file is part of the Dot Target Counter application.
# Countmon is built on DotDotGoose (https://github.com/persts/DotDotGoose), which was forked from Nenetic.
#
# Dot Target Counter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dot Target Counter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with with this software.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------
from PyQt6 import QtWidgets, QtCore, QtGui

from ddg import __version__
from ddg.about_dialog import AboutDialog
from ddg.dark_mode_palette import (
    DarkModePalette, NavyModePalette, NatureGreenPalette,
    NightForestPalette, PokemonPalette, BiophilicLightPalette,
)
from ddg.biophilic_theme import BIOPHILIC_BASE_QSS
from ddg.workspace_widget import WorkspaceWidget


def apply_theme(name, app=None):
    """Apply a named theme to the application palette."""
    if app is None:
        app = QtWidgets.QApplication.instance()

    if name == 'dark':
        app.setPalette(DarkModePalette())
    elif name == 'navy':
        app.setPalette(NavyModePalette())
    elif name == 'nature':
        app.setPalette(NatureGreenPalette())
    elif name == 'night_forest':
        app.setPalette(NightForestPalette())
    elif name == 'pokemon':
        app.setPalette(PokemonPalette())
    elif name == 'light':
        app.setPalette(BiophilicLightPalette())
    else:
        if app.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Dark:
            app.setPalette(DarkModePalette())
        else:
            app.setPalette(BiophilicLightPalette())

    # Clear first so Qt re-parses palette() references with the new palette.
    app.setStyleSheet('')
    app.setStyleSheet(BIOPHILIC_BASE_QSS)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, master_path=None):
        """
        Parameters
        ----------
        master_path : str or None
            Path to the workspace (master folder) chosen in WorkspaceDialog.
            None means no-workspace mode — a single blank tab is opened.
        """
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle('Dot Target Counter')
        self.setWindowIcon(QtGui.QIcon('icons:logo_countmon.png'))

        self.about_dialog = AboutDialog(self)

        self.error_widget = QtWidgets.QTextBrowser()
        self.error_widget.setWindowTitle(self.tr('EXCEPTION DETECTED'))
        self.error_widget.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.error_widget.resize(900, 500)

        # ── Menu bar ───────────────────────────────────────────────────────
        self.setMenuBar(QtWidgets.QMenuBar())
        self.menuBar().setNativeMenuBar(False)

        # File
        menu = self.menuBar().addMenu(self.tr('File'))
        menu.setObjectName('File')
        menu.addAction(self.tr('Open Workspace…'), self._open_workspace_dialog)
        menu.addSeparator()
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
            ('system',       self.tr('System (default)')),
            ('light',        self.tr('Light')),
            ('dark',         self.tr('Dark')),
            ('navy',         self.tr('Navy Blue')),
            ('nature',       self.tr('Nature Green')),
            ('night_forest', self.tr('Night Forest')),
            ('pokemon',      self.tr('Pokémon')),
        ]
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
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

        # ── OS colour-scheme auto-update ───────────────────────────────────
        # Keep a strong reference so the Python wrapper isn't garbage-collected
        # (dropping the signal connection silently).
        self._style_hints = QtWidgets.QApplication.instance().styleHints()
        self._style_hints.colorSchemeChanged.connect(
            self._on_os_color_scheme_changed
        )

        # ── Panel toggle buttons (top-right corner) ────────────────────────
        corner = QtWidgets.QWidget()
        corner_layout = QtWidgets.QHBoxLayout(corner)
        corner_layout.setContentsMargins(0, 2, 6, 2)
        corner_layout.setSpacing(4)

        btn_css = (
            'QPushButton {'
            '  border: 1px solid #888; border-radius: 6px;'
            '  padding: 3px 12px; font-size: 11px;'
            '  min-width: 28px;'
            '}'
            'QPushButton:checked {'
            '  background: rgba(90,122,74,180); border-color: #5A7A4A;'
            '}'
            'QPushButton:hover { background: rgba(90,122,74,60); }'
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

        # ── Open the workspace ─────────────────────────────────────────────
        self._load_workspace(master_path)

    # ── Workspace helpers ─────────────────────────────────────────────────

    def _load_workspace(self, master_path):
        workspace = WorkspaceWidget(master_path, parent=self)
        self.setCentralWidget(workspace)
        self._update_title(master_path)

    def _open_workspace_dialog(self):
        """File > Open Workspace — lets the user switch workspace at any time."""
        from ddg.workspace_dialog import WorkspaceDialog
        dialog = WorkspaceDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_path = dialog.selected_path
            # Dirty-check current workspace before switching
            current = self.centralWidget()
            if isinstance(current, WorkspaceWidget):
                if not current.check_all_tabs_before_close():
                    return
            self._load_workspace(new_path)

    def _update_title(self, master_path):
        if master_path:
            import os
            name = os.path.basename(master_path.rstrip(os.sep)) or master_path
            self.setWindowTitle(f'Dot Target Counter — {name}')
        else:
            self.setWindowTitle('Dot Target Counter')

    # ── Panel toggles ─────────────────────────────────────────────────────

    def _toggle_left_panel(self, checked):
        self._btn_left_panel.setText(('▶  ' if checked else '◀  ') + self.tr('Left Panel'))
        cw = self.centralWidget()
        if isinstance(cw, WorkspaceWidget):
            cw.toggle_left_panel(checked)

    def _toggle_right_panel(self, checked):
        self._btn_right_panel.setText(self.tr('Right Panel') + ('  ◀' if checked else '  ▶'))
        cw = self.centralWidget()
        if isinstance(cw, WorkspaceWidget):
            cw.toggle_right_panel(checked)

    # ── Theme ─────────────────────────────────────────────────────────────

    def _set_theme(self, name):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('theme', name)
        apply_theme(name)

    def _on_os_color_scheme_changed(self, _scheme):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        if settings.value('theme', 'system') == 'system':
            apply_theme('system')

    # ── Close ─────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        cw = self.centralWidget()
        if isinstance(cw, WorkspaceWidget):
            if cw.check_all_tabs_before_close():
                cw.save_workspace_state()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    # ── Errors ────────────────────────────────────────────────────────────

    def display_exception(self, error):
        self.error_widget.clear()
        for line in error:
            self.error_widget.append(line)
        self.error_widget.show()

    # ── Language ──────────────────────────────────────────────────────────

    def en_US(self):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('locale', 'en_US')
        self.restart_message()

    def es_CO(self):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('locale', 'es_CO')
        self.restart_message()

    def fr_FR(self):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('locale', 'fr')
        self.restart_message()

    def hu_HU(self):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('locale', 'hu')
        self.restart_message()

    def vi_VN(self):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('locale', 'vi_VN')
        self.restart_message()

    def zh_Hans_CN(self):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('locale', 'zh_Hans_CN')
        self.restart_message()

    def restart_message(self):
        QtWidgets.QMessageBox.warning(
            self,
            self.tr('Restart Required'),
            self.tr('You must restart the application for the language setting to be applied.'),
            QtWidgets.QMessageBox.StandardButton.Ok,
        )

    def quit(self):
        self.close()
