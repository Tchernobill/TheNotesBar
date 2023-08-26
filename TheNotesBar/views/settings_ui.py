from PySide6.QtWidgets import (QDialog, QTabWidget, QVBoxLayout, QWidget, QLabel, 
                               QApplication, QCheckBox, QComboBox, QFormLayout, QLineEdit)
from PySide6.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings

        # Window Setup
        self.setWindowTitle("Settings")
        self.setGeometry(400, 200, 600, 400)  # adjust as needed

        # Tab Widget
        self.tab_widget = QTabWidget(self)

        # Tabs Setup
        self.setup_general_tab()
        self.setup_appearance_tab()
        self.setup_data_tab()

        # Other Tabs (currently placeholders)
        self.tab_shortcuts = QWidget()
        self.tab_plugins = QWidget()
        self.tab_about = QWidget()

        # Add Tabs to the TabWidget
        self.tab_widget.addTab(self.tab_general, "General")
        self.tab_widget.addTab(self.tab_appearance, "Appearance")
        self.tab_widget.addTab(self.tab_data, "Data")
        self.tab_widget.addTab(self.tab_shortcuts, "Shortcuts")
        self.tab_widget.addTab(self.tab_plugins, "Plugins")
        self.tab_widget.addTab(self.tab_about, "About")

        # Main Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.setAttribute(Qt.WA_DeleteOnClose)  # Delete the window when closed

    def setup_general_tab(self):
        """Set up the General settings tab."""
        self.tab_general = QWidget()
        layout = QVBoxLayout(self.tab_general)

        self.auto_hide_checkbox = QCheckBox("Auto Hide", self.tab_general)
        self.auto_hide_checkbox.setChecked(self.settings.auto_hide)
        self.auto_hide_checkbox.toggled.connect(self.save_general_settings)

        self.always_on_top_checkbox = QCheckBox("Always on Top", self.tab_general)
        self.always_on_top_checkbox.setChecked(self.settings.always_on_top)
        self.always_on_top_checkbox.toggled.connect(self.save_general_settings)

        layout.addWidget(self.auto_hide_checkbox)
        layout.addWidget(self.always_on_top_checkbox)

    def save_general_settings(self):
        self.settings.auto_hide = self.auto_hide_checkbox.isChecked()
        self.settings.always_on_top = self.always_on_top_checkbox.isChecked()
        self.settings.save_settings()

    def setup_appearance_tab(self):
        """Set up the Appearance settings tab."""
        self.tab_appearance = QWidget()
        layout = QVBoxLayout(self.tab_appearance)

        # Bar Position
        self.bar_position_combo = QComboBox(self.tab_appearance)
        self.bar_position_combo.addItems(["left", "right"])
        self.bar_position_combo.setCurrentText(self.settings.bar_position)
        self.bar_position_combo.currentIndexChanged.connect(self.save_appearance_settings)

        # Default Style
        self.default_style_form = QFormLayout()
        self.font_input = QLineEdit(self.settings.default_style["font"])
        self.font_size_input = QLineEdit(str(self.settings.default_style["font_size"]))
        self.bg_color_input = QLineEdit(self.settings.default_style["background_color"])
        self.text_color_input = QLineEdit(self.settings.default_style["text_color"])

        self.font_input.editingFinished.connect(self.save_appearance_settings)
        self.font_size_input.editingFinished.connect(self.save_appearance_settings)
        self.bg_color_input.editingFinished.connect(self.save_appearance_settings)
        self.text_color_input.editingFinished.connect(self.save_appearance_settings)

        self.default_style_form.addRow(QLabel("Font:"), self.font_input)
        self.default_style_form.addRow(QLabel("Font Size:"), self.font_size_input)
        self.default_style_form.addRow(QLabel("Background Color:"), self.bg_color_input)
        self.default_style_form.addRow(QLabel("Text Color:"), self.text_color_input)

        layout.addWidget(QLabel("Bar Position:"))
        layout.addWidget(self.bar_position_combo)
        layout.addLayout(self.default_style_form)

    def save_appearance_settings(self):
        self.settings.bar_position = self.bar_position_combo.currentText()
        self.settings.default_style = {
            "font": self.font_input.text(),
            "font_size": int(self.font_size_input.text()),
            "background_color": self.bg_color_input.text(),
            "text_color": self.text_color_input.text()
        }
        self.settings.save_settings()

    def setup_data_tab(self):
        """Set up the Data settings tab."""
        self.tab_data = QWidget()
        layout = QVBoxLayout(self.tab_data)

        # Placeholder for now
        label_data = QLabel("Data settings here", self.tab_data)
        layout.addWidget(label_data)

    def show_centered(self):
        """Show the settings window centered on the screen."""
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        self.move(screen_rect.center() - self.rect().center())
        self.show()

    def closeEvent(self, event):
        self.hide()  # Hide the settings window
        event.ignore()  # Ignore the close event to prevent it from propagating