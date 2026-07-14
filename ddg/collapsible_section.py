# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtWidgets


class CollapsibleSection(QtWidgets.QWidget):
    """Accordion-style section with a clickable header and arrow toggle."""

    toggled = QtCore.pyqtSignal(bool)

    def __init__(self, title, content_widget, parent=None, collapsed=False):
        super().__init__(parent)
        self._content = content_widget
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self._toggle = QtWidgets.QToolButton()
        self._toggle.setText(title)
        self._toggle.setCheckable(True)
        self._toggle.setChecked(not collapsed)
        self._toggle.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        self._toggle.setArrowType(
            QtCore.Qt.ArrowType.RightArrow
            if collapsed
            else QtCore.Qt.ArrowType.DownArrow
        )
        self._toggle.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self._toggle.setStyleSheet(
            "QToolButton {"
            "  border: 1px solid palette(mid);"
            "  border-radius: 8px;"
            "  padding: 6px 10px;"
            "  font-weight: 600;"
            "  text-align: left;"
            "}"
            "QToolButton:hover { border-color: palette(highlight); }"
            "QToolButton:checked { color: palette(highlight); }"
        )
        self._toggle.clicked.connect(self._on_toggle)

        layout.addWidget(self._toggle)
        layout.addWidget(self._content)
        self._content.setVisible(not collapsed)

    def _on_toggle(self, expanded):
        self._content.setVisible(expanded)
        self._toggle.setArrowType(
            QtCore.Qt.ArrowType.DownArrow
            if expanded
            else QtCore.Qt.ArrowType.RightArrow
        )
        self.updateGeometry()
        self.toggled.emit(expanded)
