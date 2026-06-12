# -*- coding: utf-8 -*-
import json
import os

from PyQt6 import QtCore, QtGui, QtWidgets


class WorkspaceWidget(QtWidgets.QWidget):
    """
    Main tabbed workspace widget.

    Each tab holds an independent CentralWidget pointed at a subfolder.
    When the master folder has no subfolders the single tab points at the
    master folder itself, replicating the original single-folder behaviour.

    Workspace state (open tabs and last-used .pnt files) is persisted to
    ``<master>/.workspace.json`` automatically.
    """

    def __init__(self, master_path, parent=None):
        super().__init__(parent)
        self.master_path = master_path  # may be None (no-workspace mode)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Tab widget ────────────────────────────────────────────────────
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_tab)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)

        # "+" button in the top-left corner of the tab bar
        self._btn_new_tab = QtWidgets.QToolButton()
        self._btn_new_tab.setText(' + ')
        self._btn_new_tab.setToolTip('New tab  (Cmd+T / Ctrl+T)')
        self._btn_new_tab.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._btn_new_tab.setStyleSheet(
            'QToolButton { border: none; font-size: 14px; padding: 0 4px; }'
            'QToolButton:hover { color: #5A7A4A; }'
        )
        self._btn_new_tab.clicked.connect(self.open_new_tab_dialog)
        self.tab_widget.setCornerWidget(
            self._btn_new_tab, QtCore.Qt.Corner.TopLeftCorner
        )

        layout.addWidget(self.tab_widget)

        # ── Keyboard shortcuts ────────────────────────────────────────────
        sc_new = QtGui.QShortcut(
            QtGui.QKeySequence(
                QtCore.Qt.Modifier.CTRL | QtCore.Qt.Key.Key_T
            ),
            self,
        )
        sc_new.setContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc_new.activated.connect(self.open_new_tab_dialog)

        sc_close = QtGui.QShortcut(
            QtGui.QKeySequence(
                QtCore.Qt.Modifier.CTRL | QtCore.Qt.Key.Key_W
            ),
            self,
        )
        sc_close.setContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc_close.activated.connect(self._close_active_tab)

        # ── Open initial tabs ─────────────────────────────────────────────
        self._open_workspace()

    # ── Helpers ───────────────────────────────────────────────────────────

    def _subfolders(self):
        if not self.master_path:
            return []
        try:
            entries = os.listdir(self.master_path)
        except OSError:
            return []
        return sorted(
            d
            for d in entries
            if os.path.isdir(os.path.join(self.master_path, d))
            and not d.startswith('.')
        )

    def _workspace_file(self):
        if not self.master_path:
            return None
        return os.path.join(self.master_path, '.workspace.json')

    def _tab_label(self, path):
        """Human-readable tab label from a folder path."""
        return os.path.basename(path.rstrip(os.sep)) or path

    # ── Workspace open / restore ──────────────────────────────────────────

    def _open_workspace(self):
        ws_file = self._workspace_file()
        restored = False

        if ws_file and os.path.isfile(ws_file):
            try:
                with open(ws_file, 'r', encoding='utf-8') as fh:
                    state = json.load(fh)
                tabs = state.get('tabs', [])
                active_index = int(state.get('active_tab_index', 0))

                for tab in tabs:
                    folder = tab.get('folder', '')
                    pnt_file = tab.get('pnt_file') or None

                    if folder:
                        path = os.path.join(self.master_path, folder)
                    else:
                        path = self.master_path

                    if os.path.isdir(path):
                        self._add_tab(path, pnt_file=pnt_file, save_state=False)

                if self.tab_widget.count() > 0:
                    self.tab_widget.setCurrentIndex(
                        min(active_index, self.tab_widget.count() - 1)
                    )
                    restored = True
            except Exception:
                pass

        if not restored:
            subfolders = self._subfolders()
            if subfolders:
                for sf in subfolders:
                    self._add_tab(
                        os.path.join(self.master_path, sf), save_state=False
                    )
            elif self.master_path:
                self._add_tab(self.master_path, save_state=False)
            else:
                # No-workspace mode: one blank tab
                self._add_tab(None, save_state=False)

        self.save_workspace_state()

    # ── Tab management ────────────────────────────────────────────────────

    def _detect_pnt(self, path):
        """Return the best .pnt file inside *path*, or None if there is none.

        If multiple .pnt files exist the most-recently-modified one is chosen.
        """
        if not path or not os.path.isdir(path):
            return None
        candidates = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.lower().endswith('.pnt') and os.path.isfile(os.path.join(path, f))
        ]
        if not candidates:
            return None
        return max(candidates, key=os.path.getmtime)

    def _add_tab(self, path, pnt_file=None, save_state=True):
        # Import here to avoid circular imports at module level
        from ddg.central_widget import CentralWidget

        cw = CentralWidget(parent=self)

        if pnt_file and os.path.isfile(pnt_file):
            cw.canvas.load_points(pnt_file)
        else:
            auto_pnt = self._detect_pnt(path)
            if auto_pnt:
                cw.canvas.load_points(auto_pnt)
            elif path and os.path.isdir(path):
                cw.load_path(path)

        # Update tab title when the user later changes the folder inside the tab
        cw.canvas.directory_set.connect(
            lambda d, widget=cw: self._refresh_tab_title(widget, d)
        )
        # Save state whenever the in-tab quick-save fires
        cw.canvas.saving.connect(self.save_workspace_state)

        label = self._tab_label(path) if path else 'Untitled'
        index = self.tab_widget.addTab(cw, label)
        self.tab_widget.setCurrentIndex(index)

        if save_state:
            self.save_workspace_state()
        return index

    def _close_tab(self, index):
        if self.tab_widget.count() <= 1:
            QtWidgets.QMessageBox.information(
                self,
                'Cannot Close Tab',
                'At least one tab must remain open.',
            )
            return
        cw = self.tab_widget.widget(index)
        if not cw.canvas.dirty_data_check():
            return
        self.tab_widget.removeTab(index)
        cw.deleteLater()
        self.save_workspace_state()

    def _close_active_tab(self):
        self._close_tab(self.tab_widget.currentIndex())

    def _on_tab_changed(self, _index):
        self.save_workspace_state()

    def _refresh_tab_title(self, widget, directory):
        for i in range(self.tab_widget.count()):
            if self.tab_widget.widget(i) is widget:
                self.tab_widget.setTabText(i, self._tab_label(directory))
                self.save_workspace_state()
                break

    # ── Public API ────────────────────────────────────────────────────────

    def open_new_tab_dialog(self):
        """Open a file-picker and add the chosen folder as a new tab."""
        start = self.master_path or ''
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Folder for New Tab', start
        )
        if path:
            self._add_tab(path)

    def save_workspace_state(self):
        ws_file = self._workspace_file()
        if not ws_file:
            return
        tabs = []
        for i in range(self.tab_widget.count()):
            cw = self.tab_widget.widget(i)
            canvas_dir = (cw.canvas.directory or '').rstrip(os.sep)
            if self.master_path and canvas_dir == self.master_path.rstrip(os.sep):
                folder = ''
            else:
                folder = os.path.basename(canvas_dir) if canvas_dir else ''
            tabs.append(
                {
                    'folder': folder,
                    'pnt_file': cw.canvas.previous_file_name,
                }
            )
        state = {
            'workspace_version': 1,
            'tabs': tabs,
            'active_tab_index': self.tab_widget.currentIndex(),
        }
        try:
            with open(ws_file, 'w', encoding='utf-8') as fh:
                json.dump(state, fh, indent=2)
        except OSError:
            pass

    def check_all_tabs_before_close(self):
        """
        Iterate every tab and run its dirty-data check.
        Returns True if the caller may proceed; False if the user cancelled.
        """
        for i in range(self.tab_widget.count()):
            cw = self.tab_widget.widget(i)
            # Bring the tab into view so the user knows which one is asking
            self.tab_widget.setCurrentIndex(i)
            if not cw.canvas.dirty_data_check():
                return False
        return True

    def active_central_widget(self):
        return self.tab_widget.currentWidget()

    # ── Delegates for MainWindow panel-toggle buttons ─────────────────────

    def toggle_left_panel(self, hide):
        cw = self.active_central_widget()
        if cw is not None:
            cw.toggle_left_panel(hide)

    def toggle_right_panel(self, hide):
        cw = self.active_central_widget()
        if cw is not None:
            cw.toggle_right_panel(hide)
