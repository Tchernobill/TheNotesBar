import sys
from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QStyle, QSystemTrayIcon, QWidget, QVBoxLayout, QListWidget, QStackedWidget, QTextEdit
from PySide6.QtGui import QIcon, QAction

from views.main_window_ui import Ui_MainWindow
from views.settings_ui import SettingsWindow  # Make sure to import the SettingsWindow
from models.settings_model import Settings
from models.notes_model import Note


# TODO : Add settings window
# TODO : Add a way to add notes
# TODO : Support Markdown, HTML and other text formatting (through a plugin system)
# TODO : Add a way to delete notes
# TODO : Add a way to edit notes
# TODO : Add a way to re-order notes
# TODO : Add a way to move notes
# TODO : Add a way to resize notes
# TODO : Add a way to change notes properties (color, font, etc...)
# TODO : Add save, load, export, import functions
# TODO : Add cloud sync functions

# TODO : Handle multiple screens
# TODO : Handle multiple windows bars
# TODO : Handle multiple windows bars positions

# TODO : Implement a plugin system
# TODO : Monitor clipboart and add a way to add notes from it
# TODO : Implement a way to change the theme
# TODO : Implement a way to change the language
# TODO : Implement a way to change the shortcut keys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

        self.create_menu() # Create the tray icon and menu

        # Initialize the settings
        self.settings_model = Settings()
        self.settings_window = None

        # Initialize sliding variables
        self.close_position = QRect(self.screen().geometry().width() - 1, 0, 300, self.screen().geometry().height())
        self.open_position = QRect(self.screen().geometry().width() - 300, 0, 300, self.screen().geometry().height())

        # Set initial position
        self.setGeometry(self.close_position)

        # Set window flags to stay on top
        if self.settings_model.always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)


        # Initialize timers for sliding effect
        self.hover_timer = QTimer(self)
        self.hover_timer.timeout.connect(self.slide_out)
        self.return_timer = QTimer(self)
        self.return_timer.timeout.connect(self.slide_in)

        # Handle cursor hover
        self.setCursor(Qt.BlankCursor)
        self.cursor_hovered = False
        self.ui.centralwidget.enterEvent = self.cursor_enter_event
        self.ui.centralwidget.leaveEvent = self.cursor_leave_event



    def create_menu(self):
        # Create a context menu for the tray icon
        style = QApplication.style()
        icon = QIcon(style.standardIcon(QStyle.SP_TitleBarMenuButton))
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("The Note Bar")
        self.tray_menu = QMenu(self)

        # Create menu actions
        self.show_action = QAction("Show", self)
        self.settings_action = QAction("Settings", self)
        self.quit_action = QAction("Quit", self)

        # Add actions to the menu
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.settings_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.quit_action)

        # Connect actions to their respective methods
        self.show_action.triggered.connect(self.show)
        self.settings_action.triggered.connect(self.open_settings)
        self.quit_action.triggered.connect(self.quit_application)

        # Set the tray icon's context menu
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def cursor_enter_event(self, event):
        self.cursor_hovered = True # Set the cursor_hovered variable to True
        self.hover_timer.start(250) # Wait 250ms before sliding # TODO : Make this a setting

    def cursor_leave_event(self, event):
        self.cursor_hovered = False # Set the cursor_hovered variable to False
        self.hover_timer.stop() # Stop the timer if the cursor leaves the window
        self.return_timer.start(500) # Wait 500ms before returning # TODO : Make this a setting

    def slide_out(self):
        if self.cursor_hovered:
            self.hover_timer.stop()
            self.return_timer.stop()
            animation = QPropertyAnimation(self, b"geometry", self)
            animation.setStartValue(self.close_position)
            animation.setEndValue(self.open_position)
            animation.setEasingCurve(QEasingCurve.InQuad)
            animation.setDuration(250)
            animation.start()

    def slide_in(self):
        if not self.cursor_hovered:
            self.return_timer.stop()
            animation = QPropertyAnimation(self, b"geometry", self)
            animation.setStartValue(self.geometry())
            animation.setEndValue(self.close_position)
            animation.setEasingCurve(QEasingCurve.OutQuad)
            animation.setDuration(250)
            animation.start()

    def open_settings(self):
        if not self.settings_window:
            self.settings_window = SettingsWindow(self.settings_model)
        self.settings_window.show_centered()

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())