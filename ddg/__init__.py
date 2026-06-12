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
__version__ = '1.0'

from .dark_mode_palette import DarkModePalette, NavyModePalette, NatureGreenPalette  # noqa: F401
from .about_dialog import AboutDialog  # noqa: F401
from .canvas import Canvas  # noqa: F401
from .point_widget import PointWidget  # noqa: F401
from .central_widget import CentralWidget  # noqa: F401
from .exception_handler import ExceptionHandler  # noqa: F401
from .workspace_dialog import WorkspaceDialog  # noqa: F401
from .workspace_widget import WorkspaceWidget  # noqa: F401
from .main_window import MainWindow  # noqa: F401
