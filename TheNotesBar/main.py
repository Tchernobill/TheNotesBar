import sys
from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QStyle, QSystemTrayIcon
from PySide6.QtGui import QIcon, QAction
from views.main_window_ui import Ui_MainWindow

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

        # Set the text of the QLabel
        self.ui.label.setText("POUETTE !!")

        # Initialize sliding variables
        self.close_position = QRect(self.screen().geometry().width() - 1, 0, 300, self.screen().geometry().height())  # Modify as needed
        self.open_position = QRect(self.screen().geometry().width() - 300, 0, 300, self.screen().geometry().height())  # Modify as needed

        # Set initial position
        self.setGeometry(self.close_position)

        # Set window flags to stay on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        # Initialize timers
        self.hover_timer = QTimer(self)
        self.hover_timer.timeout.connect(self.slide_out)
        self.return_timer = QTimer(self)
        self.return_timer.timeout.connect(self.slide_in)

        # Cursor hover handling
        self.setCursor(Qt.BlankCursor)
        self.cursor_hovered = False
        self.ui.centralwidget.enterEvent = self.cursor_enter_event
        self.ui.centralwidget.leaveEvent = self.cursor_leave_event

    def create_menu(self):
        # Create a context menu
        style = app.style()
        icon = QIcon(style.standardIcon(QStyle.SP_TitleBarMenuButton))
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("The Note Bar")
        self.tray_menu = QMenu(self)

        # Create actions for the menu items
        self.show_action = QAction("Show", self)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addSeparator()
        self.quit_action = QAction("Quit", self)
        self.tray_menu.addAction(self.quit_action)

        # Connect actions to methods
        self.show_action.triggered.connect(self.show)
        self.quit_action.triggered.connect(self.quit_application)

        # Set the context menu for the tray icon
        self.tray_icon.setContextMenu(self.tray_menu)

        # Show the tray icon
        self.tray_icon.show()

    def cursor_enter_event(self, event):
        self.cursor_hovered = True
        self.hover_timer.start(500)  # Delay before sliding out

    def cursor_leave_event(self, event):
        self.cursor_hovered = False
        self.hover_timer.stop()
        self.return_timer.start(750)  # Delay before sliding in

    def slide_out(self):
        if self.cursor_hovered:
            self.hover_timer.stop()
            self.return_timer.stop()
            animation = QPropertyAnimation(self, b"geometry", self)
            animation.setStartValue(self.close_position)
            animation.setEndValue(self.open_position)
            animation.setEasingCurve(QEasingCurve.InOutCubic)
            animation.setDuration(330)  # Slide-out duration (in milliseconds)
            animation.start()

    def slide_in(self):
        if not self.cursor_hovered:
            self.return_timer.stop()
            animation = QPropertyAnimation(self, b"geometry", self)
            animation.setStartValue(self.geometry())
            animation.setEndValue(self.close_position)
            animation.setEasingCurve(QEasingCurve.InOutCubic)
            animation.setDuration(330)  # Slide-in duration (in milliseconds)
            animation.start()

    def show_main_window(self):
        self.show()

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    print("Main window created")

    sys.exit(app.exec_())
