import weakref

# Maya modules

import maya.cmds as cmds
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import *

# Shiboken

try:
    from shiboken2 import wrapInstance
except:
    from shiboken import wrapInstance


from BroTools.common.broqt.vendor.Qt import *
from BroTools.common.broqt.vendor.Qt.QtWidgets import *
from BroTools.common.broqt.vendor.Qt.QtGui import *
from BroTools.common.broqt.vendor.Qt.QtCore import *


# Custom logging function with support of print-like comma-separated args and more
from BroTools.common.debug import default_logger as log

# Globals
maya_version = int(cmds.about(v=True))
# Classes
class BroMainWindow_Dockable(MayaQWidgetDockableMixin, QMainWindow):
    DOCK_LABEL_NAME = 'no name window' # Window display name
    CONTROL_NAME = 'no_name_window' # Window unique object name
    instances = list()

    def __init__(self):
        super(BroMainWindow_Dockable, self).__init__()
        self.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))
        # Not sure, but I suppose that we better keep track of instances of our window and keep Maya environment clean.
        # So we'll remove all instances before creating a new one.
        if maya_version >= 2017:
            if cmds.window(self.CONTROL_NAME + "WorkspaceControl", ex=True):
                log.debug("Removing", self.CONTROL_NAME + "WorkspaceControl")
                cmds.deleteUI(self.CONTROL_NAME + "WorkspaceControl")
                log.debug("Removed", self.CONTROL_NAME + "WorkspaceControl")
        else:
            if cmds.window(self.CONTROL_NAME + "DockControl", ex=True):
                log.debug("Removing", self.CONTROL_NAME + "DockControl")
                cmds.deleteUI(self.CONTROL_NAME + "DockControl")
                log.debug("Removed", self.CONTROL_NAME + "DockControl")
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        # Set object name and window title
        self.setObjectName(self.CONTROL_NAME)
        self.setWindowTitle(self.DOCK_LABEL_NAME)


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.build_ui()

    @staticmethod
    def delete_instances():
        for ins in BroMainWindow_Dockable.instances:
            try:
                log.debug('Delete {}'.format(ins))
            except:
                log.debug('Window reference seems to be removed already, ignore.')
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass
            try:
                BroMainWindow_Dockable.instances.remove(ins)
                del ins
            except:
                # Supress error
                pass

    def build_ui(self):
        """
        This function is called at the end of window initialization and creates your actual UI.
        Override it with your UI.
        """
        pass
        
# Functions
def getMainWindow():
    """
    Get main Maya window instance.
    """
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QMainWindow)
    return mayaMainWindow

def dock_window(dialog_class, width=440):
    """
    This function is to be updates to actually dock window on creation to the right.
    """
    dock_win = dialog_class()
    dock_win.show(dockable=True)
    return dock_win

def show_test():
    # This is how to call and show a window
    ChildTestWindow().show(dockable=True)

# Example class
class ChildTestWindow(BroMainWindow_Dockable):
    """
    Example child window inheriting from main class.
    """
    DOCK_LABEL_NAME = 'child test window'  # Window display name
    instances = list()
    CONTROL_NAME = 'child_test_win'  # Window unique object name
    def __init__(self):
        super(ChildTestWindow, self).__init__()

    def build_ui(self):
        self.my_label = QLabel('Beam me up, Scotty!')
        self.main_layout.addWidget(self.my_label)

        self.menuBar = QMenuBar()
        self.presetsMenu = self.menuBar.addMenu(("&Presets"))
        self.saveConfigAction = QAction(("&Save Settings"), self)
        self.presetsMenu.addAction(self.saveConfigAction)

        self.setMenuBar(self.menuBar)

        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Status bar ready.")

        self.setStatusBar(self.statusBar)

        self.statusBar.setObjectName("statusBar")
        self.setStyleSheet("#statusBar {background-color:#faa300;color:#fff}")
