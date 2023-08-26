from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QListWidget, QStackedWidget, QMessageBox
from models.notes_model import NotesManager

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Initialize a QVBoxLayout for the centralwidget
        self.layout = QVBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(self.layout)

        self.noteListWidget = QListWidget(self.centralwidget)
        self.layout.addWidget(self.noteListWidget)

        self.notes_manager = NotesManager()

        try:
            notes = self.notes_manager.load_notes()
            if not notes:
                self.notes_manager.populate_sample_notes()
                notes = self.notes_manager.load_notes()

            for note in notes:
                self.noteListWidget.addItem(note.title)
                text_edit = QTextEdit()
                text_edit.setText(note.content)
                self.noteContentStackedWidget.addWidget(text_edit)

            self.noteListWidget.currentRowChanged.connect(self.noteContentStackedWidget.setCurrentIndex)

        except Exception as e:
            # Display an error message to the user
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f"An error occurred: {str(e)}")
            error_dialog.exec_()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
