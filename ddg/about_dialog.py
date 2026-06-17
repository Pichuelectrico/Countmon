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
import os
from PyQt6 import QtWidgets, QtCore, QtGui, uic
from ddg import __version__
from ddg.bundle import ui_bundle_dir

# from .ui_central_widget import Ui_central as CLASS_DIALOG
CLASS_DIALOG, _ = uic.loadUiType(os.path.join(ui_bundle_dir(), 'about_dialog.ui'))


class AboutDialog(QtWidgets.QDialog, CLASS_DIALOG):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

        self.groupBoxDevelopers.setLayout(QtWidgets.QVBoxLayout())
        self.groupBoxContributors.setLayout(QtWidgets.QVBoxLayout())
        self.groupBoxTranslators.setLayout(QtWidgets.QVBoxLayout())

        self.labelVersion.setText(__version__)

        entry = QtWidgets.QLabel('Joshua Reinoso Cevallos — {}'.format(
            self.tr('Ingeniería en Ciencias de la Computación, USFQ')))
        font = entry.font()
        font.setPointSize(10)
        entry.setFont(font)
        self.groupBoxDevelopers.layout().addWidget(entry)

        entry = QtWidgets.QLabel(
            'Isaac Reinoso Cevallos — {}'.format(
                self.tr('Ingeniería en Biotecnología, USFQ')))
        entry.setFont(font)
        self.groupBoxContributors.layout().addWidget(entry)

        role_font = QtGui.QFont(font)
        role_font.setPointSize(9)
        entry = QtWidgets.QLabel(self.tr(
            'Contribuidor principal — visión y retroalimentación de la aplicación'))
        entry.setFont(role_font)
        self.groupBoxContributors.layout().addWidget(entry)

        entry = QtWidgets.QLabel(self.tr(
            'Basado en DotDotGoose — Peter J. Ersts, American Museum of Natural History'))
        entry.setFont(font)
        self.groupBoxContributors.layout().addWidget(entry)

        entry = QtWidgets.QLabel('{} : Julie Young, [{}] {}, https://github.com/julieyoung6'.format(self.tr('Chinese (Mandarin)'), self.tr('Intern'), self.tr('Center for Biodiversity and Conservation')))
        entry.setFont(font)
        self.groupBoxTranslators.layout().addWidget(entry)

        entry = QtWidgets.QLabel('{} : Adrien Charbonneau, https://github.com/Adri-Charbonneau '.format(self.tr('French')))
        entry.setFont(font)
        self.groupBoxTranslators.layout().addWidget(entry)

        entry = QtWidgets.QLabel('{} : Charles K Barcza, https://github.com/blackPantherOS '.format(self.tr('Hungarian')))
        entry.setFont(font)
        self.groupBoxTranslators.layout().addWidget(entry)

        entry = QtWidgets.QLabel('{} : Mary Blair & Daniel López Lozano, {}'.format(self.tr('Spanish'), self.tr('Center for Biodiversity and Conservation')))
        entry.setFont(font)
        self.groupBoxTranslators.layout().addWidget(entry)

        entry = QtWidgets.QLabel('{} : Nguyễn Tuấn Anh, {}'.format(self.tr('Vietnamese'), self.tr('University of Science, Vietnam National University, Hanoi')))
        entry.setFont(font)
        self.groupBoxTranslators.layout().addWidget(entry)
