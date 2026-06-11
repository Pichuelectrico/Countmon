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
from PyQt6 import QtCore, QtGui, QtWidgets, uic

from .chip_dialog import ChipDialog

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(__file__)
WIDGET, _ = uic.loadUiType(os.path.join(bundle_dir, 'point_widget.ui'))

# Column indices
COL_NUM   = 0   # # shortcut number (read-only)
COL_NAME  = 1   # class name (editable)
COL_COLOR = 2   # color swatch (click to change)
COL_MOVE  = 3   # ↑↓ buttons widget


class PointWidget(QtWidgets.QWidget, WIDGET):
    hide_custom_fields = QtCore.pyqtSignal(bool)

    def __init__(self, canvas, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.canvas = canvas

        self.pushButtonAddClass.clicked.connect(self.add_class)
        self.pushButtonRemoveClass.clicked.connect(self.remove_class)
        self.pushButtonImport.clicked.connect(self.import_metadata)
        self.pushButtonSave.clicked.connect(self.canvas.save)
        self.pushButtonLoadPoints.clicked.connect(self.load)
        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonExport.clicked.connect(self.export)

        self.pushButtonExport.setIcon(QtGui.QIcon('icons:export.svg'))
        self.pushButtonReset.setIcon(QtGui.QIcon('icons:reset.svg'))
        self.pushButtonReset.setStyleSheet('text-align: left;')
        self.pushButtonImport.setIcon(QtGui.QIcon('icons:import.svg'))
        self.pushButtonImport.setStyleSheet('text-align: left;')
        self.pushButtonSave.setIcon(QtGui.QIcon('icons:save.svg'))
        self.pushButtonSave.setStyleSheet('text-align: left;')
        self.pushButtonLoadPoints.setIcon(QtGui.QIcon('icons:load.svg'))
        self.pushButtonLoadPoints.setStyleSheet('text-align: left;')
        self.pushButtonRemoveClass.setIcon(QtGui.QIcon('icons:delete.svg'))
        self.pushButtonAddClass.setIcon(QtGui.QIcon('icons:add.svg'))

        # ── Replace QTableWidget from .ui with a fresh 4-column table ───────
        old_table = self.tableWidgetClasses
        parent_layout = self.groupBoxClasses.layout()
        parent_layout.removeWidget(old_table)
        old_table.hide()
        old_table.setParent(None)

        self.tableWidgetClasses = QtWidgets.QTableWidget(self.groupBoxClasses)
        parent_layout.insertWidget(0, self.tableWidgetClasses)

        # Column setup
        self.tableWidgetClasses.setColumnCount(4)
        self.tableWidgetClasses.setHorizontalHeaderLabels(['#', 'Class', '', ''])
        hh = self.tableWidgetClasses.horizontalHeader()
        hh.setMinimumSectionSize(1)
        hh.setStretchLastSection(False)
        hh.setSectionResizeMode(COL_NAME, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidgetClasses.setColumnWidth(COL_NUM,   28)
        self.tableWidgetClasses.setColumnWidth(COL_COLOR, 44)
        self.tableWidgetClasses.setColumnWidth(COL_MOVE,  48)
        vh = self.tableWidgetClasses.verticalHeader()
        vh.setVisible(False)
        vh.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidgetClasses.setWordWrap(True)
        self.tableWidgetClasses.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidgetClasses.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.tableWidgetClasses.cellClicked.connect(self.cell_clicked)
        self.tableWidgetClasses.cellChanged.connect(self.cell_changed)
        self.tableWidgetClasses.selectionModel().selectionChanged.connect(
            self.selection_changed)

        # ── Rest of widget setup ───────────────────────────────────────────
        self.checkBoxDisplayPoints.toggled.connect(self.display_points)
        self.checkBoxDisplayGrid.toggled.connect(self.display_grid)
        self.canvas.image_loading.connect(self.set_sliders)
        self.canvas.image_loaded.connect(self.image_loaded)
        self.canvas.update_point_count.connect(self.update_point_count)
        self.canvas.points_loaded.connect(self.points_loaded)
        self.canvas.metadata_imported.connect(self.display_count_tree)

        self.model = QtGui.QStandardItemModel()
        self.current_model_index = QtCore.QModelIndex()
        self.treeView.setModel(self.model)
        self.reset_model()
        self.treeView.doubleClicked.connect(self.select_model_item)

        self.spinBoxPointRadius.valueChanged.connect(self.canvas.set_point_radius)
        self.spinBoxGrid.valueChanged.connect(self.canvas.set_grid_size)

        icon = QtGui.QPixmap(20, 20)
        icon.fill(QtCore.Qt.GlobalColor.yellow)
        self.labelPointColor.setPixmap(icon)
        self.labelPointColor.mousePressEvent = self.change_active_point_color
        icon = QtGui.QPixmap(20, 20)
        icon.fill(QtCore.Qt.GlobalColor.white)
        self.labelGridColor.setPixmap(icon)
        self.labelGridColor.mousePressEvent = self.change_grid_color

        self.checkBoxImageFields.clicked.connect(self.hide_custom_fields.emit)
        self.checkBoxImageFields.hide()
        self.horizontalSliderBrightness.valueChanged.connect(self.set_brightness)
        self.horizontalSliderContrast.valueChanged.connect(self.set_contrast)

    # ── Class list ─────────────────────────────────────────────────────────

    def add_class(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle(self.tr('New Class'))
        dlg.setMinimumWidth(300)
        layout = QtWidgets.QVBoxLayout(dlg)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(QtWidgets.QLabel(self.tr('Class Name')))
        line_edit = QtWidgets.QLineEdit(dlg)
        layout.addWidget(line_edit)
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(8)
        btn_cancel = QtWidgets.QPushButton(self.tr('Cancel'))
        btn_ok = QtWidgets.QPushButton(self.tr('Add'))
        btn_ok.setDefault(True)
        btn_cancel.clicked.connect(dlg.reject)
        btn_ok.clicked.connect(dlg.accept)
        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        layout.addLayout(btn_row)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            class_name = line_edit.text().strip()
            if class_name:
                self.canvas.add_class(class_name)
                self.display_classes()
                self.display_count_tree()

    def remove_class(self):
        indexes = self.tableWidgetClasses.selectedIndexes()
        if len(indexes) > 0:
            class_name = self.canvas.classes[indexes[0].row()]
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle(self.tr('Warning'))
            msgBox.setText(self.tr('{} [{}] '.format(
                self.tr('You are about to remove class'), class_name)))
            msgBox.setInformativeText(self.tr('Do you want to continue?'))
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Cancel |
                QtWidgets.QMessageBox.StandardButton.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            if msgBox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                self.canvas.remove_class(class_name)
                self.display_classes()
                self.display_count_tree()

    def _move_class(self, row, direction):
        """Move the class at `row` up (direction=-1) or down (direction=+1)."""
        new_row = row + direction
        if new_row < 0 or new_row >= len(self.canvas.classes):
            return
        classes = self.canvas.classes
        classes.insert(new_row, classes.pop(row))
        self.canvas.dirty = True
        self.display_classes()
        self.display_count_tree()
        self.tableWidgetClasses.selectRow(new_row)

    def _make_move_widget(self, row):
        """Return a small widget with ↑ and ↓ QToolButtons for reordering."""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        layout.setSpacing(1)

        btn_style = (
            "QToolButton { border: none; font-size: 9px; }"
            "QToolButton:hover { background: rgba(128,128,128,80); border-radius: 2px; }"
        )

        btn_up = QtWidgets.QToolButton()
        btn_up.setArrowType(QtCore.Qt.ArrowType.UpArrow)
        btn_up.setFixedSize(20, 18)
        btn_up.setStyleSheet(btn_style)
        btn_up.setToolTip(self.tr('Move class up'))
        btn_up.clicked.connect(lambda checked=False, r=row: self._move_class(r, -1))

        btn_down = QtWidgets.QToolButton()
        btn_down.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        btn_down.setFixedSize(20, 18)
        btn_down.setStyleSheet(btn_style)
        btn_down.setToolTip(self.tr('Move class down'))
        btn_down.clicked.connect(lambda checked=False, r=row: self._move_class(r, 1))

        layout.addWidget(btn_up)
        layout.addWidget(btn_down)
        return widget

    def display_classes(self):
        self.tableWidgetClasses.blockSignals(True)
        self.tableWidgetClasses.setRowCount(len(self.canvas.classes))
        for row, class_name in enumerate(self.canvas.classes):
            # Col 0 — shortcut number: 1-9 for rows 0-8, 0 for row 9, blank after
            if row < 9:
                shortcut = str(row + 1)
            elif row == 9:
                shortcut = '0'
            else:
                shortcut = ''
            num_item = QtWidgets.QTableWidgetItem(shortcut)
            num_item.setFlags(
                num_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            num_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetClasses.setItem(row, COL_NUM, num_item)

            # Col 1 — class name (editable)
            self.tableWidgetClasses.setItem(row, COL_NAME,
                                            QtWidgets.QTableWidgetItem(class_name))

            # Col 2 — color swatch (click-to-change, non-editable)
            color_item = QtWidgets.QTableWidgetItem()
            px = QtGui.QPixmap(18, 18)
            px.fill(self.canvas.colors[class_name])
            color_item.setData(QtCore.Qt.ItemDataRole.DecorationRole, px)
            color_item.setFlags(
                color_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.tableWidgetClasses.setItem(row, COL_COLOR, color_item)

            # Col 3 — ↑↓ move widget
            self.tableWidgetClasses.setCellWidget(
                row, COL_MOVE, self._make_move_widget(row))

        self.tableWidgetClasses.selectionModel().clear()
        self.tableWidgetClasses.blockSignals(False)

    # ── Cell events ────────────────────────────────────────────────────────

    def cell_changed(self, row, column):
        if column == COL_NAME:
            item = self.tableWidgetClasses.item(row, COL_NAME)
            if item is None or row >= len(self.canvas.classes):
                return
            new_class = item.text()
            old_class = self.canvas.classes[row]
            if old_class != new_class:
                self.tableWidgetClasses.selectionModel().clear()
                self.canvas.rename_class(old_class, new_class)
                self.display_classes()
                self.display_count_tree()

    def cell_clicked(self, row, column):
        if column == COL_COLOR:
            color = QtWidgets.QColorDialog.getColor()
            if color.isValid():
                self.canvas.colors[self.canvas.classes[row]] = color
                self.canvas.dirty = True
                color_item = QtWidgets.QTableWidgetItem()
                px = QtGui.QPixmap(18, 18)
                px.fill(color)
                color_item.setData(QtCore.Qt.ItemDataRole.DecorationRole, px)
                color_item.setFlags(
                    color_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.tableWidgetClasses.setItem(row, COL_COLOR, color_item)

    def change_active_point_color(self, event):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.set_active_point_color(color)

    def change_grid_color(self, event):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.set_grid_color(color)

    # ── Display ────────────────────────────────────────────────────────────

    def display_grid(self, display):
        self.canvas.toggle_grid(display=display)

    def display_points(self, display):
        self.canvas.toggle_points(display=display)

    def display_count_tree(self):
        self.reset_model()
        for image in sorted(self.canvas.points):
            image_item = QtGui.QStandardItem(image)
            image_item.setEditable(False)
            class_item = QtGui.QStandardItem('')
            class_item.setEditable(False)
            self.model.appendRow([image_item, class_item])
            file_name = os.path.join(self.canvas.directory, image)
            if not os.path.exists(file_name):
                font = image_item.font()
                font.setStrikeOut(True)
                image_item.setFont(font)
                image_item.setForeground(
                    QtGui.QBrush(QtCore.Qt.GlobalColor.red))
            if image == self.canvas.current_image_name:
                font = image_item.font()
                font.setBold(True)
                image_item.setFont(font)
                self.treeView.setExpanded(image_item.index(), True)
                self.current_model_index = image_item.index()

            for class_name in self.canvas.classes:
                class_item = QtGui.QStandardItem(class_name)
                class_item.setEditable(False)
                class_item.setSelectable(False)
                count = '0'
                if class_name in self.canvas.points[image]:
                    count = str(len(self.canvas.points[image][class_name]))
                count_item = QtGui.QStandardItem(count)
                count_item.setEditable(False)
                count_item.setSelectable(False)
                image_item.appendRow([class_item, count_item])
        self.treeView.scrollTo(self.current_model_index)

    # ── File operations ────────────────────────────────────────────────────

    def export(self):
        if self.radioButtonCounts.isChecked():
            fn = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr('Export Count Summary'),
                os.path.join(self.canvas.directory, 'counts.csv'),
                'Text CSV (*.csv)')
            if fn[0]:
                self.canvas.export_counts(fn[0])
        elif self.radioButtonPoints.isChecked():
            fn = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr('Export Points'),
                os.path.join(self.canvas.directory, 'points.csv'),
                'Text CSV (*.csv)')
            if fn[0]:
                self.canvas.export_points(fn[0])
        elif self.radioButtonOverlay.isChecked():
            fn = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr('Export Image With Points'),
                os.path.join(self.canvas.directory, 'overlay.png'),
                'PNG (*.png);;JPG (*.jpg)')
            if fn[0]:
                self.canvas.export_overlay(fn[0])
        else:
            self.chip_dialog = ChipDialog(
                self.canvas.classes, self.canvas.points,
                self.canvas.directory, self.canvas.survey_id)
            self.chip_dialog.show()

    def image_loaded(self, directory, file_name):
        self.display_count_tree()

    def import_metadata(self):
        if self.canvas.dirty_data_check():
            fn = QtWidgets.QFileDialog.getOpenFileName(
                self, self.tr('Select Points File'),
                self.canvas.directory, 'Point Files (*.pnt)')
            if fn[0]:
                self.canvas.import_metadata(fn[0])

    def load(self):
        if self.canvas.dirty_data_check():
            fn = QtWidgets.QFileDialog.getOpenFileName(
                self, self.tr('Select Points File'),
                self.canvas.directory, 'Point Files (*.pnt)')
            if fn[0]:
                self.canvas.load_points(fn[0])

    # ── Navigation ─────────────────────────────────────────────────────────

    def next(self):
        max_index = self.model.rowCount()
        next_index = self.current_model_index.row() + 1
        if next_index < max_index:
            self.select_model_item(self.model.item(next_index).index())

    def previous(self):
        prev_index = self.current_model_index.row() - 1
        if prev_index >= 0:
            self.select_model_item(self.model.item(prev_index).index())

    def reset(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle(self.tr('Warning'))
        msgBox.setText(self.tr('You are about to clear all data'))
        msgBox.setInformativeText(self.tr('Do you want to continue?'))
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Cancel |
            QtWidgets.QMessageBox.StandardButton.Ok)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
        if msgBox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
            self.canvas.reset()
            self.display_classes()
            self.display_count_tree()

    def reset_model(self):
        self.current_model_index = QtCore.QModelIndex()
        self.model.clear()
        self.model.setColumnCount(2)
        self.model.setHeaderData(0, QtCore.Qt.Orientation.Horizontal,
                                 self.tr('Image'))
        self.model.setHeaderData(1, QtCore.Qt.Orientation.Horizontal,
                                 self.tr('Count'))
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.header().setStretchLastSection(False)
        self.treeView.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.treeView.setTextElideMode(QtCore.Qt.TextElideMode.ElideMiddle)

    def select_model_item(self, model_index):
        item = self.model.itemFromIndex(model_index)
        if item.isSelectable():
            if item.column() != 0:
                item = self.model.itemFromIndex(
                    self.model.index(item.row(), 0))
            self.canvas.load_image(
                os.path.join(self.canvas.directory, item.text()))

    def selection_changed(self, selected, deselected):
        if len(selected.indexes()) > 0:
            self.canvas.set_current_class(selected.indexes()[0].row())
        else:
            self.canvas.set_current_class(None)

    # ── Active class ───────────────────────────────────────────────────────

    def set_active_class(self, row):
        if row < self.tableWidgetClasses.rowCount():
            self.tableWidgetClasses.selectRow(row)

    def points_loaded(self):
        self.display_classes()
        self.update_ui_settings()

    # ── Display settings ───────────────────────────────────────────────────

    def set_active_point_color(self, color):
        icon = QtGui.QPixmap(20, 20)
        icon.fill(color)
        self.labelPointColor.setPixmap(icon)
        self.canvas.set_point_color(color)

    def set_brightness(self, value):
        self.canvas.generate_lookup_table(
            value, self.horizontalSliderContrast.value())
        self.canvas.redraw_image()

    def set_contrast(self, value):
        self.canvas.generate_lookup_table(
            self.horizontalSliderBrightness.value(), value)
        self.canvas.redraw_image()

    def set_grid_color(self, color):
        icon = QtGui.QPixmap(20, 20)
        icon.fill(color)
        self.labelGridColor.setPixmap(icon)
        self.canvas.set_grid_color(color)

    def set_sliders(self, large_image, redraw):
        self.horizontalSliderBrightness.setTracking(not large_image)
        self.horizontalSliderContrast.setTracking(not large_image)
        if not redraw:
            self.horizontalSliderBrightness.blockSignals(True)
            self.horizontalSliderContrast.blockSignals(True)
            self.horizontalSliderBrightness.setValue(0)
            self.horizontalSliderContrast.setValue(0)
            self.horizontalSliderBrightness.blockSignals(False)
            self.horizontalSliderContrast.blockSignals(False)

    def update_point_count(self, image_name, class_name, class_count):
        items = self.model.findItems(image_name)
        if len(items) == 0:
            self.display_count_tree()
        else:
            items[0].child(
                self.canvas.classes.index(class_name), 1
            ).setText(str(class_count))

    def update_ui_settings(self):
        ui = self.canvas.ui
        color = QtGui.QColor(
            ui['point']['color'][0],
            ui['point']['color'][1],
            ui['point']['color'][2])
        self.set_active_point_color(color)
        self.spinBoxPointRadius.setValue(ui['point']['radius'])
        color = QtGui.QColor(
            ui['grid']['color'][0],
            ui['grid']['color'][1],
            ui['grid']['color'][2])
        self.set_grid_color(color)
        self.spinBoxGrid.setValue(ui['grid']['size'])
