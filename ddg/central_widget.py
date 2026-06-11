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
import os
import sys
from PyQt6 import QtCore, QtWidgets, QtGui, uic

from ddg import Canvas
from ddg import PointWidget
from ddg.fields import BoxText, LineText

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(__file__)
CLASS_DIALOG, _ = uic.loadUiType(os.path.join(bundle_dir, 'central_widget.ui'))


class CentralWidget(QtWidgets.QDialog, CLASS_DIALOG):

    load_custom_data = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.canvas = Canvas(self)

        self.point_widget = PointWidget(self.canvas, self)
        self.findChild(QtWidgets.QFrame, 'framePointWidget').layout().addWidget(self.point_widget)
        self.point_widget.hide_custom_fields.connect(self.hide_custom_fields)
        self.canvas.saving.connect(self.display_quick_save)

        # ── Keyboard shortcuts ──────────────────────────────────────────────

        # Quick save
        self._shortcut(QtCore.Qt.Key.Key_S, self.canvas.quick_save,
                       modifier=QtCore.Qt.KeyboardModifier.ControlModifier)
        # Undo / Redo
        self._shortcut(QtCore.Qt.Key.Key_Z, self.canvas.undo,
                       modifier=QtCore.Qt.KeyboardModifier.ControlModifier)
        self._shortcut(QtCore.Qt.Key.Key_Y, self.canvas.redo,
                       modifier=QtCore.Qt.KeyboardModifier.ControlModifier)

        # Arrow keys — navigate between images (WASD now pan the canvas)
        self._shortcut(QtCore.Qt.Key.Key_Up, self.point_widget.previous)
        self._shortcut(QtCore.Qt.Key.Key_Down, self.point_widget.next)

        # Left / Right arrows — toggle side panels
        self._shortcut(QtCore.Qt.Key.Key_Left,  self._shortcut_toggle_left)
        self._shortcut(QtCore.Qt.Key.Key_Right, self._shortcut_toggle_right)

        # T — new class dialog
        self._shortcut(QtCore.Qt.Key.Key_T, self.point_widget.add_class)

        # I / O — counter / reviewer mode
        self._shortcut(QtCore.Qt.Key.Key_I,
                       lambda: self.graphicsView.set_mode('counter'))
        self._shortcut(QtCore.Qt.Key.Key_O,
                       lambda: self.graphicsView.set_mode('reviewer'))

        # H — toggle point display (D is now used for panning right)
        self._shortcut(QtCore.Qt.Key.Key_H,
                       self.point_widget.checkBoxDisplayPoints.toggle)

        # ── Signal connections ──────────────────────────────────────────────
        self.graphicsView.setScene(self.canvas)
        self.graphicsView.drop_complete.connect(self.canvas.load)
        self.graphicsView.region_selected.connect(self.canvas.select_points)
        self.graphicsView.delete_selection.connect(self.canvas.delete_selected_points)
        self.graphicsView.relabel_selection.connect(self.canvas.relabel_selected_points)
        self.graphicsView.toggle_points.connect(self.point_widget.checkBoxDisplayPoints.toggle)
        self.graphicsView.toggle_grid.connect(self.point_widget.checkBoxDisplayGrid.toggle)
        self.graphicsView.switch_class.connect(self.point_widget.set_active_class)
        self.graphicsView.add_point.connect(self.canvas.add_point)
        self.graphicsView.mode_changed.connect(self._update_mode_badge)
        self.canvas.image_loaded.connect(self.graphicsView.image_loaded)
        self.canvas.directory_set.connect(self.display_working_directory)

        # Image data fields
        self.canvas.image_loaded.connect(self.display_coordinates)
        self.canvas.image_loaded.connect(self.get_custom_field_data)
        self.canvas.fields_updated.connect(self.display_custom_fields)
        self.lineEditX.textEdited.connect(self.update_coordinates)
        self.lineEditY.textEdited.connect(self.update_coordinates)

        # Buttons
        self.pushButtonAddField.clicked.connect(self.add_field_dialog)
        self.pushButtonDeleteField.clicked.connect(self.delete_field_dialog)
        self.pushButtonFolder.clicked.connect(self.select_folder)
        self.pushButtonZoomOut.clicked.connect(self.graphicsView.zoom_out)
        self.pushButtonZoomIn.clicked.connect(self.graphicsView.zoom_in)

        # Fix icons since no QRC file integration
        self.pushButtonFolder.setIcon(QtGui.QIcon('icons:folder.svg'))
        self.pushButtonZoomIn.setIcon(QtGui.QIcon('icons:zoom_in.svg'))
        self.pushButtonZoomOut.setIcon(QtGui.QIcon('icons:zoom_out.svg'))
        self.pushButtonDeleteField.setIcon(QtGui.QIcon('icons:delete.svg'))
        self.pushButtonAddField.setIcon(QtGui.QIcon('icons:add.svg'))

        # ── Quick-save overlay ─────────────────────────────────────────────
        self.quick_save_frame = QtWidgets.QFrame(self.graphicsView)
        self.quick_save_frame.setStyleSheet(
            "QFrame { background: #4caf50; color: #FFF; font-weight: bold }")
        self.quick_save_frame.setLayout(QtWidgets.QHBoxLayout())
        self.quick_save_frame.layout().addWidget(QtWidgets.QLabel(self.tr('Saving...')))
        self.quick_save_frame.setGeometry(3, 3, 100, 35)
        self.quick_save_frame.hide()

        # ── Mode badge overlay — both tags always visible ──────────────────
        self.mode_badge = QtWidgets.QFrame(self.graphicsView)
        self.mode_badge.setStyleSheet(
            "QFrame { background: rgba(30,30,30,200); border-radius: 5px; }")
        lay = QtWidgets.QHBoxLayout(self.mode_badge)
        lay.setContentsMargins(6, 3, 6, 3)
        lay.setSpacing(6)

        self._lbl_counter = QtWidgets.QLabel(self.tr('● Counter  [I]'))
        self._lbl_reviewer = QtWidgets.QLabel(self.tr('● Reviewer  [O]'))
        for lbl in (self._lbl_counter, self._lbl_reviewer):
            lbl.setStyleSheet("font-size: 11px; font-weight: bold;")
        lay.addWidget(self._lbl_counter)

        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        sep.setStyleSheet("color: rgba(180,180,180,100);")
        lay.addWidget(sep)

        lay.addWidget(self._lbl_reviewer)
        self.mode_badge.adjustSize()
        self.mode_badge.move(3, 42)
        self._update_mode_badge('reviewer')

        self.lineEditSurveyId.textChanged.connect(self.canvas.update_survey_id)
        self.canvas.points_loaded.connect(self.lineEditSurveyId.setText)

    # ── Helpers ────────────────────────────────────────────────────────────

    def _shortcut(self, key, slot, modifier=QtCore.Qt.KeyboardModifier.NoModifier):
        if modifier == QtCore.Qt.KeyboardModifier.NoModifier:
            sc = QtGui.QShortcut(QtGui.QKeySequence(key), self)
        else:
            sc = QtGui.QShortcut(QtGui.QKeySequence(modifier | key), self)
        sc.setContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc.activated.connect(slot)
        return sc

    def _update_mode_badge(self, mode):
        ACTIVE_COUNTER  = "font-size: 11px; font-weight: bold; color: #66bb6a;"   # green
        ACTIVE_REVIEWER = "font-size: 11px; font-weight: bold; color: #42a5f5;"   # blue
        INACTIVE        = "font-size: 11px; font-weight: bold; color: rgba(160,160,160,130);"

        if mode == 'counter':
            self._lbl_counter.setStyleSheet(ACTIVE_COUNTER)
            self._lbl_reviewer.setStyleSheet(INACTIVE)
        else:
            self._lbl_counter.setStyleSheet(INACTIVE)
            self._lbl_reviewer.setStyleSheet(ACTIVE_REVIEWER)
        self.mode_badge.adjustSize()

    # ── Panel visibility (called from MainWindow corner buttons) ───────────

    def toggle_left_panel(self, hide):
        frame = self.findChild(QtWidgets.QFrame, 'framePointWidget')
        if hide:
            frame.hide()
        else:
            frame.show()

    def toggle_right_panel(self, hide):
        if hide:
            self.frameCustomField.hide()
        else:
            self.frameCustomField.show()

    def _shortcut_toggle_left(self):
        """Called by ← shortcut — delegates to MainWindow button so its state stays in sync."""
        mw = self.parent()
        if mw is not None and hasattr(mw, '_btn_left_panel'):
            mw._btn_left_panel.toggle()
        else:
            frame = self.findChild(QtWidgets.QFrame, 'framePointWidget')
            self.toggle_left_panel(frame.isVisible())

    def _shortcut_toggle_right(self):
        """Called by → shortcut — delegates to MainWindow button so its state stays in sync."""
        mw = self.parent()
        if mw is not None and hasattr(mw, '_btn_right_panel'):
            mw._btn_right_panel.toggle()
        else:
            self.toggle_right_panel(self.frameCustomField.isVisible())

    # ── Resize ─────────────────────────────────────────────────────────────

    def resizeEvent(self, theEvent):
        self.graphicsView.resize_image()

    # ── Image data field functions ─────────────────────────────────────────

    def add_field(self):
        field_def = (self.field_name.text(), self.field_type.currentText())
        field_names = [x[0] for x in self.canvas.custom_fields['fields']]
        if field_def[0] in field_names:
            QtWidgets.QMessageBox.warning(self, self.tr('Warning'),
                                          self.tr('Field name already exists'))
        else:
            self.canvas.add_custom_field(field_def)
            self.add_dialog.close()

    def add_field_dialog(self):
        self.field_name = QtWidgets.QLineEdit()
        self.field_type = QtWidgets.QComboBox()
        self.field_type.addItems(['line', 'box'])
        self.add_button = QtWidgets.QPushButton(self.tr('Save'))
        self.add_button.clicked.connect(self.add_field)
        self.add_dialog = QtWidgets.QDialog(self)
        self.add_dialog.setWindowTitle(self.tr('Add Custom Field'))
        self.add_dialog.setLayout(QtWidgets.QVBoxLayout())
        self.add_dialog.layout().addWidget(self.field_name)
        self.add_dialog.layout().addWidget(self.field_type)
        self.add_dialog.layout().addWidget(self.add_button)
        self.add_dialog.resize(250, self.add_dialog.height())
        self.add_dialog.show()

    def delete_field(self):
        self.canvas.delete_custom_field(self.field_list.currentText())
        self.delete_dialog.close()

    def delete_field_dialog(self):
        self.field_list = QtWidgets.QComboBox()
        self.field_list.addItems([x[0] for x in self.canvas.custom_fields['fields']])
        self.delete_button = QtWidgets.QPushButton(self.tr('Delete'))
        self.delete_button.clicked.connect(self.delete_field)
        self.delete_dialog = QtWidgets.QDialog(self)
        self.delete_dialog.setWindowTitle(self.tr('Delete Custom Field'))
        self.delete_dialog.setLayout(QtWidgets.QVBoxLayout())
        self.delete_dialog.layout().addWidget(self.field_list)
        self.delete_dialog.layout().addWidget(self.delete_button)
        self.delete_dialog.resize(250, self.delete_dialog.height())
        self.delete_dialog.show()

    def display_coordinates(self, directory, image):
        if image in self.canvas.coordinates:
            self.lineEditX.setText(self.canvas.coordinates[image]['x'])
            self.lineEditY.setText(self.canvas.coordinates[image]['y'])
        else:
            self.lineEditX.setText('')
            self.lineEditY.setText('')

    def display_custom_fields(self, fields):

        def build(item):
            container = QtWidgets.QGroupBox(item[0], self)
            container.setObjectName(item[0])
            container.setLayout(QtWidgets.QVBoxLayout())
            if item[1].lower() == 'line':
                edit = LineText(container)
            else:
                edit = BoxText(container)
            edit.update.connect(self.canvas.save_custom_field_data)
            self.load_custom_data.connect(edit.load_data)
            container.layout().addWidget(edit)
            return container

        custom_fields = self.findChild(QtWidgets.QFrame, 'frameCustomFields')
        if custom_fields.layout() is None:
            custom_fields.setLayout(QtWidgets.QVBoxLayout())
        else:
            layout = custom_fields.layout()
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        for item in fields:
            widget = build(item)
            custom_fields.layout().addWidget(widget)
        v = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                  QtWidgets.QSizePolicy.Policy.Expanding)
        custom_fields.layout().addItem(v)
        self.get_custom_field_data()

    def display_working_directory(self, directory):
        self.labelWorkingDirectory.setText(directory)

    def display_quick_save(self):
        self.quick_save_frame.show()
        QtCore.QTimer.singleShot(500, self.quick_save_frame.hide)

    def get_custom_field_data(self):
        self.load_custom_data.emit(self.canvas.get_custom_field_data())

    def hide_custom_fields(self, hide):
        if hide is True:
            self.frameCustomField.hide()
        else:
            self.frameCustomField.show()

    def select_folder(self):
        name = QtWidgets.QFileDialog.getExistingDirectory(
            self, self.tr('Select image folder'), self.canvas.directory)
        if name != '':
            self.canvas.load([QtCore.QUrl('file:{}'.format(name))])

    def update_coordinates(self, text):
        x = self.lineEditX.text()
        y = self.lineEditY.text()
        self.canvas.save_coordinates(x, y)
