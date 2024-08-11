from PyQt5.QtWidgets import (QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, 
                             QCheckBox, QPushButton, QApplication, QMessageBox, QScrollArea, QWidget, QComboBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from mod_downloader import ModDownloader
from profile_manager import ProfileManager
from config import MINECRAFT_VERSIONS, MOD_LIST
import webbrowser

class ModInstallWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Mod Installer")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPixmap(QWizard.LogoPixmap, QPixmap("path_to_minecraft_logo.png"))
        self.setOption(QWizard.HaveHelpButton, True)
        self.setMinimumSize(800, 600)

        self.selected_mods = []
        self.setup_pages()

    def setup_pages(self):
        self.addPage(VersionSelectionPage())
        self.addPage(ModSelectionPage())
        self.addPage(InstallationPage())

    def accept(self):
        self.selected_mods = [
            mod['name'] for mod in MOD_LIST
            if mod['checkbox'].isChecked()
        ]
        super().accept()

class VersionSelectionPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Select Minecraft Version")
        layout = QVBoxLayout()
        self.version_selector = QComboBox()
        self.version_selector.addItems(MINECRAFT_VERSIONS)
        layout.addWidget(QLabel("Choose the Minecraft version:"))
        layout.addWidget(self.version_selector)
        self.setLayout(layout)

class ModSelectionPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Select Mods to Install")
        self.setSubTitle("Check the mods you want to install. Click on screenshots for more information.")

        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        for mod in MOD_LIST:
            mod_widget = QWidget()
            mod_layout = QHBoxLayout(mod_widget)

            mod['checkbox'] = QCheckBox(mod['name'])
            mod['checkbox'].setChecked(True)
            mod_layout.addWidget(mod['checkbox'])

            screenshot_label = QLabel()
            pixmap = QPixmap(mod['screenshot_path'])
            screenshot_label.setPixmap(pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            screenshot_label.setToolTip("Click to view full image")
            screenshot_label.mousePressEvent = lambda event, url=mod['info_url']: webbrowser.open(url)
            mod_layout.addWidget(screenshot_label)

            description = QLabel(mod['description'])
            description.setWordWrap(True)
            mod_layout.addWidget(description)

            scroll_layout.addWidget(mod_widget)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

class InstallationPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Installation")
        self.setSubTitle("Click 'Install' to begin the mod installation process.")

        layout = QVBoxLayout()
        self.status_label = QLabel("Ready to install.")
        layout.addWidget(self.status_label)

        self.install_button = QPushButton("Install")
        self.install_button.clicked.connect(self.install_mods)
        layout.addWidget(self.install_button)

        self.setLayout(layout)

    def install_mods(self):
        wizard = self.wizard()
        selected_version = wizard.page(0).version_selector.currentText()
        selected_mods = wizard.selected_mods

        downloader = ModDownloader(minecraft_version=selected_version)
        result = downloader.download_mods(selected_mods)

        if result is None:
            QMessageBox.critical(self, "Installation Failed", 
                "Some mods could not be downloaded. Check the console for details.")
            self.status_label.setText("Installation failed.")
        else:
            QMessageBox.information(self, "Installation Complete", 
                                    "Mods have been successfully installed!")
            self.status_label.setText("Installation complete.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wizard = ModInstallWizard()
    wizard.show()
    sys.exit(app.exec_())