# -*- coding: utf-8 -*-
import os
from PyQt6 import QtCore, QtGui, QtWidgets


class WorkspaceDialog(QtWidgets.QDialog):
    """Startup dialog for selecting or creating a workspace (master folder)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Dot Target Counter')
        self.setWindowIcon(QtGui.QIcon('icons:logo_countmon.png'))
        self.setMinimumSize(720, 440)
        self.setMaximumSize(900, 560)
        self._selected_path = None
        self._setup_ui()
        self._load_recent()

    # ── UI construction ───────────────────────────────────────────────────

    def _setup_ui(self):
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── LEFT PANEL — branding ─────────────────────────────────────────
        left = QtWidgets.QWidget()
        left.setObjectName('brandPanel')
        left.setStyleSheet(
            '#brandPanel {'
            '  background: qlineargradient('
            '    x1:0, y1:0, x2:0, y2:1,'
            '    stop:0 #2E3D22, stop:1 #1A2412'
            '  );'
            '}'
        )
        left.setFixedWidth(260)

        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.setContentsMargins(28, 40, 28, 32)
        left_layout.setSpacing(0)
        left_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Logo
        logo_lbl = QtWidgets.QLabel()
        logo_lbl.setPixmap(QtGui.QIcon('icons:logo_countmon.png').pixmap(72, 72))
        logo_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(logo_lbl)

        left_layout.addSpacing(18)

        # App name
        name_lbl = QtWidgets.QLabel('Dot Target\nCounter')
        name_lbl.setStyleSheet(
            'color: #E8F0DC;'
            'font-size: 26px;'
            'font-weight: 700;'
            'line-height: 1.2;'
        )
        name_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(name_lbl)

        left_layout.addSpacing(14)

        # Slogan
        slogan_lbl = QtWidgets.QLabel('"You dot the target,\nwe\'ll count it."')
        slogan_lbl.setStyleSheet(
            'color: #9AB87A;'
            'font-size: 13px;'
            'font-style: italic;'
            'line-height: 1.5;'
        )
        slogan_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        slogan_lbl.setWordWrap(True)
        left_layout.addWidget(slogan_lbl)

        left_layout.addStretch()

        # Version
        from ddg import __version__
        ver_lbl = QtWidgets.QLabel(f'v{__version__}')
        ver_lbl.setStyleSheet('color: #5A7A4A; font-size: 11px;')
        ver_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(ver_lbl)

        root.addWidget(left)

        # ── RIGHT PANEL — workspace selector ──────────────────────────────
        right = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(32, 36, 32, 28)
        right_layout.setSpacing(12)

        # Heading
        heading = QtWidgets.QLabel('Open Workspace')
        heading.setStyleSheet('font-size: 17px; font-weight: 700;')
        right_layout.addWidget(heading)

        sub = QtWidgets.QLabel('Select a folder to start or continue working.')
        sub.setStyleSheet('font-size: 12px; color: palette(mid);')
        right_layout.addWidget(sub)

        right_layout.addSpacing(4)

        # Recent label + clear button row
        lbl_row = QtWidgets.QHBoxLayout()
        lbl_recent = QtWidgets.QLabel('Recent Workspaces')
        lbl_recent.setStyleSheet('font-size: 12px; font-weight: 600;')
        lbl_row.addWidget(lbl_recent)
        lbl_row.addStretch()

        self._btn_clear = QtWidgets.QToolButton()
        self._btn_clear.setText('Clear all')
        self._btn_clear.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._btn_clear.setStyleSheet('font-size: 11px;')
        self._btn_clear.clicked.connect(self._clear_recent)
        lbl_row.addWidget(self._btn_clear)
        right_layout.addLayout(lbl_row)

        # Recent workspaces list
        self._list = QtWidgets.QListWidget()
        self._list.setAlternatingRowColors(True)
        self._list.setSpacing(1)
        self._list.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self._list.customContextMenuRequested.connect(self._list_context_menu)
        self._list.itemDoubleClicked.connect(self._open_recent)
        self._list.setToolTip(
            'Double-click to open  •  Right-click to remove from list'
        )
        right_layout.addWidget(self._list)

        hint = QtWidgets.QLabel(
            'Double-click to open  •  Right-click to remove a single entry'
        )
        hint.setStyleSheet('font-size: 10px; color: palette(mid);')
        right_layout.addWidget(hint)

        right_layout.addSpacing(8)

        # Action buttons
        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        right_layout.addWidget(sep)

        right_layout.addSpacing(4)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(8)

        btn_open = QtWidgets.QPushButton(' Open Workspace…')
        btn_open.setIcon(QtGui.QIcon('icons:folder.svg'))
        btn_open.setDefault(True)
        btn_open.setFixedHeight(36)
        btn_open.clicked.connect(self._browse)

        btn_skip = QtWidgets.QPushButton('Continue without Workspace')
        btn_skip.setFixedHeight(36)
        btn_skip.clicked.connect(self._skip)

        btn_row.addWidget(btn_open)
        btn_row.addStretch()
        btn_row.addWidget(btn_skip)
        right_layout.addLayout(btn_row)

        root.addWidget(right, stretch=1)

    # ── Recent workspaces ─────────────────────────────────────────────────

    def _load_recent(self):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        recent = settings.value('recent_workspaces', [])
        if isinstance(recent, str):
            recent = [recent] if recent else []
        self._list.clear()
        for path in recent:
            item = QtWidgets.QListWidgetItem()
            item.setText(path)
            item.setToolTip(path)
            if not os.path.isdir(path):
                item.setForeground(QtGui.QColor(180, 80, 80))
                item.setToolTip(f'{path}  [not found]')
            self._list.addItem(item)
        self._btn_clear.setVisible(self._list.count() > 0)

    @staticmethod
    def add_to_recent(path: str):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        recent = settings.value('recent_workspaces', [])
        if isinstance(recent, str):
            recent = [recent] if recent else []
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        settings.setValue('recent_workspaces', recent[:10])

    @staticmethod
    def _save_recent_list(paths: list):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        settings.setValue('recent_workspaces', paths)

    # ── Slots ─────────────────────────────────────────────────────────────

    def _open_recent(self, item):
        path = item.text()
        if os.path.isdir(path):
            self._accept_path(path)
        else:
            btn = QtWidgets.QMessageBox.warning(
                self,
                'Folder Not Found',
                f'The following folder could not be found:\n{path}\n\n'
                'Remove it from recent workspaces?',
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No,
            )
            if btn == QtWidgets.QMessageBox.StandardButton.Yes:
                self._remove_path_from_recent(path)
                self._load_recent()

    def _list_context_menu(self, pos):
        item = self._list.itemAt(pos)
        if item is None:
            return
        menu = QtWidgets.QMenu(self)
        act_open = menu.addAction('Open')
        act_remove = menu.addAction('Remove from list')
        chosen = menu.exec(self._list.mapToGlobal(pos))
        if chosen == act_open:
            self._open_recent(item)
        elif chosen == act_remove:
            self._remove_path_from_recent(item.text())
            self._load_recent()

    def _clear_recent(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            'Clear Recent Workspaces',
            'Remove all entries from the recent workspaces list?',
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.Cancel,
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self._save_recent_list([])
            self._load_recent()

    def _browse(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Workspace Folder', ''
        )
        if path:
            self._accept_path(path)

    def _skip(self):
        self._selected_path = None
        self.accept()

    def _accept_path(self, path):
        self._selected_path = path
        self.add_to_recent(path)
        self.accept()

    @staticmethod
    def _remove_path_from_recent(path: str):
        settings = QtCore.QSettings('DotTargetCounter', 'DotTargetCounter')
        recent = settings.value('recent_workspaces', [])
        if isinstance(recent, str):
            recent = [recent] if recent else []
        if path in recent:
            recent.remove(path)
        settings.setValue('recent_workspaces', recent)

    # ── closeEvent — X button quits the app ───────────────────────────────

    def closeEvent(self, event):
        self.reject()
        event.accept()

    # ── Public property ───────────────────────────────────────────────────

    @property
    def selected_path(self):
        """The chosen workspace path, or None if the user chose to skip."""
        return self._selected_path
