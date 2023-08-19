from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        # Main Window Setup
        MainWindow.resize(300, 600)  # Width: 300px, Height: 600px
        
        # Central Widget
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Vertical Layout
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        
        # Label
        self.label = QLabel(self.centralwidget)
        self.label.setText("The Notes Bar")
        self.verticalLayout.addWidget(self.label)
        
        # Text Edit for Notes
        self.textEdit = QTextEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.textEdit)

        # Set Layout to Central Widget
        self.centralwidget.setLayout(self.verticalLayout)
