# -*- coding: utf-8 -*-
#
# Countmon — Biophilic Base Theme
#
# A single palette-adaptive QSS applied to every theme.
# Colors are expressed via palette() references so each QPalette
# (dark, navy, nature, light/biophilic-light …) keeps its own hues
# while gaining the modern organic shape: rounded corners, generous
# padding, slim scrollbars, and refined widget geometry.

BIOPHILIC_BASE_QSS = """

/* ── Global (base: labels, inputs, tree/table content) ───────────────── */
QWidget {
    font-family: "Inter", "Segoe UI", "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    font-size: 12pt;
}

/* ── MenuBar ─────────────────────────────────────────────────────────── */
QMenuBar {
    background-color: palette(window);
    color: palette(window-text);
    border-bottom: 1px solid palette(mid);
    padding: 1px 4px;
    spacing: 2px;
    font-size: 13pt;
}
QMenuBar::item {
    background: transparent;
    color: palette(window-text);
    padding: 4px 10px;
    border-radius: 5px;
}
QMenuBar::item:selected {
    background-color: palette(highlight);
    color: palette(highlighted-text);
}
QMenuBar::item:pressed {
    background-color: palette(highlight);
    color: palette(highlighted-text);
}

/* ── Menu (dropdown) ─────────────────────────────────────────────────── */
QMenu {
    background-color: palette(base);
    color: palette(window-text);
    border: 1px solid palette(mid);
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 5px 24px 5px 12px;
    border-radius: 5px;
    background: transparent;
    color: palette(window-text);
}
QMenu::item:selected {
    background-color: palette(highlight);
    color: palette(highlighted-text);
}
QMenu::separator {
    height: 1px;
    background: palette(mid);
    margin: 4px 8px;
}

/* ── QPushButton ─────────────────────────────────────────────────────── */
QPushButton {
    background-color: palette(button);
    color: palette(button-text);
    border: 1px solid palette(mid);
    border-radius: 8px;
    padding: 5px 16px;
    min-height: 26px;
    font-size: 13pt;
    font-weight: 600;
}
QPushButton:hover {
    border-color: palette(highlight);
}
QPushButton:pressed {
    background-color: palette(dark);
    color: palette(button-text);
}
QPushButton:checked {
    background-color: palette(highlight);
    color: palette(highlighted-text);
    border-color: palette(highlight);
}
QPushButton:disabled {
    color: palette(mid);
    border-color: palette(mid);
}

/* ── QToolButton ─────────────────────────────────────────────────────── */
QToolButton {
    background: transparent;
    border: none;
    border-radius: 5px;
    padding: 2px;
}
QToolButton:hover {
    background-color: palette(button);
    border: 1px solid palette(mid);
}
QToolButton:pressed {
    background-color: palette(dark);
}

/* ── QGroupBox ───────────────────────────────────────────────────────── */
QGroupBox {
    background-color: palette(base);
    border: 1px solid palette(mid);
    border-radius: 10px;
    margin-top: 22px;
    padding: 12px 8px 8px 8px;
    font-size: 15pt;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: 2px;
    padding: 0 6px;
    color: palette(highlight);
    font-size: 15pt;
    font-weight: bold;
    background-color: palette(base);
}

/* ── QLineEdit ───────────────────────────────────────────────────────── */
QLineEdit {
    background-color: palette(base);
    color: palette(text);
    border: 1px solid palette(mid);
    border-radius: 6px;
    padding: 4px 8px;
    selection-background-color: palette(highlight);
    selection-color: palette(highlighted-text);
}
QLineEdit:focus {
    border-color: palette(highlight);
}
QLineEdit:disabled {
    color: palette(mid);
    border-color: palette(mid);
}

/* ── QTextEdit / QPlainTextEdit ──────────────────────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: palette(base);
    color: palette(text);
    border: 1px solid palette(mid);
    border-radius: 8px;
    padding: 6px 8px;
    selection-background-color: palette(highlight);
    selection-color: palette(highlighted-text);
}
QTextEdit:focus, QPlainTextEdit:focus {
    border-color: palette(highlight);
}

/* ── QComboBox ───────────────────────────────────────────────────────── */
QComboBox {
    background-color: palette(button);
    color: palette(button-text);
    border: 1px solid palette(mid);
    border-radius: 6px;
    padding: 4px 8px;
    min-height: 22px;
}
QComboBox:hover {
    border-color: palette(highlight);
}
QComboBox:focus {
    border-color: palette(highlight);
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: palette(base);
    border: 1px solid palette(mid);
    border-radius: 6px;
    selection-background-color: palette(highlight);
    selection-color: palette(highlighted-text);
    color: palette(text);
    outline: none;
}

/* ── QTableWidget / QTableView ───────────────────────────────────────── */
QTableWidget, QTableView {
    background-color: palette(base);
    alternate-background-color: palette(alternate-base);
    gridline-color: palette(mid);
    border: 1px solid palette(mid);
    border-radius: 8px;
    selection-background-color: palette(highlight);
    selection-color: palette(highlighted-text);
    outline: none;
}
QTableWidget::item, QTableView::item {
    padding: 3px 6px;
    border: none;
}
QTableWidget::item:selected, QTableView::item:selected {
    background-color: palette(highlight);
    color: palette(highlighted-text);
}

/* ── QHeaderView ─────────────────────────────────────────────────────── */
QHeaderView {
    background-color: transparent;
    border: none;
}
QHeaderView::section {
    background-color: palette(alternate-base);
    color: palette(window-text);
    border: none;
    border-bottom: 1px solid palette(mid);
    border-right: 1px solid palette(mid);
    padding: 5px 8px;
    font-size: 15pt;
    font-weight: bold;
}
QHeaderView::section:last {
    border-right: none;
}

/* ── QTreeView ───────────────────────────────────────────────────────── */
QTreeView {
    background-color: palette(base);
    alternate-background-color: palette(alternate-base);
    border: 1px solid palette(mid);
    border-radius: 8px;
    selection-background-color: palette(highlight);
    selection-color: palette(highlighted-text);
    outline: none;
}
QTreeView::item {
    padding: 3px 4px;
    border-radius: 4px;
}
QTreeView::item:selected {
    background-color: palette(highlight);
    color: palette(highlighted-text);
}
QTreeView::item:hover:!selected {
    background-color: palette(button);
}

/* ── QScrollBar (vertical) ───────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 2px 2px 2px 0;
}
QScrollBar::handle:vertical {
    background: palette(mid);
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: palette(dark);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
    height: 0;
    border: none;
}

/* ── QScrollBar (horizontal) ─────────────────────────────────────────── */
QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 0 2px 2px 2px;
}
QScrollBar::handle:horizontal {
    background: palette(mid);
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background: palette(dark);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
    width: 0;
    border: none;
}

/* ── QSlider ─────────────────────────────────────────────────────────── */
QSlider::groove:horizontal {
    height: 5px;
    background: palette(mid);
    border-radius: 3px;
    margin: 0 4px;
}
QSlider::handle:horizontal {
    background: palette(highlight);
    border: 2px solid palette(dark);
    width: 14px;
    height: 14px;
    border-radius: 7px;
    margin: -5px 0;
}
QSlider::handle:horizontal:hover {
    border-color: palette(highlight);
}
QSlider::sub-page:horizontal {
    background: palette(highlight);
    border-radius: 3px;
    opacity: 0.6;
}

/* ── QCheckBox ───────────────────────────────────────────────────────── */
QCheckBox {
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid palette(mid);
    border-radius: 4px;
    background: palette(base);
}
QCheckBox::indicator:hover {
    border-color: palette(highlight);
}
QCheckBox::indicator:checked {
    background-color: palette(highlight);
    border-color: palette(highlight);
}
QCheckBox::indicator:disabled {
    background: palette(alternate-base);
    border-color: palette(mid);
}

/* ── QRadioButton ────────────────────────────────────────────────────── */
QRadioButton {
    spacing: 6px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid palette(mid);
    border-radius: 8px;
    background: palette(base);
}
QRadioButton::indicator:hover {
    border-color: palette(highlight);
}
QRadioButton::indicator:checked {
    background-color: palette(highlight);
    border-color: palette(highlight);
}

/* ── QSpinBox ────────────────────────────────────────────────────────── */
QSpinBox, QDoubleSpinBox {
    background-color: palette(base);
    color: palette(text);
    border: 1px solid palette(mid);
    border-radius: 6px;
    padding: 3px 6px;
}
QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: palette(highlight);
}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background: palette(button);
    border: none;
    border-radius: 3px;
    width: 16px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background: palette(dark);
}

/* ── QFrame (separators) ─────────────────────────────────────────────── */
QFrame[frameShape="4"],
QFrame[frameShape="5"] {
    color: palette(mid);
}

/* ── QLabel ──────────────────────────────────────────────────────────── */
QLabel {
    background: transparent;
}

/* ── QToolTip ────────────────────────────────────────────────────────── */
QToolTip {
    background-color: palette(tooltip-base);
    color: palette(tooltip-text);
    border: 1px solid palette(highlight);
    border-radius: 5px;
    padding: 4px 8px;
    font-size: 11pt;
}

/* ── QTabWidget / QTabBar ────────────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid palette(mid);
    border-radius: 8px;
    background: palette(base);
}
QTabBar::tab {
    background: palette(button);
    border: 1px solid palette(mid);
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 6px 16px;
    margin-right: 2px;
    color: palette(window-text);
    font-size: 15pt;
}
QTabBar::tab:selected {
    background: palette(base);
    font-weight: bold;
}
QTabBar::tab:hover:!selected {
    border-color: palette(highlight);
}

/* ── QStatusBar ──────────────────────────────────────────────────────── */
QStatusBar {
    background-color: palette(window);
    border-top: 1px solid palette(mid);
}

/* ── QDialog / QMessageBox / QInputDialog ────────────────────────────── */
QDialog, QMessageBox, QInputDialog {
    background-color: palette(window);
}

"""
